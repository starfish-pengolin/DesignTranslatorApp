import FreeCAD
import Part
import os

def import_blender_script(blender_script_path, output_fcstd_path="ImportedFromBlender.fcstd"):
    """
    Read Blender Python commands and reconstruct objects in FreeCAD.
    Supports basic cube, cylinder, sphere, cone primitives.
    """
    if not os.path.exists(blender_script_path):
        raise FileNotFoundError(f"Blender script not found: {blender_script_path}")

    doc = FreeCAD.newDocument("BlenderImport")

    with open(blender_script_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if "primitive_cube_add" in line:
            import re
            loc_match = re.search(r'location=\(([^)]+)\)', line)
            scale_match = re.search(r'scale=\(([^)]+)\)', line)
            loc = [float(x) for x in loc_match.group(1).split(',')] if loc_match else [0,0,0]
            box = doc.addObject("Part::Box", "Cube")
            box.Length = box.Width = box.Height = 1
            box.Placement.Base = FreeCAD.Vector(*loc)
            if scale_match:
                scale = [float(x) for x in scale_match.group(1).split(',')]
                box.Length = scale[0]*2
                box.Width  = scale[1]*2
                box.Height = scale[2]*2

        elif "primitive_cylinder_add" in line:
            import re
            r_match = re.search(r'radius=([0-9.]+)', line)
            d_match = re.search(r'depth=([0-9.]+)', line)
            loc_match = re.search(r'location=\(([^)]+)\)', line)
            radius = float(r_match.group(1)) if r_match else 1
            depth = float(d_match.group(1)) if d_match else 1
            loc = [float(x) for x in loc_match.group(1).split(',')] if loc_match else [0,0,0]
            cyl = doc.addObject("Part::Cylinder", "Cylinder")
            cyl.Radius = radius
            cyl.Height = depth
            cyl.Placement.Base = FreeCAD.Vector(*loc)

        elif "primitive_uv_sphere_add" in line:
            import re
            r_match = re.search(r'radius=([0-9.]+)', line)
            loc_match = re.search(r'location=\(([^)]+)\)', line)
            radius = float(r_match.group(1)) if r_match else 1
            loc = [float(x) for x in loc_match.group(1).split(',')] if loc_match else [0,0,0]
            sph = doc.addObject("Part::Sphere", "Sphere")
            sph.Radius = radius
            sph.Placement.Base = FreeCAD.Vector(*loc)

        elif "primitive_cone_add" in line:
            import re
            r1_match = re.search(r'radius1=([0-9.]+)', line)
            r2_match = re.search(r'radius2=([0-9.]+)', line)
            d_match = re.search(r'depth=([0-9.]+)', line)
            loc_match = re.search(r'location=\(([^)]+)\)', line)
            radius1 = float(r1_match.group(1)) if r1_match else 1
            radius2 = float(r2_match.group(1)) if r2_match else 0
            depth = float(d_match.group(1)) if d_match else 1
            loc = [float(x) for x in loc_match.group(1).split(',')] if loc_match else [0,0,0]
            cone = doc.addObject("Part::Cone", "Cone")
            cone.Radius1 = radius1
            cone.Radius2 = radius2
            cone.Height = depth
            cone.Placement.Base = FreeCAD.Vector(*loc)

    doc.saveAs(output_fcstd_path)
    print(f"Imported Blender script saved as FreeCAD file: {output_fcstd_path}")
    return output_fcstd_path
