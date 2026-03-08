# bayesian-dengue-hierarchical-analysis
Bayesian hierarchical modeling of dengue fever incidence using PyMC. Compares Poisson vs Negative Binomial models with LOO cross-validation. Academic project - TU Dortmund University.


# Bayesian Hierarchical Analysis of Dengue Fever Incidence

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyMC](https://img.shields.io/badge/PyMC-5.0+-orange.svg)](https://www.pymc.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> A Bayesian hierarchical modeling approach to predict dengue fever risk using district-level case counts with climatic and spatial covariates.

## 📊 Project Overview

This project applies **Bayesian hierarchical modeling** to analyze dengue fever incidence across districts, accounting for spatial heterogeneity and overdispersion in count data. We compare Poisson and Negative Binomial regression models using Leave-One-Out Cross-Validation (LOO-CV).

**Academic Context:**
- Course: Advanced Bayesian Data Analysis
- Institution: TU Dortmund University
- Date: March 2025
- Authors: Usama Tauqeer Katib, Devensingh Rajput

## 🎯 Key Features

- **Hierarchical Bayesian Models**: Poisson and Negative Binomial regression with random district effects
- **Robust Model Comparison**: LOO cross-validation for out-of-sample predictive performance
- **Comprehensive Diagnostics**: Trace plots, R-hat statistics, posterior predictive checks
- **Publication-Ready Visualizations**: Professional plots for all diagnostics and results
- **Reproducible Research**: Complete code and LaTeX report included

## 🔬 Methodology

### Models Implemented

1. **Hierarchical Poisson Model**
   - Assumes variance = mean
   - Baseline model for count data
   
2. **Hierarchical Negative Binomial Model** ⭐ (Selected)
   - Accounts for overdispersion
   - Superior predictive performance (ΔELPD = 911.4)

### Prior Specifications

- Intercept: Normal(0, 5)
- District effects: Normal(0, α_sd)
- Dispersion: Exponential(1)
- All priors weakly informative and domain-appropriate

### Key Results

- **Model Comparison**: Negative Binomial significantly outperforms Poisson
- **ELPD Difference**: -911.4 (strong evidence for NegBin)
- **Convergence**: R̂ ≈ 1.00 for all parameters
- **Predictive Performance**: 95% credible intervals well-calibrated

## 📁 Repository Structure
```
├── code/
│   ├── data_preprocessing.py       # Data cleaning and preparation
│   ├── model_poisson.py            # Hierarchical Poisson model
│   ├── model_negbin.py             # Hierarchical Negative Binomial model
│   ├── diagnostics.py              # Convergence diagnostics
│   └── visualizations.py           # Generate all plots
├── data/
│   └── dengue_district_data.csv    # District-level case counts
├── figures/
│   ├── workflow_diagram.pdf
│   ├── trace_plots.pdf
│   ├── density_plots.pdf
│   ├── prior_predictive.pdf
│   ├── ppc_poisson.pdf
│   ├── ppc_negbin.pdf
│   └── spatial_map.pdf
├── report/
│   ├── bayesian_dengue_report.tex  # Full LaTeX report
│   ├── bayesian_dengue_report.pdf  # Compiled PDF
│   └── references.bib              # Bibliography
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── LICENSE                         # MIT License
```

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.8+
PyMC 5.0+
ArviZ 0.15+
NumPy, Pandas, Matplotlib, Seaborn
```

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/bayesian-dengue-hierarchical-analysis.git
cd bayesian-dengue-hierarchical-analysis

# Install dependencies
pip install -r requirements.txt
```

### Running the Analysis
```bash
# 1. Preprocess data
python code/data_preprocessing.py

# 2. Fit Poisson model
python code/model_poisson.py

# 3. Fit Negative Binomial model
python code/model_negbin.py

# 4. Run diagnostics
python code/diagnostics.py

# 5. Generate visualizations
python code/visualizations.py
```

### Quick Start with Jupyter Notebook
```bash
jupyter notebook notebooks/full_analysis.ipynb
```

## 📖 Documentation

Full documentation available in the [report](report/bayesian_dengue_report.pdf) including:
- Detailed methodology
- Prior specifications and justifications
- Complete convergence diagnostics
- Posterior predictive checks
- Model comparison results
- Limitations and future work


## 🛠️ Technologies Used

- **Bayesian Modeling**: PyMC5, ArviZ
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Model Comparison**: LOO-CV (via ArviZ)
- **Reporting**: LaTeX, BibTeX

## 📈 Results Summary

✅ **Overdispersion confirmed**: Variance >> Mean  
✅ **Spatial heterogeneity**: Significant district effects  
✅ **Model selection**: Negative Binomial strongly preferred  
✅ **Convergence**: All chains converged (R̂ ≈ 1.00)  
✅ **Predictive performance**: Well-calibrated uncertainty  

## 🎓 Academic Output

- **Full Report**: [PDF](report/bayesian_dengue_report.pdf)
- **Course**: Advanced Bayesian Data Analysis

## 🤝 Contributing

This is an academic project. If you find issues or have suggestions:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 👥 Authors

**Usama Tauqeer Katib** - [GitHub](https://github.com/yourusername)  
Student ID: 255679  
Email: usama.katib@tu-dortmund.de

**Devensingh Rajput** - [GitHub](https://github.com/partnerusername)  
Student ID: 259637  
Email: devensingh.rajput@tu-dortmund.de

## 🙏 Acknowledgments

- Prof. Paul Buerkner - Course instructor
- TU Dortmund University - Department of Statistics
- PyMC Development Team - Excellent probabilistic programming framework
- Centers for Disease Control (CDC) - BRFSS data source

## 📚 References

1. Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.
2. McElreath, R. (2020). *Statistical Rethinking* (2nd ed.). CRC Press.
3. Vehtari, A., Gelman, A., & Gabry, J. (2017). Practical Bayesian model evaluation using LOO cross-validation. *Statistics and Computing*, 27(5), 1413-1432.

## 📞 Contact

For questions about this project:
- Open an issue on GitHub
- Email: usama.katib@tu-dortmund.de

---

**⭐ If you find this project useful, please give it a star!**

*Last Updated: March 2025*
```

---

## 🏷️ **GitHub Topics/Tags to Add:**

When you create the repo, add these topics:
```
bayesian-statistics
hierarchical-models
pymc
dengue-fever
epidemiology
mcmc
negative-binomial
spatial-analysis
loo-cv
data-science
academic-research
tu-dortmund
