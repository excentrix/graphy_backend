import traceback
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import numpy as np
import pandas as pd


def manipulate_data(df_dict, filter_column=None, filter_value=None, columns=None):
    try:
        df = pd.DataFrame(df_dict)

        # Log data types of each column for debugging purposes
        print("Data Types Before Manipulation:")
        print(df.dtypes)

        # Apply filtering if specified
        if filter_column and filter_value:
            if filter_column not in df.columns:
                raise KeyError(f"Column '{filter_column}' does not exist in the dataset.")
            df = df[df[filter_column] == filter_value]

        # Select specific columns if specified
        if columns:
            column_list = columns.split(',')
            missing_columns = [col for col in column_list if col not in df.columns]
            if missing_columns:
                raise KeyError(f"The following columns are missing from the dataset: {', '.join(missing_columns)}")
            df = df[column_list]

        # Return manipulated data preview
        response = {
            "columns": df.columns.tolist(),
            "preview": df.head(5).replace({np.nan: None}).to_dict(orient="records")
        }
        return jsonable_encoder(response)
    except KeyError as ke:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Key error: {str(ke)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An error occurred during data manipulation: {str(e)}")