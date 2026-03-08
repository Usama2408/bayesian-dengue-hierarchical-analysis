# ============================================================
# BAYESIAN DENGUE MODELING — FULL INTEGRATED SCRIPT
# ============================================================

import os
import numpy as np
import pandas as pd
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
import seaborn as sns

FIGURE_DIR = "figures"

if os.path.exists(FIGURE_DIR):
    for file in os.listdir(FIGURE_DIR):
        file_path = os.path.join(FIGURE_DIR, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
else:
    os.makedirs(FIGURE_DIR)

# ============================================================
# SAFETY FOR WINDOWS MULTIPROCESSING
# ============================================================
if __name__ == "__main__":

    # ============================================================
    # SETTINGS
    # ============================================================
    np.random.seed(42)
    os.makedirs("figures", exist_ok=True)

    # ============================================================
    # LOAD DATA
    # ============================================================
    df = pd.read_csv("data/dengue_data_with_weather_data.csv")

    # Basic cleaning
    df = df.dropna()

    # Encode district index
    df["district_idx"] = df["District"].astype("category").cat.codes
    n_districts = df["district_idx"].nunique()

    cases = df["Cases"].values
    district_idx = df["district_idx"].values

    # ============================================================
    # FREQUENCY PLOT (AUTO SAVE + SHOW)
    # ============================================================
    plt.figure(figsize=(10, 6))
    plt.hist(cases, bins=30, edgecolor="black")
    plt.title("Distribution of Dengue Cases")
    plt.xlabel("Number of Cases")
    plt.ylabel("Frequency")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("figures/frequency_plot.png", dpi=300)
    plt.show(block=False)
    plt.pause(15)
    plt.close()

    # ============================================================
    # POISSON REGRESSION
    # ============================================================
    with pm.Model() as poisson_model:
        alpha = pm.Normal("alpha", 0, 5)
        district_effect = pm.Normal("district_effect", 0, 1, shape=n_districts)

        mu = pm.math.exp(alpha + district_effect[district_idx])

        y_obs = pm.Poisson("y_obs", mu=mu, observed=cases)

        idata_poisson = pm.sample(
            2000,
            tune=2000,
            chains=2,
            cores=2,
            target_accept=0.9,
            return_inferencedata=True,
            idata_kwargs={"log_likelihood": True}
        )

    # ============================================================
    # NEGATIVE BINOMIAL REGRESSION
    # ============================================================
    with pm.Model() as nb_model:
        alpha_mu = pm.Normal("alpha_mu", 0, 5)
        alpha_sd = pm.HalfNormal("alpha_sd", 1)
        district_effect = pm.Normal(
            "district_effect", mu=alpha_mu, sigma=alpha_sd, shape=n_districts
        )

        mu = pm.math.exp(district_effect[district_idx])
        phi = pm.Exponential("phi", 1)

        y_obs = pm.NegativeBinomial(
            "y_obs", mu=mu, alpha=phi, observed=cases
        )

        idata_nb = pm.sample(
            2000,
            tune=2000,
            chains=2,
            cores=2,
            target_accept=0.9,
            return_inferencedata=True,
            idata_kwargs={"log_likelihood": True}
        )

    # ============================================================
    # TRACE PLOTS
    # ============================================================
    az.plot_trace(idata_poisson)
    plt.tight_layout()
    plt.savefig("figures/trace_poisson.png", dpi=300)
    plt.show(block=False)
    plt.pause(2)
    plt.close()

    az.plot_trace(idata_nb)
    plt.tight_layout()
    plt.savefig("figures/trace_nb.png", dpi=300)
    plt.show(block=False)
    plt.pause(2)
    plt.close()

    # ============================================================
    # POSTERIOR PREDICTIVE CHECKS
    # ============================================================
    with poisson_model:
        ppc_pois = pm.sample_posterior_predictive(
            idata_poisson,
            return_inferencedata=True,
            random_seed=42
        )

    with nb_model:
        ppc_nb = pm.sample_posterior_predictive(
            idata_nb,
            return_inferencedata=True,
            random_seed=42
        )
    # ============================================================
# POSTERIOR PREDICTIVE CHECKS (IMPROVED VISUALIZATION)
# ============================================================

# -------- Poisson PPC --------
    y_rep_pois = (
        ppc_pois.posterior_predictive["y_obs"]
        .stack(sample=("chain", "draw"))
        .values
    )

    plt.figure(figsize=(10, 6))
    plt.hist(
        y_rep_pois.flatten(),
        bins=40,
        density=True,
        alpha=0.6,
        label="Simulated (Posterior Predictive)"
    )
    plt.hist(
        cases,
        bins=40,
        density=True,
        histtype="step",
        linewidth=2,
        color="red",
        label="Observed Data"
    )
    plt.xlabel("Monthly Dengue Cases")
    plt.ylabel("Density")
    plt.title("Posterior Predictive Check — Poisson Model")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("figures/ppc_poisson_overlay.png", dpi=300)
    plt.show(block=False)
    plt.pause(2)
    plt.close()

    # -------- Negative Binomial PPC --------
    y_rep_nb = (
        ppc_nb.posterior_predictive["y_obs"]
        .stack(sample=("chain", "draw"))
        .values
    )

    plt.figure(figsize=(10, 6))
    plt.hist(
        y_rep_nb.flatten(),
        bins=40,
        density=True,
        alpha=0.6,
        label="Simulated (Posterior Predictive)"
    )
    plt.hist(
        cases,
        bins=40,
        density=True,
        histtype="step",
        linewidth=2,
        color="red",
        label="Observed Data"
    )
    plt.xlabel("Monthly Dengue Cases")
    plt.ylabel("Density")
    plt.title("Posterior Predictive Check — Negative Binomial Model")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("figures/ppc_nb_overlay.png", dpi=300)
    plt.show(block=False)
    plt.pause(2)
    plt.close()

    # az.plot_ppc(ppc_pois, group="posterior")
    # plt.savefig("figures/ppc_poisson.png", dpi=300)
    # plt.show(block=False)
    # plt.pause(2)
    # plt.close()

    # az.plot_ppc(ppc_nb, group="posterior")
    # plt.savefig("figures/ppc_nb.png", dpi=300)
    # plt.show(block=False)
    # plt.pause(2)
    # plt.close()
    
    
    # ============================================================
    # MODEL COMPARISON (WAIC + LOO)
    # ============================================================
    waic_pois = az.waic(idata_poisson)
    waic_nb = az.waic(idata_nb)

    loo_pois = az.loo(idata_poisson)
    loo_nb = az.loo(idata_nb)

    with open("figures/model_comparison.txt", "w") as f:
        f.write("MODEL COMPARISON RESULTS\n")
        f.write("========================\n\n")
        f.write(f"Poisson WAIC (elpd): {waic_pois.elpd_waic:.2f}\n")
        f.write(f"Negative Binomial WAIC (elpd): {waic_nb.elpd_waic:.2f}\n\n")
        f.write(f"Poisson LOO: {loo_pois.elpd_loo:.2f}\n")
        f.write(f"Negative Binomial LOO: {loo_nb.elpd_loo:.2f}\n")

    # ============================================================
    # SPATIAL VISUALIZATION (LAT / LON)
    # ============================================================
    spatial_df = pd.DataFrame({
        "Latitude": df.groupby("District", observed=True)["Latitude"].mean().values,
        "Longitude": df.groupby("District", observed=True)["Longitude"].mean().values,
        "Cases": df.groupby("District", observed=True)["Cases"].mean().values
    })

    plt.figure(figsize=(8, 6))
    sc = plt.scatter(
        spatial_df["Longitude"],
        spatial_df["Latitude"],
        c=spatial_df["Cases"],
        s=80,
        cmap="viridis"
    )
    plt.colorbar(sc, label="Average Dengue Cases")
    plt.title("Spatial Distribution of Dengue Cases")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("figures/spatial_dengue_map.png", dpi=300)
    plt.show(block=False)
    plt.pause(2)
    plt.close()

    # ============================================================
    # FINAL SUMMARY
    # ============================================================
    print("✔ Analysis complete")
    print("✔ All plots saved in /figures")
    print("✔ No manual figure closing required")