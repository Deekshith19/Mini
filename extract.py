import json
from fpdf import FPDF

# Function to extract URLs and their associated sub-parameters
def extract_urls_from_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Check the type of data
    if isinstance(data, list):
        print("JSON Data (first 5 entries):", data[:5])  # Print first 5 entries if it's a list
    elif isinstance(data, dict):
        print("JSON Data (dictionary keys):", list(data.keys()))  # Print the keys if it's a dictionary
    else:
        print("Unexpected JSON structure:", type(data))
    
    extracted_data = []
    
    # Adjust logic based on the type of data
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):  # Ensure item is a dictionary
                url = item.get('url')
                http_method = item.get('http_method')
                status_code = item.get('status_code')
                cookies = item.get('cookies')
                headers = item.get('headers')
                
                # Add each extracted item to the list
                extracted_data.append({
                    'url': url,
                    'http_method': http_method,
                    'status_code': status_code,
                    'cookies': cookies,
                    'headers': headers
                })
            else:
                print("Unexpected format in list item: ", item)
    elif isinstance(data, dict):
        # Handle the case where the data is a dictionary
        url = data.get('url')
        http_method = data.get('http_method')
        status_code = data.get('status_code')
        cookies = data.get('cookies')
        headers = data.get('headers')
        
        extracted_data.append({
            'url': url,
            'http_method': http_method,
            'status_code': status_code,
            'cookies': cookies,
            'headers': headers
        })
    
    return extracted_data

# Function to generate PDF from extracted data
def generate_pdf(extracted_data, output_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Add a page to the PDF
    pdf.add_page()
    
    # Set title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Crawled URL Information", ln=True, align='C')
    
    # Set body font
    pdf.set_font('Arial', '', 12)
    
    # Loop through extracted data and add to the PDF
    for entry in extracted_data:
        pdf.ln(10)  # Add some space between entries
        pdf.cell(200, 10, txt=f"URL: {entry['url']}", ln=True)
        pdf.cell(200, 10, txt=f"HTTP Method: {entry['http_method']}", ln=True)
        pdf.cell(200, 10, txt=f"Status Code: {entry['status_code']}", ln=True)
        pdf.cell(200, 10, txt=f"Cookies: {entry['cookies']}", ln=True)
        pdf.cell(200, 10, txt=f"Headers: {entry['headers']}", ln=True)
    
    # Output the PDF to a file
    pdf.output(output_pdf)

def main():
    # Path to the JSON file
    json_file = 'main__crawled.json'  # Replace with your JSON file path
    
    # Extract URL and sub-parameter data
    extracted_data = extract_urls_from_json(json_file)
    
    # Generate PDF with extracted data
    output_pdf = 'crawled_urls_report.pdf'  # Output PDF file name
    generate_pdf(extracted_data, output_pdf)
    
    print(f"PDF report generated: {output_pdf}")

if __name__ == "__main__":
    main()

