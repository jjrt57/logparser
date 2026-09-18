# Gaussian Log Parser

A minimalist Streamlit web application designed for the computational chemistry community. This tool parses standard Gaussian `.log` and `.out` files to extract key thermodynamic, structural, and bonding data, providing a rapid dashboard overview, NBO analysis, and an interactive 3D visualization of the optimized geometry.

## Features

* **Data Extraction**: Final SCF Energy (Hartree), HOMO/LUMO energies (a.u., reported separately for alpha/beta spin on unrestricted calculations), and the HOMO-LUMO gap (eV).
* **Method Detection**: Reads the functional, restriction type (R/U/RO), basis set, and full route section directly from the log.
* **Structural Parsing**: Extracts final coordinates (Input/Standard orientation) and optimized parameters (bond lengths and angles).
* **NBO Analysis**: Natural population (atomic charges) and second-order perturbation (donor → acceptor E(2)) tables, when `pop=nbo` was used.
* **Interactive 3D Visualization**: Molecular viewer with standard Jmol color schemes. Hovering over a HOMO/LUMO value highlights that orbital's relative atomic contribution as a colour gradient (atom-resolved when the log includes `pop=full`; a general highlight otherwise).
* **Report Generation**: One-click download of a clean, plain-text summary report containing all extracted data.

## Live Demo
You can access the hosted version of this tool here: 
** https://goparse.streamlit.app **


## Local Installation

If you prefer to run the parser locally on your own machine, follow these steps:

1. **Clone the repository:**

   ```
   git clone git@github.com:jjrt57/logparser.git
   cd logparser
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment.

   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```
   streamlit run app.py
   ```

The application will open automatically in your default browser at `http://localhost:8501`.

## Usage

1. Drag and drop your Gaussian `.log` or `.out` file into the upload area.
2. The dashboard populates with the detected method/basis, energies, structure, and NBO tables (where present in the file).
3. Hover over the HOMO or LUMO value to see that orbital highlighted on the 3D structure.
4. Click **Download parsed data** to save the textual summary to your local machine.
