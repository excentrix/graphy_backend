import traceback
from typing import Dict

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import pandas as pd


def generate_insights(df_dict: Dict) -> Dict:
    try:
        df = pd.DataFrame(df_dict)

        # Generate basic insights
        insights = {}
        
        # 1. Summary Statistics
        insights["summary_statistics"] = df.describe().to_dict()

        # 2. Count of Missing Values per Column
        insights["missing_values"] = df.isnull().sum().to_dict()

        # 3. Data Types
        insights["data_types"] = df.dtypes.astype(str).to_dict()

        # 4. Correlation Matrix (for numeric columns)
        numeric_cols = df.select_dtypes(include=["number"])
        if not numeric_cols.empty:
            insights["correlation_matrix"] = numeric_cols.corr().to_dict()

        # More insights can be added as needed

        return jsonable_encoder(insights)

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An error occurred while generating insights: {str(e)}")