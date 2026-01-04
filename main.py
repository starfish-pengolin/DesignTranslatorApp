from fastapi import FastAPI

app = FastAPI(title="Design Translator API")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "DesignTranslator API running"}

@app.post("/export/")
def export_endpoint(file_name: str):
    # Placeholder for your export logic
    return {"status": "success", "file": file_name}
