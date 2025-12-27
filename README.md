**Project 8 Introduction and Explanation**

**1.	Jupyter Notebook: land_fraction_and_lifetime_exposure.ipynb**

*1.1 Course Context*

This Jupyter Notebook presents a demonstration of Python-based methodologies employed for the analysis of the relationship between land surface fractions and lifetime exposure metrics. The emphasis is placed on methodological understanding, reproducibility, and transparent data handling.

*1.2 Objectives*

The management of gridded environmental datasets within the Python programming environment is imperative for effective analysis and interpretation of ecological data.
The application of pre-processing steps, including masking and aggregation, is a prerequisite for the subsequent analysis.
The computation of land surface fractions and exposure-related metrics is imperative.
The visualisation of spatial patterns and relationships is an essential component of the analysis.
The results must be interpreted in an environmental context.
Data input: The data input will include land surface or land cover fractions and exposure-related variables. It should be noted that the datasets are not included in the present document and must be provided separately.

*1.3 Requirements*

It’s necessary to create an environment and to install the following packages. The Python packages that are required are as follows:
  • pandas: 1.4.2
  
  • numpy: 1.22.4

  • scipy: 1.8.1
  
  • matplotlib: 3.5.3
  
  •	xarray: 2022.6.0
  
  •	geopandas: 0.12.2

*1.4 Structure of the notebook*

1. The following section will provide a concise overview of the introduction and setup.
2. Data loading
3. The processes of pre-processing and quality control are of paramount importance.
4. The following text will provide a detailed explanation of the computation of metrics.
5. Visualisation
6. Discussion

The following steps are required in order to successfully execute the given procedure: firstly, install the necessary packages; secondly, provide the required input data; and finally, run the notebook cells in sequence

**2.	Python Script: Python_Script_Spyder.py**

*2.1	Course Context*

Following the same methodological approach as presented in the accompanying Jupyter Notebook, it demonstrates the use of Python for processing, analysing and visualising environmental or climate-related data.
The main objective of this script is to replicate and present the analysis from the notebook in a linear Python workflow, showing how an interactive notebook can be converted into a structured Python execution process.

*2.2	Requirements*

2.2.1	Spyder & Conda Environment Setup – Full Recap

This section summarizes the complete process used to fix Spyder, avoid breaking Jupyter, and create a clean and stable Conda environment setup. It includes the rationale and exact commands used, and can be kept as a reference or shared with a TA.

2.2.2 Initial Problem

Spyder failed to start correctly due to kernel and console errors caused by environment mixing and Windows Python path conflicts. Jupyter was already working and needed to remain untouched.

2.2.3 Final Design Decision

A professional separation of environments was adopted: base for Conda only, project8_env for Jupyter, and spyder_env for Spyder and scientific libraries.

2.2.4 Creating the Spyder Environment

conda create -n spyder_env python=3.10 spyder=5.5 spyder-kernels=2.5 -y

2.2.5 Installing Required Libraries

All scientific libraries were installed using conda-forge to ensure compatibility on Windows.
  conda install -c conda-forge numpy=1.22.4
  conda install -c conda-forge pandas=1.4.2
  conda install -c conda-forge scipy=1.8.1
  conda install -c conda-forge matplotlib=3.5.3
  OR
  conda install -c conda-forge matplotlib=3.8
  conda install -c conda-forge xarray=2022.6.0
  conda install -c conda-forge geopandas=0.12.2

2.2.6 Launching Spyder

Spyder is launched from its dedicated environment using:
  conda activate spyder_env

2.2.7 Final State

Spyder works correctly, all imports succeed, and Jupyter remains fully intact in project8_env.

*3.	Structure*

The Python script has a clear, linear execution flow and is divided into several logical sections. First, all the necessary Python libraries are imported, and the basic configuration settings are defined. Next, external environmental or climate-related input data is loaded from a file. The data are then preprocessed, including cleaning, masking and basic transformations necessary for the analysis. The core analysis is then performed, with relevant metrics computed based on the processed data. Finally, the results are visualised using standard plotting routines. This structure mirrors the workflow of the corresponding Jupyter notebook, demonstrating how an interactive notebook-based analysis can be translated into a reproducible Python script.

In summary, the script shows how an interactive Jupyter Notebook workflow can be converted into a structured, reproducible Python script that supports best practices in scientific data analysis.
