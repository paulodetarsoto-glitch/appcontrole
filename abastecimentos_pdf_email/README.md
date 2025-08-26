# Abastecimentos PDF Email Project

Este projeto é uma aplicação em Python que permite coletar informações sobre abastecimentos de veículos e enviar essas informações por e-mail em formato PDF. A aplicação inclui um formulário para entrada de dados e utiliza templates para gerar o PDF e o corpo do e-mail.

## Estrutura do Projeto

```
abastecimentos_pdf_email
├── src
│   ├── app.py               # Ponto de entrada da aplicação
│   ├── forms.py             # Definição do formulário de coleta de dados
│   ├── pdf_generator.py      # Geração do documento PDF
│   ├── emailer.py           # Funções para envio de e-mails
│   ├── db.py                # Gerenciamento de conexões com o banco de dados
│   ├── utils.py             # Funções utilitárias
│   └── templates
│       ├── email.html       # Template HTML para o corpo do e-mail
│       └── pdf_template.html # Template HTML para o documento PDF
├── tests
│   ├── test_forms.py        # Testes unitários para o formulário
│   ├── test_pdf.py          # Testes unitários para a geração de PDF
│   └── test_email.py        # Testes unitários para o envio de e-mails
├── requirements.txt          # Dependências do projeto
├── .env.example              # Exemplo de variáveis de ambiente
├── .gitignore                # Arquivos e diretórios a serem ignorados pelo Git
├── Dockerfile                # Instruções para construir a imagem Docker
└── README.md                 # Documentação do projeto
```

## Instalação

1. Clone o repositório:
   ```
   git clone <URL_DO_REPOSITORIO>
   cd abastecimentos_pdf_email
   ```

2. Crie um ambiente virtual e ative-o:
   ```
   python -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   venv\Scripts\activate     # Para Windows
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente conforme necessário, utilizando o arquivo `.env.example` como referência.

## Uso

1. Execute a aplicação:
   ```
   python src/app.py
   ```

2. Acesse a aplicação em seu navegador no endereço `http://localhost:5000`.

3. Preencha o formulário com as informações de abastecimento e envie.

4. O PDF será gerado e enviado para o e-mail especificado.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.