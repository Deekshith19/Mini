import json
from fpdf import FPDF
import os

def add_section(pdf, title, content):
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, title, ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 10, content)
    pdf.ln()

def format_json_data(data):
    formatted_data = ""
    for key, value in data.items():
        if isinstance(value, list):
            formatted_data += f"{key}:\n"
            for item in value:
                formatted_data += f"  - {item}\n"
        else:
            formatted_data += f"{key}: {value}\n"
    return formatted_data

def generate_pdf_report(json_file1, json_file2, output_pdf):
    # Load JSON data
    with open(json_file1, 'r') as file1, open(json_file2, 'r') as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)

    # Create PDF
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, 'Crawling Information Report', ln=True, align="C")
    pdf.ln(10)

    # Section 1: Data from the first JSON
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, 'Data from First Crawl (main__crawled.json)', ln=True)
    pdf.ln(5)
    add_section(pdf, "Crawled Data", format_json_data(data1))

    # Section 2: Data from the second JSON
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, 'Data from Second Crawl (second_crawled.json)', ln=True)
    pdf.ln(5)
    add_section(pdf, "Crawled Data", format_json_data(data2))

    # Output the PDF
    pdf.output(output_pdf)
    print(f"PDF report generated: {output_pdf}")

if __name__ == "__main__":
    json_file1 = 'main__crawled.json'
    json_file2 = 'second_crawled.json'
    output_pdf = 'crawlinfo.pdf'

    # Check if the files exist before generating the report
    if os.path.exists(json_file1) and os.path.exists(json_file2):
        generate_pdf_report(json_file1, json_file2, output_pdf)
    else:
        print("One or both JSON files do not exist. Cannot generate report.")

