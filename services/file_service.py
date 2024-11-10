import os
from fastapi import HTTPException
import pandas as pd
from openpyxl import load_workbook
import traceback
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import numpy as np

UPLOAD_FOLDER = "uploads"

# Ensure the uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

async def save_file(file):
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return file_location

def parse_file(file_location, content_type):
    try:
        # Read the uploaded file into a DataFrame
        if content_type == "text/csv":
            df = pd.read_csv(file_location)
        elif content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(file_location, engine="openpyxl")
        else:
            df = pd.read_excel(file_location)

        # Convert any non-serializable data (e.g., Timestamps, NaN, inf) to string or replace them
        df = df.map(lambda x: str(x) if isinstance(x, (datetime, pd.Timestamp)) else (None if isinstance(x, float) and not np.isfinite(x) else x))

        # Return basic information about the DataFrame
        response = {
            "filename": os.path.basename(file_location),
            "columns": df.columns.tolist(),
            "preview": df.head(5).replace({np.nan: None}).to_dict(orient="records"),
            'dataframe': df.to_dict(orient="records")
            # 'dataframe': df.to_dict(orient="records")
        }
        return jsonable_encoder(response)
    except ValueError as ve:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Value error: {str(ve)}")
    except pd.errors.EmptyDataError:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="The file is empty or does not contain any data.")
    except FileNotFoundError:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="The file was not found.")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred while processing the file: {str(e)}")
