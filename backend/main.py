# backend/main.py
from fastapi import FastAPI,UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import chardet

app = FastAPI()

# Allow frontend (Vite dev server) to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Your frontend dev port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Visualizer.ai Backend Running ✅"}

@app.post("/parse_csv")
async def parse_csv(file: UploadFile = File(...)):
    try:
        # Read the file bytes
        contents = await file.read()
        # Detect encoding
        result = chardet.detect(contents)
        encoding = result["encoding"] or "utf-8"

        # Load CSV file into a pandas DataFrame using detected encoding
        from io import BytesIO
        df = pd.read_csv(BytesIO(contents), encoding=encoding)

        # Prepare response
        response = {
            "status": "success",
            "columns": df.columns.tolist(),
            "num_rows": len(df),
            "preview": df.head(5).to_dict(orient="records"),
            "data": df.to_dict(orient="records"),  # Full dataset as list of dicts
        }

        return response

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }