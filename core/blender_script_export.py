import FreeCAD
from FreeCAD import Base
import os

def generate_blender_script(fcstd_path, output_dir, name="BlenderModel"):
    """
    Export FreeCAD objects as Blender Python commands.
    """
    if not os.path.exists(fcstd_path):
        raise FileNotFoundError(f"CAD file not found: {fcstd_path}")

    os.makedirs(output_dir, exist_ok=True)
    doc = FreeCAD.open(fcstd_path)
    script_path = os.path.join(output_dir, f"{name}.py")

    with open(script_path, "w") as f:
        f.write("import bpy\n\n")
        f.write("bpy.ops.object.select_all(action='SELECT')\n")
        f.write("bpy.ops.object.delete(use_global=False)\n\n")

        for obj in doc.Objects:
            if hasattr(obj, "Shape") and obj.Shape:
                shape_type = obj.Shape.ShapeType
                pos = obj.Shape.BoundBox.Center

                if shape_type == "Box":
                    dims = obj.Shape.BoundBox
                    f.write(f"bpy.ops.mesh.primitive_cube_add(size=1, location=({pos.x}, {pos.y}, {pos.z}))\n")
                    f.write(f"bpy.context.object.scale = ({dims.XLength/2}, {dims.YLength/2}, {dims.ZLength/2})\n")
                elif shape_type == "Cylinder":
                    cyl = obj.Shape
                    f.write(f"bpy.ops.mesh.primitive_cylinder_add(radius={cyl.Radius}, depth={cyl.Height}, location=({pos.x}, {pos.y}, {pos.z}))\n")
                elif shape_type == "Sphere":
                    sph = obj.Shape
                    f.write(f"bpy.ops.mesh.primitive_uv_sphere_add(radius={sph.Radius}, location=({pos.x}, {pos.y}, {pos.z}))\n")
                elif shape_type == "Cone":
                    cone = obj.Shape
                    f.write(f"bpy.ops.mesh.primitive_cone_add(radius1={cone.Radius1}, radius2={cone.Radius2}, depth={cone.Height}, location=({pos.x}, {pos.y}, {pos.z}))\n")
                else:
                    f.write(f"bpy.ops.mesh.primitive_cube_add(size=1, location=({pos.x}, {pos.y}, {pos.z}))\n")

    FreeCAD.closeDocument(doc.Name)
    print(f"B

