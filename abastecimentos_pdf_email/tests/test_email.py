import pytest
from src.emailer import send_email_with_attachment

def test_send_email_with_attachment(mocker):
    # Mock the SMTP server
    mock_smtp = mocker.patch('src.emailer.smtplib.SMTP')
    mock_instance = mock_smtp.return_value

    # Test data
    to_address = "test@posto.com"
    subject = "Teste de Abastecimento"
    body = "Por favor, veja o anexo."
    attachment_path = "path/to/abastecimento.pdf"

    # Call the function
    result = send_email_with_attachment(to_address, subject, body, attachment_path)

    # Assertions
    assert result is True
    mock_instance.send_message.assert_called_once()
    assert mock_instance.send_message.call_args[0][0]['To'] == to_address
    assert mock_instance.send_message.call_args[0][0]['Subject'] == subject
    assert mock_instance.send_message.call_args[0][0].get_content() == body

def test_send_email_without_attachment(mocker):
    # Mock the SMTP server
    mock_smtp = mocker.patch('src.emailer.smtplib.SMTP')
    mock_instance = mock_smtp.return_value

    # Test data
    to_address = "test@posto.com"
    subject = "Teste de Abastecimento"
    body = "Sem anexo desta vez."

    # Call the function
    result = send_email_with_attachment(to_address, subject, body)

    # Assertions
    assert result is True
    mock_instance.send_message.assert_called_once()
    assert mock_instance.send_message.call_args[0][0]['To'] == to_address
    assert mock_instance.send_message.call_args[0][0]['Subject'] == subject
    assert mock_instance.send_message.call_args[0][0].get_content() == body

def test_send_email_failure(mocker):
    # Mock the SMTP server to raise an exception
    mock_smtp = mocker.patch('src.emailer.smtplib.SMTP', side_effect=Exception("SMTP error"))
    
    # Test data
    to_address = "test@posto.com"
    subject = "Teste de Abastecimento"
    body = "Por favor, veja o anexo."
    attachment_path = "path/to/abastecimento.pdf"

    # Call the function and assert it raises an exception
    with pytest.raises(Exception):
        send_email_with_attachment(to_address, subject, body, attachment_path)