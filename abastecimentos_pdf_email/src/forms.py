from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class AbastecimentoForm(FlaskForm):
    placa = StringField('Placa', validators=[DataRequired(), Length(max=10)])
    justificativa = TextAreaField('Justificativa', validators=[DataRequired()])
    supervisor = StringField('Supervisor', validators=[DataRequired(), Length(max=50)])
    setor = StringField('Setor', validators=[DataRequired(), Length(max=50)])
    quantidade_litros = IntegerField('Quantidade de Litros', validators=[DataRequired(), NumberRange(min=1)])
    tipo_combustivel = SelectField('Tipo de Combustível', choices=[
        ('Gasolina', 'Gasolina'),
        ('Etanol', 'Etanol'),
        ('Diesel S10', 'Diesel S10'),
        ('Diesel S500', 'Diesel S500'),
        ('GNV', 'GNV')
    ], validators=[DataRequired()])
    submit = SubmitField('Enviar')