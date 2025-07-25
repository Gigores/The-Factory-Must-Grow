import pygame as pg
from rdkit import Chem
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
import math

smile = str


def adjust_brightness(color: str, brightness_factor: float) -> tuple:

    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)

    r = min(255, max(0, int(r * brightness_factor)))
    g = min(255, max(0, int(g * brightness_factor)))
    b = min(255, max(0, int(b * brightness_factor)))

    return int(r), int(g), int(b)


class MoleculeRenderer:

    def __init__(self):

        self.cashed_textures = dict()

    def render_molecule_diagram(self, smiles: smile, atom_colors: dict, res_x=96, res_y=96, width=400, height=400, atom_radius=6, bond_width=4, scale_factor=1.0, offset_x=0, offset_y=0):

        if smiles in self.cashed_textures:
            return self.cashed_textures[smiles]

        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"Invalid molecule formula: {smiles}")

        mol = Chem.AddHs(mol)
        rdDepictor.Compute2DCoords(mol)

        conf = mol.GetConformer()
        atom_positions = [conf.GetAtomPosition(i) for i in range(mol.GetNumAtoms())]
        bonds = [(bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()) for bond in mol.GetBonds()]
        atom_types = [atom.GetSymbol() for atom in mol.GetAtoms()]

        x_coords = [pos.x for pos in atom_positions]
        y_coords = [pos.y for pos in atom_positions]

        mean_x = sum(x_coords) / len(x_coords)
        mean_y = sum(y_coords) / len(y_coords)

        margin = 20
        max_x, min_x = max(x_coords), min(x_coords)
        max_y, min_y = max(y_coords), min(y_coords)

        scale_x = (res_x - 2 * margin) / (max_x - min_x) if max_x > min_x else 1
        scale_y = (res_y - 2 * margin) / (max_y - min_y) if max_y > min_y else 1
        scale = min(scale_x, scale_y) * scale_factor

        def transform(pos):
            x = int((pos.x - mean_x) * scale + res_x / 2 + offset_x)
            y = int((res_y / 2) - (pos.y - mean_y) * scale + offset_y)
            return x, y

        surface = pg.Surface((res_x, res_y))
        surface.fill((0, 255, 0, 0))
        surface.set_colorkey((0, 255, 0, 0))

        for start_idx, end_idx in bonds :
            start_pos = transform(atom_positions[start_idx])
            end_pos = transform(atom_positions[end_idx])
            pg.draw.line(surface, "#bbbbbb", start_pos, end_pos, bond_width)
            pg.draw.line(surface, "#ffffff", start_pos, end_pos, bond_width // 2)

        for idx, atom in enumerate(atom_types):
            pos = transform(atom_positions[idx])
            shine_pos_x = pos[0] - atom_radius // 4
            shine_pos_y = pos[1] - atom_radius // 4
            color = atom_colors.get(atom, "#ffffff")
            pg.draw.circle(surface, color, pos, atom_radius)
            pg.draw.circle(surface, adjust_brightness(color, 0.75), pos, atom_radius, 1)
            pg.draw.circle(surface, adjust_brightness(color, 1.5), (shine_pos_x, shine_pos_y), atom_radius // 3)

        return pg.transform.scale(surface, (width, height))
