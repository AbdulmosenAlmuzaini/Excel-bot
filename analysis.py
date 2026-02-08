import pandas as pd
import os
from logger import log_error

def analyze_excel(file_path):
    try:
        # Check extension
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.csv':
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        # Basic Info
        summary = {
            "rows": len(df),
            "cols": len(df.columns),
            "headers": list(df.columns),
            "stats": df.describe(include='all').to_dict(),
            "sample": df.head(5).to_dict(orient='records')
        }

        # Simple Forecasting (if there are numeric columns)
        numeric_cols = df.select_dtypes(include=['number']).columns
        forecasting = {}
        if not numeric_cols.empty:
            for col in numeric_cols:
                # Basic trend check
                if len(df) > 1:
                    change = df[col].iloc[-1] - df[col].iloc[0]
                    trend = "Increasing" if change > 0 else "Decreasing" if change < 0 else "Stable"
                    forecasting[col] = f"Trend: {trend}. Total change: {change:.2f}"

        # Combine for AI prompt
        analysis_text = f"File Analysis Summary:\n- Rows: {summary['rows']}, Columns: {summary['cols']}\n- Headers: {', '.join(summary['headers'])}\n"
        if forecasting:
            analysis_text += "- Forecasting Insights:\n"
            for col, insight in forecasting.items():
                analysis_text += f"  * {col}: {insight}\n"
        
        analysis_text += "\nData Sample (Top 5 Rows):\n"
        analysis_text += str(df.head(5))

        return analysis_text
    except Exception as e:
        log_error(f"Analysis Error: {e}")
        return f"Error analyzing file: {e}"

def is_valid_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    return ext in ['.xlsx', '.xls', '.csv']
