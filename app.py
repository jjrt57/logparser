import streamlit as st
import py3Dmol
from stmol import showmol

# --- Constants & Dictionaries ---
ATOMIC_SYMBOLS = {
    1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 10: 'Ne',
    11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P', 16: 'S', 17: 'Cl', 18: 'Ar',
    19: 'K', 20: 'Ca', 21: 'Sc', 22: 'Ti', 23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co',
    28: 'Ni', 29: 'Cu', 30: 'Zn', 31: 'Ga', 32: 'Ge', 33: 'As', 34: 'Se', 35: 'Br', 36: 'Kr',
    37: 'Rb', 38: 'Sr', 39: 'Y', 40: 'Zr', 41: 'Nb', 42: 'Mo', 43: 'Tc', 44: 'Ru', 45: 'Rh',
    46: 'Pd', 47: 'Ag', 48: 'Cd', 49: 'In', 50: 'Sn', 51: 'Sb', 52: 'Te', 53: 'I', 54: 'Xe',
    55: 'Cs', 56: 'Ba', 57: 'La', 58: 'Ce', 59: 'Pr', 60: 'Nd', 61: 'Pm', 62: 'Sm', 63: 'Eu',
    64: 'Gd', 65: 'Tb', 66: 'Dy', 67: 'Ho', 68: 'Er', 69: 'Tm', 70: 'Yb', 71: 'Lu', 72: 'Hf',
    73: 'Ta', 74: 'W', 75: 'Re', 76: 'Os', 77: 'Ir', 78: 'Pt', 79: 'Au', 80: 'Hg', 81: 'Tl',
    82: 'Pb', 83: 'Bi' 
}

JMOL_COLORS = {
    'H': '#FFFFFF', 'He': '#D9FFFF', 'Li': '#CC80FF', 'Be': '#C2FF00', 'B': '#00FF00',
    'C': '#909090', 'N': '#3050F8', 'O': '#FF0D0D', 'F': '#90E050', 'Ne': '#B3E3F5',
    'Na': '#AB5CF2', 'Mg': '#8AFF00', 'Al': '#BFA6A6', 'Si': '#F0C8A0', 'P': '#FF8000',
    'S': '#FFFF30', 'Cl': '#1FF01F', 'Ar': '#80D1E3', 'K': '#8F40D4', 'Ca': '#3DFF00',
    'Sc': '#E6E6E6', 'Ti': '#BFC2C7', 'V': '#A6A6AB', 'Cr': '#8A99C7', 'Mn': '#9C7AC7',
    'Fe': '#E06633', 'Co': '#F090A0', 'Ni': '#50D050', 'Cu': '#C88033', 'Zn': '#7D80B0',
    'Ga': '#C28F8F', 'Ge': '#668F8F', 'As': '#BD80E3', 'Se': '#FFA100', 'Br': '#A62929',
    'Kr': '#5CB8D1', 'Rb': '#702EB0', 'Sr': '#00FF00', 'Y': '#94FFFF', 'Zr': '#94E0E0',
    'Nb': '#73C2C9', 'Mo': '#54B5B5', 'Tc': '#3B9E9E', 'Ru': '#248F8F', 'Rh': '#0A7D8C',
    'Pd': '#006985', 'Ag': '#C0C0C0', 'Cd': '#FFD98F', 'In': '#A67573', 'Sn': '#668080',
    'Sb': '#9E63B5', 'Te': '#D47A00', 'I': '#940094', 'Xe': '#429EB0', 'Cs': '#57178F',
    'Ba': '#00C900', 'La': '#70D4FF', 'Ce': '#FFFFC7', 'Pr': '#D9FFC7', 'Nd': '#C7FFC7',
    'Pm': '#A3FFC7', 'Sm': '#8FFFC7', 'Eu': '#61FFC7', 'Gd': '#45FFC7', 'Tb': '#30FFC7',
    'Dy': '#1FFFC7', 'Ho': '#00FF9C', 'Er': '#00E675', 'Tm': '#00D452', 'Yb': '#00BF38',
    'Lu': '#00AB24', 'Hf': '#4DC2FF', 'Ta': '#4DA6FF', 'W': '#2194D6', 'Re': '#267DAB',
    'Os': '#266696', 'Ir': '#175487', 'Pt': '#D0D0E0', 'Au': '#FFD123', 'Hg': '#B8B8D0',
    'Tl': '#A6544D', 'Pb': '#575961', 'Bi': '#9E4FB5'
}

LEGEND_SIZES = {
    'H': 10, 'He': 11, 'Li': 22, 'Be': 16, 'B': 15,
    'C': 16, 'N': 15, 'O': 14, 'F': 14, 'Ne': 15,
    'Na': 24, 'Mg': 21, 'Al': 19, 'Si': 20, 'P': 19,
    'S': 18, 'Cl': 18, 'Ar': 19, 'K': 26, 'Ca': 24,
    'Sc': 22, 'Ti': 21, 'V': 20, 'Cr': 19, 'Mn': 19,
    'Fe': 19, 'Co': 19, 'Ni': 19, 'Cu': 19, 'Zn': 20,
    'Ga': 20, 'Ge': 20, 'As': 19, 'Se': 19, 'Br': 19,
    'Kr': 20, 'Rb': 27, 'Sr': 25, 'Y': 24, 'Zr': 22,
    'Nb': 21, 'Mo': 20, 'Tc': 20, 'Ru': 19, 'Rh': 19,
    'Pd': 19, 'Ag': 21, 'Cd': 22, 'In': 22, 'Sn': 22,
    'Sb': 21, 'Te': 21, 'I': 21, 'Xe': 22, 'Cs': 29,
    'Ba': 27, 'La': 25, 'Ce': 25, 'Pr': 25, 'Nd': 25,
    'Pm': 24, 'Sm': 24, 'Eu': 24, 'Gd': 24, 'Tb': 23,
    'Dy': 23, 'Ho': 23, 'Er': 23, 'Tm': 23, 'Yb': 23,
    'Lu': 23, 'Hf': 22, 'Ta': 21, 'W': 20, 'Re': 20,
    'Os': 19, 'Ir': 19, 'Pt': 20, 'Au': 21, 'Hg': 21,
    'Tl': 22, 'Pb': 22, 'Bi': 22
}

# --- Core Functions ---
def parse_gaussian_log(file_content):
    lines = file_content.splitlines()
    
    results = {
        "energy": "N/A",
        "homo": "N/A",
        "lumo": "N/A",
        "coordinates": [],
        "parameters": []
    }
    
    for line in reversed(lines):
        if "SCF Done:" in line:
            results["energy"] = line.split()[4]
            break
            
    occs = []
    virts = []
    for line in lines:
        if "occ. eigenvalues" in line:
            occs.extend([float(x) for x in line.split()[4:]])
            virts = [] 
        elif "virt. eigenvalues" in line:
            if len(virts) == 0: 
                virts.extend([float(x) for x in line.split()[4:]])
                
    if occs and virts:
        results["homo"] = str(occs[-1])
        results["lumo"] = str(virts[0])
        
    coord_start = -1
    for i in range(len(lines)-1, -1, -1):
        if "Standard orientation:" in lines[i] or "Input orientation:" in lines[i]:
            coord_start = i + 5
            break
    
    if coord_start != -1:
        for j in range(coord_start, len(lines)):
            if "---" in lines[j]:
                break
            results["coordinates"].append(lines[j].strip())
            
    param_start = -1
    for i in range(len(lines)-1, -1, -1):
        if "!   Optimized Parameters   !" in lines[i]:
            param_start = i + 5
            break
            
    if param_start != -1:
        for j in range(param_start, len(lines)):
            if "---" in lines[j]:
                break
            results["parameters"].append(lines[j].strip())
            
    return results

def convert_to_xyz(gaussian_coords):
    num_atoms = len(gaussian_coords)
    xyz_str = f"{num_atoms}\nGenerated by Streamlit Parser\n"
    
    for line in gaussian_coords:
        parts = line.split()
        if len(parts) >= 6:
            atomic_num = int(parts[1])
            symbol = ATOMIC_SYMBOLS.get(atomic_num, "X")
            x, y, z = parts[3], parts[4], parts[5]
            xyz_str += f"{symbol} {x} {y} {z}\n"
            
    return xyz_str

def generate_text_report(results):
    report = "--- GAUSSIAN LOG PARSER REPORT ---\n\n"
    report += f"Final Energy: {results['energy']} Hartree\n"
    report += f"HOMO Energy:  {results['homo']} a.u.\n"
    report += f"LUMO Energy:  {results['lumo']} a.u.\n\n"
    
    report += "--- FINAL COORDINATES ---\n"
    report += "Center  Atomic  Atomic  Coordinates (Angstroms)\n"
    report += "Number  Number  Type    X           Y           Z\n"
    report += "-"*65 + "\n"
    for c in results['coordinates']:
        report += f"{c}\n"
        
    report += "\n--- OPTIMIZED PARAMETERS ---\n"
    for p in results['parameters']:
        report += f"{p}\n"
        
    return report

# --- User Interface ---
st.set_page_config(page_title="Gaussian Log Parser", layout="centered")

st.title("Gaussian Output Parser")
st.markdown("Upload a Gaussian output file to extract final geometries, energies, and molecular orbitals.")

uploaded_file = st.file_uploader("Select .log or .out file", type=["log", "out"], label_visibility="collapsed")

if uploaded_file is not None:
    content = uploaded_file.getvalue().decode("utf-8")
    
    with st.spinner("Parsing data..."):
        results = parse_gaussian_log(content)
    
    st.divider()
    
    #Metric Layout
    st.subheader("Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Final Energy (Hartree)", results['energy'])
    col2.metric("HOMO (a.u.)", results['homo'])
    col3.metric("LUMO (a.u.)", results['lumo'])
    
    st.divider()
    
    # 3D Visualization
    if results["coordinates"]:
        st.subheader("Structure")
        
        # 1. Determine which unique atoms are in this specific molecule
        unique_atoms = set()
        for line in results["coordinates"]:
            parts = line.split()
            if len(parts) >= 6:
                atomic_num = int(parts[1])
                symbol = ATOMIC_SYMBOLS.get(atomic_num, "X")
                unique_atoms.add(symbol)
                
        # 2. Buil HTML 
        legend_html = "<div style='display: flex; gap: 20px; margin-bottom: 15px; padding: 10px; background-color: rgba(128,128,128,0.1); border-radius: 5px; flex-wrap: wrap;'>"
        legend_html += "<span style='font-weight: 600; font-size: 14px; margin-right: 10px; display: flex; align-items: center;'>Atoms:</span>"
        
        for atom in sorted(unique_atoms):
            color = JMOL_COLORS.get(atom, "#FF1493")
            size = LEGEND_SIZES.get(atom, 16)
            
            # Formatted on a single line to prevent Streamlit from treating it as a Markdown code block
            legend_html += f"<div style='display: flex; align-items: center; font-size: 14px;'><div style='width: {size}px; height: {size}px; background-color: {color}; border-radius: 50%; border: 1px solid #999; margin-right: 8px;'></div>{atom}</div>"
            
        legend_html += "</div>"
        
        # Render the legend above the viewer
        st.markdown(legend_html, unsafe_allow_html=True)
        
        # 3. Render the 3D Viewer
        xyz_data = convert_to_xyz(results["coordinates"])
        view = py3Dmol.view(width=800, height=400)
        view.addModel(xyz_data, "xyz")
        
        # Apply the Jmol color scheme to the 3D rendering
        view.setStyle({"stick": {"radius": 0.15, "colorscheme": "Jmol"}, 
                       "sphere": {"scale": 0.25, "colorscheme": "Jmol"}})
        view.zoomTo()
        
        showmol(view, height=400, width=800)
    
    st.divider()
    
    # File Download
    report_text = generate_text_report(results)
    st.download_button(
        label="Download Parsed Data",
        data=report_text,
        file_name=f"{uploaded_file.name}_parsed.txt",
        mime="text/plain"
    )