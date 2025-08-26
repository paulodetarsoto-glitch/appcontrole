from src.forms import AbastecimentoForm

def test_abastecimento_form_valid_data():
    form_data = {
        'placa': 'ABC1234',
        'justificativa': 'Abastecimento regular',
        'supervisor': 'João Silva',
        'setor': 'Logística',
        'quantidade_litros': 50,
        'tipo_combustivel': 'Gasolina'
    }
    form = AbastecimentoForm(data=form_data)
    assert form.validate() is True

def test_abastecimento_form_invalid_data():
    form_data = {
        'placa': '',
        'justificativa': 'Abastecimento regular',
        'supervisor': 'João Silva',
        'setor': 'Logística',
        'quantidade_litros': 50,
        'tipo_combustivel': 'Gasolina'
    }
    form = AbastecimentoForm(data=form_data)
    assert form.validate() is False
    assert 'This field is required.' in form.errors['placa']

def test_abastecimento_form_quantity_negative():
    form_data = {
        'placa': 'ABC1234',
        'justificativa': 'Abastecimento regular',
        'supervisor': 'João Silva',
        'setor': 'Logística',
        'quantidade_litros': -10,
        'tipo_combustivel': 'Gasolina'
    }
    form = AbastecimentoForm(data=form_data)
    assert form.validate() is False
    assert 'Must be greater than or equal to 0.' in form.errors['quantidade_litros']