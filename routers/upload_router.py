# routers/upload_router.py
from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from backend.services.data_insights import generate_insights
from backend.services.file_service import save_file, parse_file 
from backend.services.data_manipulation import manipulate_data
import os
import traceback

router = APIRouter()

uploaded_data_cache = {}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in [
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "text/csv"
    ]:
        raise HTTPException(status_code=400, detail="Invalid file format. Only CSV or Excel files are allowed.")

    try:
        # Save the uploaded file
        file_location = await save_file(file)

        # Parse the uploaded file
        response = parse_file(file_location, file.content_type)

        # Cache the DataFrame for manipulation
        uploaded_data_cache[file.filename] = response["dataframe"]

        return JSONResponse(content=response)

    except Exception as e:
        # Log the complete traceback for debugging purposes
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing the file: {str(e)}")

    finally:
        # Clean up: Remove the uploaded file
        if 'file_location' in locals() and os.path.exists(file_location):
            os.remove(file_location)

@router.get("/manipulate")
async def manipulate_data_route(
    filename: str = Query(..., description="The filename of the uploaded data to manipulate"),
    filter_column: str = Query(None, description="The column to apply a filter on"),
    filter_value: str = Query(None, description="The value to filter the column by"),
    columns: str = Query(None, description="Comma-separated list of columns to select")
):
    # Normalize filename for consistent lookup
    normalized_filename = filename.lower().replace(" ", "_")

    if normalized_filename not in uploaded_data_cache:
        raise HTTPException(status_code=404, detail="File not found. Please upload the file first.")

    try:
        # Manipulate the cached DataFrame
        dataframe = uploaded_data_cache[normalized_filename]
        response = manipulate_data(dataframe, filter_column, filter_value, columns)

        return JSONResponse(content=response)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing the data manipulation: {str(e)}")
    
@router.get("/insights")
async def generate_insights_route(
    filename: str = Query(..., description="The filename of the uploaded data to generate insights for")
):
    # Normalize filename for consistent lookup
    normalized_filename = filename.lower().replace(" ", "_")

    if normalized_filename not in uploaded_data_cache:
        raise HTTPException(status_code=404, detail="File not found. Please upload the file first.")

    try:
        # Generate insights from the cached DataFrame
        dataframe = uploaded_data_cache[normalized_filename]
        response = generate_insights(dataframe)

        return JSONResponse(content=response)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")