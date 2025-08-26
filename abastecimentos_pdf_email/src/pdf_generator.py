from fpdf import FPDF
from jinja2 import Environment, FileSystemLoader
import os

def generate_pdf(data, output_path):
    # Create a PDF document
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set font
    pdf.set_font("Arial", size=12)

    # Add content to the PDF
    pdf.cell(200, 10, txt="Relatório de Abastecimento", ln=True, align='C')
    pdf.ln(10)

    # Add form data to the PDF
    for key, value in data.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)

    # Save the PDF to the specified output path
    pdf.output(output_path)

def render_pdf_template(data):
    # Load the HTML template for the PDF
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
    template = env.get_template('pdf_template.html')
    
    # Render the template with the provided data
    return template.render(data)

def save_pdf_from_template(data, output_path):
    html_content = render_pdf_template(data)
    
    # Convert HTML to PDF (using a library like pdfkit or similar)
    # This part is a placeholder; you would need to implement the conversion
    # pdfkit.from_string(html_content, output_path)  # Uncomment when pdfkit is set up

    # For now, just create a simple PDF with the data
    generate_pdf(data, output_path)  # Fallback to simple PDF generation
