# Copyright (c) 2026 Rohit Nongmaithem
# Licensed under the MIT License.
# See LICENSE file in the project root for full license information.

import json
import re

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

HARTREE_TO_EV = 27.211386245988

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

# =====================================================================
# Parsing
# =====================================================================

def parse_route_and_method(lines):
    """Route section (the '# ...' command line) plus the method/basis,
    pulled from the more reliable 'SCF Done' and 'Standard basis' lines
    rather than trying to fully interpret the (often long, wrapped)
    route line."""
    route = None
    for i, line in enumerate(lines[:200]):
        if re.match(r'^\s*-{5,}\s*$', line):
            j = i + 1
            if j < len(lines) and lines[j].strip().startswith('#'):
                collected = []
                k = j
                while k < len(lines) and not re.match(r'^\s*-{5,}\s*$', lines[k]):
                    collected.append(lines[k].strip())
                    k += 1
                route = ' '.join(collected).strip()
                break

    method_raw = None
    for line in reversed(lines):
        m = re.search(r'SCF Done:\s*E\((\S+)\)', line)
        if m:
            method_raw = m.group(1)
            break

    restriction, functional = None, method_raw
    if method_raw:
        upper = method_raw.upper()
        if upper.startswith('RO'):
            restriction, functional = 'RO', method_raw[2:]
        elif upper.startswith('U'):
            restriction, functional = 'U', method_raw[1:]
        elif upper.startswith('R'):
            restriction, functional = 'R', method_raw[1:]

    basis = None
    for line in lines:
        m = re.search(r'Standard basis:\s*(.+)', line)
        if m:
            basis = m.group(1).strip()
            break

    return {
        "route": route,
        "method_raw": method_raw,
        "functional": functional,
        "restriction": restriction,
        "basis": basis,
    }


def parse_homo_lumo(lines):
    """Bug fix: the previous version matched any 'occ./virt. eigenvalues'
    line without checking the Alpha/Beta label, so on unrestricted (open
    shell) jobs the alpha and beta blocks got silently concatenated and
    the reported HOMO/LUMO ended up being whichever spin's block came
    last in the file - with no indication which one it was.

    This tracks alpha and beta separately, and only resets a spin/type's
    accumulator when a *new* (non-contiguous) run of that label starts,
    so multi-line blocks are still combined correctly and, for files with
    several SCF cycles (e.g. an optimisation), only the LAST block for
    each label is kept - consistent with how the energy is already read
    from the last 'SCF Done' line.
    """
    blocks = {"alpha_occ": [], "alpha_virt": [], "beta_occ": [], "beta_virt": []}
    last_label = None
    label_re = re.compile(r'^\s*(Alpha|Beta)\s+(occ\.|virt\.)\s+eigenvalues\s+--\s*(.*)$')

    for line in lines:
        m = label_re.match(line)
        if not m:
            continue
        spin, kind, rest = m.group(1), m.group(2), m.group(3)
        key = ("alpha" if spin == "Alpha" else "beta") + ("_occ" if kind == "occ." else "_virt")
        try:
            vals = [float(x) for x in rest.split()]
        except ValueError:
            continue
        if key != last_label:
            blocks[key] = []
        blocks[key].extend(vals)
        last_label = key

    unrestricted = bool(blocks["beta_occ"] or blocks["beta_virt"])
    out = {"unrestricted": unrestricted}
    if blocks["alpha_occ"]:
        out["homo_alpha"] = blocks["alpha_occ"][-1]
    if blocks["alpha_virt"]:
        out["lumo_alpha"] = blocks["alpha_virt"][0]
    if unrestricted:
        if blocks["beta_occ"]:
            out["homo_beta"] = blocks["beta_occ"][-1]
        if blocks["beta_virt"]:
            out["lumo_beta"] = blocks["beta_virt"][0]
    return out


def _find_last_index(lines, pattern):
    idx = None
    for i, line in enumerate(lines):
        if re.search(pattern, line):
            idx = i
    return idx


def parse_mo_coefficient_weights(lines, num_atoms, spin_prefix="Alpha "):
    """Best-effort parse of the LAST '<spin>Molecular Orbital Coefficients'
    table (only printed when the route section includes pop=full / pop=reg)
    to get each atom's relative contribution to the HOMO and LUMO, as the
    sum of squared AO coefficients on that atom's basis functions.

    This is an AO-population-style weighting, not a real-space isosurface -
    it tells you which atoms carry more HOMO/LUMO character, not the shape
    or sign (phase) of the orbital lobes. A true isosurface needs a
    Gaussian cube file (via cubegen) or an .fchk, which a standard .log
    does not contain.

    Returns {"homo_weights": [...], "lumo_weights": [...], "homo_mo": n,
    "lumo_mo": n} indexed in Center-Number order (1..num_atoms), or None
    if the section isn't present or doesn't parse confidently.
    """
    heading_pat = rf'^\s*{spin_prefix}Molecular Orbital Coefficients\s*:?\s*$'
    start = _find_last_index(lines, heading_pat)
    if start is None and spin_prefix == "Alpha ":
        start = _find_last_index(lines, r'^\s*Molecular Orbital Coefficients\s*:?\s*$')
    if start is None:
        return None

    end = len(lines)
    for i in range(start + 1, len(lines)):
        if re.search(r'Density Matrix', lines[i]) or (
            i > start + 1 and re.search(r'Molecular Orbital Coefficients', lines[i])
        ):
            end = i
            break
    section = lines[start:end]
    n = len(section)

    mo_index_re = re.compile(r'^\s*(\d+(?:\s+\d+)*)\s*$')
    occ_row_re = re.compile(r'^\s*([OV](?:\s+[OV])*)\s*$')
    eig_row_re = re.compile(r'^\s*Eigenvalues\s*--\s*(.*)$')

    try:
        i = 0
        global_mo = []
        while i < n:
            m_idx = mo_index_re.match(section[i])
            if m_idx and i + 2 < n:
                mo_nums = [int(x) for x in m_idx.group(1).split()]
                m_occ = occ_row_re.match(section[i + 1])
                m_eig = eig_row_re.match(section[i + 2])
                if m_occ and m_eig and len(m_occ.group(1).split()) == len(mo_nums):
                    block_start = i + 3
                    n_cols = len(mo_nums)
                    for col_idx, (mo_num, occ) in enumerate(zip(mo_nums, m_occ.group(1).split())):
                        global_mo.append({"mo": mo_num, "occ": occ, "block_start": block_start,
                                           "n_cols": n_cols, "col": col_idx})
                    i += 3
                    continue
            i += 1

        if not global_mo:
            return None

        occ_mos = [g for g in global_mo if g["occ"] == "O"]
        virt_mos = [g for g in global_mo if g["occ"] == "V"]
        if not occ_mos or not virt_mos:
            return None
        homo_info = max(occ_mos, key=lambda g: g["mo"])
        lumo_info = min(virt_mos, key=lambda g: g["mo"])

        def sum_squares_for(col_info):
            block_start, n_cols, col = col_info["block_start"], col_info["n_cols"], col_info["col"]
            weights = [0.0] * (num_atoms + 1)
            current_atom = None
            j = block_start
            while j < n:
                line = section[j]
                if mo_index_re.match(line) and j + 2 < n and occ_row_re.match(section[j + 1]):
                    break
                tokens = line.split()
                if len(tokens) < n_cols + 1:
                    if line.strip() == "" and current_atom is not None:
                        break
                    j += 1
                    continue
                coef_tokens = tokens[-n_cols:]
                try:
                    coefs = [float(t) for t in coef_tokens]
                except ValueError:
                    j += 1
                    continue
                left = tokens[:-n_cols]
                if not left or not left[0].isdigit():
                    j += 1
                    continue
                if len(left) >= 3 and left[1].isdigit() and left[2].isalpha():
                    current_atom = int(left[1])
                if current_atom is not None and 1 <= current_atom <= num_atoms:
                    weights[current_atom] += coefs[col] ** 2
                j += 1
            return weights[1:]

        return {
            "homo_weights": sum_squares_for(homo_info),
            "lumo_weights": sum_squares_for(lumo_info),
            "homo_mo": homo_info["mo"],
            "lumo_mo": lumo_info["mo"],
        }
    except Exception:
        # Any surprise in the table's formatting -> gracefully say "unavailable"
        # rather than risk silently mapping coefficients to the wrong atom.
        return None


def parse_natural_charges(lines):
    start = None
    for i, line in enumerate(lines):
        if "Summary of Natural Population Analysis" in line:
            start = i
            break
    if start is None:
        return None
    row_re = re.compile(r'^\s*(\d+)\s+([A-Za-z]{1,2})\s+(-?\d+\.\d+)')
    charges, misses = [], 0
    for line in lines[start + 1: start + 400]:
        m = row_re.match(line)
        if m:
            charges.append({"index": int(m.group(1)), "symbol": m.group(2), "charge": float(m.group(3))})
            misses = 0
        elif charges:
            misses += 1
            if misses >= 2:
                break
    return charges or None


def parse_second_order(lines):
    start = None
    for i, line in enumerate(lines):
        if "SECOND ORDER PERTURBATION THEORY ANALYSIS" in line.upper():
            start = i
            break
    if start is None:
        return None
    row_re = re.compile(
        r'^\s*\d+\.\s+(.*?)\s*/\s*(.*?)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$'
    )
    lead_num_re = re.compile(r'^\d+\.\s*')
    rows = []
    for line in lines[start + 1:]:
        m = row_re.match(line)
        if m:
            rows.append({
                "donor": m.group(1).strip(),
                "acceptor": lead_num_re.sub('', m.group(2).strip()),
                "e2_kcal": float(m.group(3)),
                "e_diff_au": float(m.group(4)),
                "fij_au": float(m.group(5)),
            })
    rows.sort(key=lambda r: r["e2_kcal"], reverse=True)
    return rows or None


def parse_gaussian_log(file_content):
    lines = file_content.splitlines()

    results = {
        "energy": "N/A",
        "homo": "N/A",
        "lumo": "N/A",
        "coordinates": [],
        "parameters": [],
    }

    for line in reversed(lines):
        if "SCF Done:" in line:
            results["energy"] = line.split()[4]
            break

    hl = parse_homo_lumo(lines)
    results["unrestricted"] = hl["unrestricted"]
    for key in ("homo_alpha", "lumo_alpha", "homo_beta", "lumo_beta"):
        if key in hl:
            results[key] = hl[key]
    results["homo"] = f"{hl['homo_alpha']:.5f}" if "homo_alpha" in hl else "N/A"
    results["lumo"] = f"{hl['lumo_alpha']:.5f}" if "lumo_alpha" in hl else "N/A"
    if "homo_alpha" in hl and "lumo_alpha" in hl:
        gap_au = hl["lumo_alpha"] - hl["homo_alpha"]
        results["gap_alpha_au"] = gap_au
        results["gap_alpha_ev"] = gap_au * HARTREE_TO_EV
    if "homo_beta" in hl and "lumo_beta" in hl:
        gap_au = hl["lumo_beta"] - hl["homo_beta"]
        results["gap_beta_au"] = gap_au
        results["gap_beta_ev"] = gap_au * HARTREE_TO_EV

    coord_start = -1
    for i in range(len(lines) - 1, -1, -1):
        if "Standard orientation:" in lines[i] or "Input orientation:" in lines[i]:
            coord_start = i + 5
            break

    if coord_start != -1:
        for j in range(coord_start, len(lines)):
            if "---" in lines[j]:
                break
            results["coordinates"].append(lines[j].strip())

    param_start = -1
    for i in range(len(lines) - 1, -1, -1):
        if "!   Optimized Parameters   !" in lines[i]:
            param_start = i + 5
            break

    if param_start != -1:
        for j in range(param_start, len(lines)):
            if "---" in lines[j]:
                break
            results["parameters"].append(lines[j].strip())

    route_method = parse_route_and_method(lines)
    results["route"] = route_method["route"]
    results["functional"] = route_method["functional"]
    results["restriction"] = route_method["restriction"]
    results["basis"] = route_method["basis"]

    results["natural_charges"] = parse_natural_charges(lines)
    results["second_order"] = parse_second_order(lines)

    num_atoms = 0
    for line in results["coordinates"]:
        if len(line.split()) >= 6:
            num_atoms += 1

    results["mo_alpha"] = parse_mo_coefficient_weights(lines, num_atoms, "Alpha ") if num_atoms else None
    results["mo_beta"] = (
        parse_mo_coefficient_weights(lines, num_atoms, "Beta ")
        if num_atoms and results["unrestricted"] else None
    )

    return results


def convert_to_xyz(gaussian_coords):
    """Returns (xyz_string, atom_center_numbers) - the second list gives the
    Gaussian 'Center Number' for each line actually written, in order, so
    per-atom data (e.g. MO weights, keyed by Center Number) can be lined up
    with the atoms as 3Dmol.js will see them."""
    valid_rows = []
    for line in gaussian_coords:
        parts = line.split()
        if len(parts) >= 6:
            valid_rows.append(parts)

    xyz_str = f"{len(valid_rows)}\nGenerated by Streamlit Parser\n"
    centers = []
    for parts in valid_rows:
        atomic_num = int(parts[1])
        symbol = ATOMIC_SYMBOLS.get(atomic_num, "X")
        x, y, z = parts[3], parts[4], parts[5]
        xyz_str += f"{symbol} {x} {y} {z}\n"
        centers.append(int(parts[0]))

    return xyz_str, centers


def weights_in_xyz_order(weights, centers):
    if not weights:
        return None
    try:
        return [weights[c - 1] for c in centers]
    except IndexError:
        return None


def generate_text_report(results):
    report = "--- GAUSSIAN LOG PARSER REPORT ---\n\n"

    if results.get("functional"):
        method_line = results["functional"]
        if results.get("restriction"):
            method_line = f"{results['restriction']}-{method_line}"
        if results.get("basis"):
            method_line += f" / {results['basis']}"
        report += f"Method: {method_line}\n"
    if results.get("route"):
        report += f"Route section: {results['route']}\n"
    report += "\n"

    report += f"Final Energy: {results['energy']} Hartree\n"
    if results.get("unrestricted"):
        report += f"HOMO (alpha): {results.get('homo', 'N/A')} a.u.\n"
        report += f"LUMO (alpha): {results.get('lumo', 'N/A')} a.u.\n"
        if "homo_beta" in results:
            report += f"HOMO (beta):  {results['homo_beta']:.5f} a.u.\n"
        if "lumo_beta" in results:
            report += f"LUMO (beta):  {results['lumo_beta']:.5f} a.u.\n"
    else:
        report += f"HOMO Energy:  {results.get('homo', 'N/A')} a.u.\n"
        report += f"LUMO Energy:  {results.get('lumo', 'N/A')} a.u.\n"
    if "gap_alpha_au" in results:
        report += f"HOMO-LUMO Gap: {results['gap_alpha_au']:.5f} a.u. ({results['gap_alpha_ev']:.3f} eV)\n"
    report += "\n"

    report += "--- FINAL COORDINATES ---\n"
    report += "Center  Atomic  Atomic  Coordinates (Angstroms)\n"
    report += "Number  Number  Type    X           Y           Z\n"
    report += "-" * 65 + "\n"
    for c in results['coordinates']:
        report += f"{c}\n"

    report += "\n--- OPTIMIZED PARAMETERS ---\n"
    for p in results['parameters']:
        report += f"{p}\n"

    if results.get("natural_charges"):
        report += "\n--- NBO NATURAL CHARGES ---\n"
        for row in results["natural_charges"]:
            report += f"{row['index']:>4} {row['symbol']:<2}  {row['charge']:>10.5f}\n"

    if results.get("second_order"):
        report += "\n--- NBO SECOND-ORDER PERTURBATION (E(2), donor -> acceptor) ---\n"
        for row in results["second_order"]:
            report += (f"{row['donor']:<32} -> {row['acceptor']:<32}  "
                        f"E(2)={row['e2_kcal']:>7.2f} kcal/mol\n")

    return report


# =====================================================================
# Interactive 3D viewer (hover-linked HOMO/LUMO gradient)
# =====================================================================

VIEWER_TEMPLATE = r"""
<div id="gp-root">
  <style>
    #gp-root { font-family: 'IBM Plex Sans', -apple-system, sans-serif; }
    #gp-cards {
      display: flex; flex-wrap: wrap; gap: 0;
      border: 1px solid #E6E8EC; border-radius: 10px; overflow: hidden;
      background: #FFFFFF; margin-bottom: 14px;
    }
    .gp-card {
      flex: 1 1 130px; padding: 14px 16px; border-right: 1px solid #E6E8EC;
      cursor: default; transition: background-color .15s ease;
    }
    .gp-card:last-child { border-right: none; }
    .gp-card[data-accent]:hover { background: #F9FAFC; cursor: pointer; }
    .gp-card-label {
      font-size: 12.5px; color: #6B7280; margin-bottom: 4px; letter-spacing: .01em;
    }
    .gp-card-value {
      font-family: 'IBM Plex Mono', ui-monospace, monospace;
      font-size: 17px; color: #14171F; font-weight: 500;
    }
    .gp-card-unit { font-size: 12px; color: #9AA0AC; margin-left: 3px; }
    #gp-viewer { width: 100%; height: 420px; border-radius: 10px; background: #FFFFFF;
                 border: 1px solid #E6E8EC; position: relative; }
    #gp-caption {
      font-size: 12.5px; color: #6B7280; margin-top: 8px; min-height: 16px;
    }
    #gp-caption b { color: #14171F; font-weight: 500; }
  </style>

  <div id="gp-cards">__CARDS_HTML__</div>
  <div id="gp-viewer"></div>
  <div id="gp-caption">Hover a HOMO or LUMO value above to highlight its relative orbital character on the structure.</div>
</div>

<script src="https://3Dmol.org/build/3Dmol-min.js"></script>
<script>
(function () {
  const xyz = __XYZ_JSON__;
  const weights = __WEIGHTS_JSON__;

  const defaultStyle = {
    stick: { radius: 0.15, colorscheme: 'Jmol' },
    sphere: { scale: 0.25, colorscheme: 'Jmol' }
  };
  const PALE = [237, 238, 242];

  function hexToRgb(hex) {
    const h = hex.replace('#', '');
    return [parseInt(h.substring(0, 2), 16), parseInt(h.substring(2, 4), 16), parseInt(h.substring(4, 6), 16)];
  }
  function rgbToHex(rgb) {
    return '#' + rgb.map(v => Math.round(Math.max(0, Math.min(255, v))).toString(16).padStart(2, '0')).join('');
  }
  function blend(rgbA, rgbB, t) {
    return rgbToHex(rgbA.map((v, i) => v + (rgbB[i] - v) * t));
  }

  let viewer;
  function init() {
    viewer = $3Dmol.createViewer(document.getElementById('gp-viewer'), { backgroundColor: 'white' });
    viewer.addModel(xyz, 'xyz');
    viewer.setStyle({}, defaultStyle);
    viewer.zoomTo();
    viewer.render();
  }

  function applyDefault() {
    viewer.setStyle({}, defaultStyle);
    document.getElementById('gp-caption').innerHTML =
      'Hover a HOMO or LUMO value above to highlight its relative orbital character on the structure.';
    viewer.render();
  }

  function applyGradient(kind, accentHex, label) {
    const w = weights[kind];
    const accentRgb = hexToRgb(accentHex);
    if (w) {
      const maxW = Math.max.apply(null, w) || 1;
      viewer.setStyle({}, {
        stick: { radius: 0.13, colorscheme: 'Jmol', opacity: 0.45 },
        sphere: {
          scale: 0.30,
          colorfunc: function (atom) {
            const t = Math.max(0, Math.min(1, (w[atom.index] || 0) / maxW));
            return blend(PALE, accentRgb, Math.pow(t, 0.65));
          }
        }
      });
      document.getElementById('gp-caption').innerHTML =
        '<b>' + label + '</b> \u2014 sphere colour intensity \u2248 relative AO contribution weight (magnitude only, not orbital phase).';
    } else {
      viewer.setStyle({}, {
        stick: { radius: 0.13, colorscheme: 'Jmol', opacity: 0.35 },
        sphere: { scale: 0.27, color: accentHex, opacity: 0.55 }
      });
      document.getElementById('gp-caption').innerHTML =
        '<b>' + label + '</b> \u2014 per-atom weighting unavailable in this file (add <code>pop=full</code> to the route section for atom-resolved character).';
    }
    viewer.render();
  }

  function wireCards() {
    document.querySelectorAll('.gp-card').forEach(function (card) {
      const kind = card.getAttribute('data-kind');
      const accent = card.getAttribute('data-accent');
      const label = card.getAttribute('data-label');
      if (!kind || !accent) return;
      card.addEventListener('mouseenter', function () { applyGradient(kind, accent, label); });
      card.addEventListener('mouseleave', applyDefault);
    });
  }

  init();
  wireCards();
})();
</script>
"""


def _card_html(label, value, unit, kind=None, accent=None):
    attrs = ""
    if kind and accent:
        attrs = f' data-kind="{kind}" data-accent="{accent}" data-label="{label}"'
    unit_html = f'<span class="gp-card-unit">{unit}</span>' if unit else ""
    return (
        f'<div class="gp-card"{attrs}>'
        f'<div class="gp-card-label">{label}</div>'
        f'<div class="gp-card-value">{value}{unit_html}</div>'
        f'</div>'
    )


def render_interactive_viewer(results):
    xyz_data, centers = convert_to_xyz(results["coordinates"])
    if not centers:
        return

    ACCENT_HOMO = "#C2703D"
    ACCENT_LUMO = "#2E7D9A"

    mo_alpha = results.get("mo_alpha")
    mo_beta = results.get("mo_beta")

    weights = {
        "homo_alpha": weights_in_xyz_order(mo_alpha["homo_weights"], centers) if mo_alpha else None,
        "lumo_alpha": weights_in_xyz_order(mo_alpha["lumo_weights"], centers) if mo_alpha else None,
        "homo_beta": weights_in_xyz_order(mo_beta["homo_weights"], centers) if mo_beta else None,
        "lumo_beta": weights_in_xyz_order(mo_beta["lumo_weights"], centers) if mo_beta else None,
    }

    cards = [_card_html("SCF energy", results["energy"], "Ha")]

    unrestricted = results.get("unrestricted")
    homo_label = "HOMO (\u03b1)" if unrestricted else "HOMO"
    lumo_label = "LUMO (\u03b1)" if unrestricted else "LUMO"

    if "homo_alpha" in results:
        cards.append(_card_html(homo_label, f"{results['homo_alpha']:.5f}", "Ha", "homo_alpha", ACCENT_HOMO))
    if "lumo_alpha" in results:
        cards.append(_card_html(lumo_label, f"{results['lumo_alpha']:.5f}", "Ha", "lumo_alpha", ACCENT_LUMO))
    if "gap_alpha_ev" in results:
        cards.append(_card_html("Gap" + (" (\u03b1)" if unrestricted else ""),
                                 f"{results['gap_alpha_ev']:.2f}", "eV"))
    if unrestricted:
        if "homo_beta" in results:
            cards.append(_card_html("HOMO (\u03b2)", f"{results['homo_beta']:.5f}", "Ha", "homo_beta", ACCENT_HOMO))
        if "lumo_beta" in results:
            cards.append(_card_html("LUMO (\u03b2)", f"{results['lumo_beta']:.5f}", "Ha", "lumo_beta", ACCENT_LUMO))
        if "gap_beta_ev" in results:
            cards.append(_card_html("Gap (\u03b2)", f"{results['gap_beta_ev']:.2f}", "eV"))

    html = VIEWER_TEMPLATE
    html = html.replace("__CARDS_HTML__", "".join(cards))
    html = html.replace("__XYZ_JSON__", json.dumps(xyz_data))
    html = html.replace("__WEIGHTS_JSON__", json.dumps(weights))

    components.html(html, height=520, scrolling=False)


# =====================================================================
# Styling
# =====================================================================

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }

    .stApp { background-color: #FFFFFF; }
    .block-container { padding-top: 2.5rem; max-width: 880px; }

    h1, h2, h3 { color: #14171F; font-weight: 600; letter-spacing: -0.01em; }
    p, li, label { color: #14171F; }

    #gp-title { font-size: 28px; font-weight: 700; color: #14171F; margin-bottom: 2px; }
    #gp-subtitle { font-size: 14.5px; color: #6B7280; margin-bottom: 22px; }

    .gp-banner {
        border: 1px solid #E6E8EC; border-left: 3px solid #2A3EB1;
        background: #F6F7F9; border-radius: 8px;
        padding: 12px 16px; margin-bottom: 22px;
        font-size: 14px; color: #14171F;
    }
    .gp-banner b { color: #2A3EB1; }
    .gp-banner code {
        background: #EDEEF2; padding: 1px 6px; border-radius: 4px;
        font-family: 'IBM Plex Mono', monospace; font-size: 12.5px;
    }

    .gp-section-title {
        font-size: 15px; font-weight: 600; color: #14171F;
        margin: 28px 0 10px 0; padding-bottom: 8px; border-bottom: 1px solid #E6E8EC;
    }
    .gp-empty-note {
        font-size: 13.5px; color: #9AA0AC; padding: 10px 0;
    }

    [data-testid="stFileUploader"] {
        border: 1.5px dashed #C8CBD2; border-radius: 10px; background: #FAFBFC;
        padding: 6px;
    }

    [data-testid="stDataFrame"] { border: 1px solid #E6E8EC; border-radius: 8px; }

    .stDownloadButton button {
        background-color: #14171F; color: #FFFFFF; border: none;
        border-radius: 7px; font-weight: 500; padding: 0.5rem 1.1rem;
    }
    .stDownloadButton button:hover { background-color: #2A3EB1; color: #FFFFFF; }

    .gp-legend {
        display: flex; gap: 18px; flex-wrap: wrap; margin: 10px 0 4px 0;
        font-size: 13px; color: #14171F;
    }
    .gp-legend-item { display: flex; align-items: center; gap: 7px; }
    .gp-legend-dot { border-radius: 50%; border: 1px solid rgba(0,0,0,0.15); }
    </style>
    """, unsafe_allow_html=True)


# =====================================================================
# UI
# =====================================================================

st.set_page_config(page_title="Gaussian Output Parser", page_icon="\U0001F9EA", layout="centered")
inject_css()

st.markdown('<div id="gp-title">Gaussian Output Parser</div>', unsafe_allow_html=True)
st.markdown(
    '<div id="gp-subtitle">Upload a Gaussian output file to extract geometries, energies, '
    'molecular orbitals, and NBO analysis.</div>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader("Select .log or .out file", type=["log", "out"], label_visibility="collapsed")

if uploaded_file is not None:
    content = uploaded_file.getvalue().decode("utf-8", errors="replace")

    with st.spinner("Parsing data..."):
        results = parse_gaussian_log(content)

    # --- Method / route banner -------------------------------------------------
    if results.get("functional") or results.get("basis"):
        method_txt = results.get("functional") or "Unknown method"
        if results.get("restriction"):
            restriction_name = {"R": "restricted", "U": "unrestricted", "RO": "restricted open-shell"}
            method_txt = f"{method_txt} <span style='color:#6B7280'>({restriction_name.get(results['restriction'], results['restriction'])})</span>"
        basis_txt = f" &nbsp;/&nbsp; <b>{results['basis']}</b>" if results.get("basis") else ""
        st.markdown(
            f'<div class="gp-banner"><b>{method_txt}</b>{basis_txt}</div>',
            unsafe_allow_html=True,
        )
        if results.get("route"):
            with st.expander("Full route section"):
                st.code(results["route"], language=None)
    else:
        st.markdown(
            '<div class="gp-banner">Method / basis not detected in this file.</div>',
            unsafe_allow_html=True,
        )

    # --- Interactive overview + structure ---------------------------------------
    if results["coordinates"]:
        st.markdown('<div class="gp-section-title">Structure & orbital energies</div>', unsafe_allow_html=True)

        unique_atoms = set()
        for line in results["coordinates"]:
            parts = line.split()
            if len(parts) >= 6:
                unique_atoms.add(ATOMIC_SYMBOLS.get(int(parts[1]), "X"))

        legend_html = '<div class="gp-legend">'
        for atom in sorted(unique_atoms):
            color = JMOL_COLORS.get(atom, "#FF1493")
            size = LEGEND_SIZES.get(atom, 16)
            legend_html += (
                f'<div class="gp-legend-item">'
                f'<div class="gp-legend-dot" style="width:{size}px;height:{size}px;background-color:{color};"></div>'
                f'{atom}</div>'
            )
        legend_html += '</div>'
        st.markdown(legend_html, unsafe_allow_html=True)

        render_interactive_viewer(results)
    else:
        st.markdown('<div class="gp-section-title">Structure</div>', unsafe_allow_html=True)
        st.markdown('<div class="gp-empty-note">No coordinate block found in this file.</div>', unsafe_allow_html=True)

    # --- NBO ---------------------------------------------------------------
    st.markdown('<div class="gp-section-title">NBO \u2014 natural charges</div>', unsafe_allow_html=True)
    if results.get("natural_charges"):
        df_charges = pd.DataFrame(results["natural_charges"])
        df_charges = df_charges.rename(columns={"index": "Center", "symbol": "Atom", "charge": "Natural charge"})
        st.dataframe(df_charges, use_container_width=True, hide_index=True)
    else:
        st.markdown(
            '<div class="gp-empty-note">No NBO natural population analysis found. '
            'Add <code>pop=nbo</code> (or <code>pop=(nbo,full)</code>) to the route section to include it.</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="gp-section-title">NBO \u2014 second-order perturbation (donor \u2192 acceptor)</div>', unsafe_allow_html=True)
    if results.get("second_order"):
        df_so = pd.DataFrame(results["second_order"])
        df_so = df_so.rename(columns={
            "donor": "Donor NBO", "acceptor": "Acceptor NBO",
            "e2_kcal": "E(2) kcal/mol", "e_diff_au": "E(j)-E(i) a.u.", "fij_au": "F(i,j) a.u.",
        })
        st.dataframe(df_so, use_container_width=True, hide_index=True)
        st.caption("Sorted by E(2) descending. Format can vary slightly by Gaussian/NBO version \u2014 "
                   "if rows look missing or malformed, this parser may need a small adjustment for your version.")
    else:
        st.markdown(
            '<div class="gp-empty-note">No second-order perturbation table found (needs '
            '<code>pop=nbo</code> in the route section).</div>',
            unsafe_allow_html=True,
        )

    # --- Optimized parameters ------------------------------------------------
    if results["parameters"]:
        st.markdown('<div class="gp-section-title">Optimized parameters</div>', unsafe_allow_html=True)
        with st.expander(f"{len(results['parameters'])} parameters", expanded=False):
            st.code("\n".join(results["parameters"]), language=None)

    # --- Download --------------------------------------------------------------
    st.markdown('<div class="gp-section-title">Export</div>', unsafe_allow_html=True)
    report_text = generate_text_report(results)
    st.download_button(
        label="Download parsed data",
        data=report_text,
        file_name=f"{uploaded_file.name}_parsed.txt",
        mime="text/plain",
    )
