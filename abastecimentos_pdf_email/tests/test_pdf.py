import pytest
from src.pdf_generator import generate_pdf

def test_generate_pdf():
    # Dados de teste
    data = {
        "placa": "ABC1234",
        "justificativa": "Abastecimento regular",
        "supervisor": "João Silva",
        "setor": "Logística",
        "quantidade_litros": 50,
        "tipo_combustivel": "Gasolina"
    }
    
    # Gera o PDF
    pdf_path = generate_pdf(data)
    
    # Verifica se o PDF foi gerado
    assert pdf_path is not None
    assert pdf_path.endswith('.pdf')
    
    # Verifica se o arquivo PDF existe
    import os
    assert os.path.exists(pdf_path)
    
    # Limpeza: remove o PDF gerado após o teste
    os.remove(pdf_path)