def normalize_text(text):
    """Normalize text by stripping whitespace and capitalizing."""
    if text:
        return text.strip().title()
    return text

def validate_liters(liters):
    """Validate that the quantity of liters is a positive number."""
    if liters <= 0:
        raise ValueError("Quantidade de litros deve ser maior que zero.")
    return liters

def format_email_subject(placa):
    """Format the email subject line."""
    return f"Requisição de Abastecimento - {placa}"

def format_pdf_filename(placa):
    """Generate a filename for the PDF based on the vehicle plate."""
    return f"abastecimento_{placa}.pdf"