# Gaussian Log Parser

A minimalist Streamlit web application designed for the computational chemistry community. This tool parses standard Gaussian `.log` and `.out` files to extract key thermodynamic and structural data, providing both a rapid dashboard overview and an interactive 3D visualization of the optimized geometry.

## Features

* **Data Extraction**: Automatically retrieves Final SCF Energy (Hartree), HOMO, and LUMO energies (a.u.).
* **Structural Parsing**: Extracts final coordinates (Input/Standard orientation) and optimized parameters (bond lengths and angles).
* **3D Visualization**: Interactive molecular viewer powered by `py3Dmol` with standard Jmol color schemes and a dynamic legend.
* **Report Generation**: One-click download of a clean, plain-text summary report containing all extracted data.

## Live Demo
You can access the hosted version of this tool here: 
**[Insert your Streamlit Cloud URL here]**

## Local Installation

If you prefer to run the parser locally on your own machine, follow these steps:

1. **Clone the repository:**
   
   git clone git@github.com:jjrt57/logparser.git
   cd logparser

2. ** Install dependencies:**
    It is recommended to use a virtual environment.
     
      pip install -r requirements.txt

3. Run the application:

      streamlit run app.py

The application will automatically open in your default web browser at `http://localhost:8501`.

## Usage

1. Drag and drop your Gaussian `.log` or `.out` file into the upload area.
2. The dashboard will instantly populate with the extracted metrics and render the 3D structure.
3. Click **Download Parsed Data** to save the textual summary to your local machine.
