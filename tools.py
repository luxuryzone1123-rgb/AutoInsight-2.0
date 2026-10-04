import os
import pandas as pd
from crewai.tools import tool
from fpdf import FPDF

@tool("profile_csv_dataset")
def profile_csv_dataset(file_path: str) -> str:
    """Reads a CSV file and calculates key metrics, column stats, missing values, and numeric descriptions."""
    if not os.path.exists(file_path):
        return f"Error: Dataset file not found at path: {file_path}"
    
    try:
        df = pd.read_csv(file_path)
        num_rows, num_cols = df.shape
        missing_vals = df.isnull().sum().to_dict()
        data_types = df.dtypes.astype(str).to_dict()
        
        numeric_summary = ""
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            numeric_summary = numeric_df.describe().to_string()
        else:
            numeric_summary = "No numeric columns found for descriptive stats."

        output = f"""
=== CSV DATASET PROFILING SUMMARY ===
File Path: {file_path}
Total Rows: {num_rows}
Total Columns: {num_cols}

Column Data Types:
{data_types}

Missing Values Count:
{missing_vals}

Numeric Columns Descriptive Statistics:
{numeric_summary}
=====================================
"""
        return output
    except Exception as e:
        return f"Error profiling dataset: {str(e)}"


@tool("create_pdf_report")
def create_pdf_report(report_text: str) -> str:
    """Generates an executive PDF report file from a markdown or formatted text string."""
    try:
        os.makedirs("reports", exist_ok=True)
        pdf_path = os.path.join("reports", "AutoInsight_Executive_Report.pdf")

        class PDF(FPDF):
            def header(self):
                self.set_font('Helvetica', 'B', 14)
                self.cell(0, 10, 'AutoInsight AI - Executive Report', border=0, new_x="LMARGIN", new_y="NEXT", align='C')
                self.ln(5)

            def footer(self):
                self.set_y(-15)
                self.set_font('Helvetica', 'I', 8)
                self.cell(0, 10, f'Page {self.page_no()}', border=0, align='C')

        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Helvetica', size=11)

        # Clean text for FPDF latin-1 compatibility
        clean_text = report_text.encode('latin-1', 'replace').decode('latin-1')

        for line in clean_text.split('\n'):
            pdf.multi_cell(0, 8, txt=line)

        pdf.output(pdf_path)
        return f"PDF Report successfully created at: {pdf_path}"
    except Exception as e:
        return f"Failed to generate PDF report: {str(e)}"