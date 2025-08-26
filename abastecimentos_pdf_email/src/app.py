from flask import Flask, render_template, request, redirect, url_for
from forms import AbastecimentoForm
from pdf_generator import generate_pdf
from emailer import send_email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = AbastecimentoForm()
    if form.validate_on_submit():
        # Collect form data
        placa = form.placa.data
        justificativa = form.justificativa.data
        supervisor = form.supervisor.data
        setor = form.setor.data
        quantidade_litros = form.quantidade_litros.data
        tipo_combustivel = form.tipo_combustivel.data
        
        # Generate PDF
        pdf_path = generate_pdf(placa, justificativa, supervisor, setor, quantidade_litros, tipo_combustivel)
        
        # Send email with PDF attachment
        send_email(pdf_path)
        
        return redirect(url_for('success'))
    
    return render_template('index.html', form=form)

@app.route('/success')
def success():
    return "Abastecimento registrado e e-mail enviado com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)