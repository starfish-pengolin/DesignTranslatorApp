#!/usr/bin/env python3
import os
import sys

# Ensure project root is on sys.path so `import core` works when uvicorn imports this module.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Runtime check for python-multipart (FastAPI needs this for UploadFile/Form)
try:
    import multipart  # type: ignore
except Exception:
    raise RuntimeError(
        "Missing dependency: python-multipart. Install with: pip install python-multipart"
    )

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import shutil
import uuid

# Import your core functions (should succeed now that ROOT is on sys.path)
from core.blender_export import export_highpoly
from core.blender_script_export import generate_blender_script

app = FastAPI(title="DesignTranslator API")

ROOT_PATH = Path(__file__).resolve().parents[1]
TMP_DIR = ROOT_PATH / "tmp"
STATIC_DIR = ROOT_PATH / "frontend_dist"

TMP_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="frontend")


@app.post("/api/export")
async def export_endpoint(file: UploadFile = File(...), name: str = Form(default="export")):
    uid = uuid.uuid4().hex
    workdir = TMP_DIR / uid
    workdir.mkdir(parents=True, exist_ok=True)
    input_path = workdir / file.filename
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    try:
        out = export_highpoly(str(input_path), str(workdir), name=name)
        return FileResponse(
            str(out), media_type="application/octet-stream", filename=os.path.basename(out)
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/api/generate_script")
async def script_endpoint(file: UploadFile = File(...), name: str = Form(default="import_script")):
    uid = uuid.uuid4().hex
    workdir = TMP_DIR / uid
    workdir.mkdir(parents=True, exist_ok=True)
    input_path = workdir / file.filename
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    try:
        stl_path = str(input_path)
        if input_path.suffix.lower() != ".stl":
            stl_path = export_highpoly(str(input_path), str(workdir), name=f"{name}_for_blender")
        script = generate_blender_script(stl_path, str(workdir), name=name)
        return FileResponse(script, media_type="text/x-python", filename=os.path.basename(script))
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
