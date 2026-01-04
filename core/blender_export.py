import FreeCAD
import Part
import Mesh
import os

def export_highpoly(fcstd_path, output_dir, name="HighPolyModel"):
    """
    Export FreeCAD objects to STL for Blender.
    """
    if not os.path.exists(fcstd_path):
        raise FileNotFoundError(f"CAD file not found: {fcstd_path}")

    os.makedirs(output_dir, exist_ok=True)
    doc = FreeCAD.open(fcstd_path)
    stl_paths = []

    for obj in doc.Objects:
        if hasattr(obj, "Shape") and obj.Shape:
            stl_file = os.path.join(output_dir, f"{obj.Name}_{name}.stl")
            Mesh.export([obj], stl_file)
            stl_paths.append(stl_file)
            print(f"Exported {stl_file}")

    FreeCAD.closeDocument(doc.Name)
    return stl_paths
