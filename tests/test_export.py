import os
from core.blender_export import export_highpoly


def test_export_tmp(tmp_path):
    # create a tiny sphere using trimesh if available, otherwise skip
    import trimesh

    mesh = trimesh.creation.icosphere(subdivisions=1, radius=0.5)
    f = tmp_path / "sphere.stl"
    mesh.export(str(f))
    out = export_highpoly(str(f), str(tmp_path), name="out")
    assert os.path.exists(out)
