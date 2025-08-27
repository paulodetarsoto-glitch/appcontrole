# =========================================================
# Abastecimentos de Veículos - Controle
# Autor: Paulo Varão
# Atualizado: Versão sem banco de dados, usando apenas st.session_state
# =========================================================
import os
import io
import json
import pandas as pd
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
import base64
import plotly.express as px
import numpy as np

# ===========================
# Configurações iniciais / settings
# ===========================
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
DEFAULT_LOGO_PATH = os.path.join(PROJECT_DIR, "Logo_FrangoAmericano_slogan_COLOR.png")
SETTINGS_PATH = os.path.join(PROJECT_DIR, "settings.json")
DATA_FILE_PATH = os.path.join(PROJECT_DIR, "abastecimentos.csv")
CSS_PATH = os.path.join(PROJECT_DIR, "styles.css")

def create_default_settings():
    """Cria um arquivo de configurações padrão se ele não existir."""
    default_settings = {
        "logo_path": DEFAULT_LOGO_PATH,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "smtp_user": "",
        "smtp_password": "",
        "smtp_use_tls": True
    }
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(default_settings, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def create_default_css():
    """Cria um arquivo CSS padrão com suporte a tema escuro/claro se ele não existir."""
    CUSTOM_CSS = """
    :root {
        /* Variáveis para o tema claro (padrão) */
        --primary-dark: #01263f;
        --primary-medium: #003b63;
        --highlight-blue: #1F77B4;
        --app-background: #f0f2f6;
        --card-background: #ffffff;
        --text-color: #333333;
        --text-muted: #666666;
        --border-color: #e0e0e0;
        --input-background: #fcfcfc;
        --info-color: #17a2b8;
        --success-color: #28a745;
        --warning-color: #ffc107;
        --error-color: #dc3545;
    }

    @media (prefers-color-scheme: dark) {
        /* Variáveis para o tema escuro */
        --primary-dark: #007bff;
        --primary-medium: #0056b3;
        --highlight-blue: #33aaff;
        --app-background: #1a1a1a;
        --card-background: #2d2d2d;
        --text-color: #f0f2f6;
        --text-muted: #aaaaaa;
        --border-color: #444444;
        --input-background: #1a1a1a;
        --info-color: #5bc0de;
        --success-color: #5cb85c;
        --warning-color: #f0ad4e;
        --error-color: #d9534f;
    }

    /* Estilos Gerais */
    body {
        background: var(--app-background) !important;
        color: var(--text-color);
        font-family: 'Segoe UI', Roboto, sans-serif;
        margin: 0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, var(--primary-dark), var(--primary-medium));
        color: white !important;
        padding-top: 12px;
        box-shadow: 2px 0 5px rgba(0,0,0,0.1);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .sidebar-logo-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 8px 0 12px 0;
        margin-bottom: 20px;
    }
    [data-testid="stSidebarNav"] li > a {
        font-size: 1.1em;
        padding: 10px 20px;
        border-radius: 8px;
        margin: 5px 10px;
        transition: background-color 0.3s, color 0.3s;
    }
    [data-testid="stSidebarNav"] li > a:hover {
        background-color: rgba(255, 255, 255, 0.1);
        color: var(--highlight-blue) !important;
    }
    [data-testid="stSidebarNav"] li > a.current {
        background-color: var(--highlight-blue);
        font-weight: bold;
    }

    /* Cards */
    .app-card {
        background: var(--card-background);
        border-radius: 8px;
        padding: 15px 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid var(--border-color);
    }
    .title-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 15px;
        background: linear-gradient(90deg, var(--primary-dark), var(--primary-medium));
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .title-bar h2 {
        color: white !important;
        margin: 0;
        font-size: 1.8em;
        font-weight: 600;
    }
    .title-bar img {
        filter: brightness(0) invert(1);
    }
    .top-actions > button {
        margin-left: 10px;
        border-radius: 20px;
        padding: 8px 18px;
        font-weight: 500;
    }
    .table-actions button {
        margin-right: 8px;
        border-radius: 20px;
        padding: 6px 15px;
    }

    /* Botões */
    .stButton>button {
        background: var(--highlight-blue);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.2s, transform 0.2s;
    }
    .stButton>button:hover {
        background: var(--primary-medium);
        transform: translateY(-2px);
    }
    .stButton>button:active {
        transform: translateY(0);
    }

    /* Títulos */
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary-dark);
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    h3 {
        border-bottom: 2px solid var(--border-color);
        padding-bottom: 5px;
        margin-bottom: 15px;
        color: var(--primary-medium);
    }

    /* Mensagens de feedback */
    [data-testid="stNotification"] {
        border-radius: 8px;
        padding: 12px 18px;
        border: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    [data-testid="stNotification"] p {
        font-size: 1.0em;
    }

    [data-testid="stInfo"] { background-color: rgba(23,162,184,0.1); border-left: 5px solid var(--info-color); color: var(--info-color); }
    [data-testid="stSuccess"] { background-color: rgba(40,167,69,0.1); border-left: 5px solid var(--success-color); color: var(--success-color); }
    [data-testid="stWarning"] { background-color: rgba(255,193,7,0.1); border-left: 5px solid var(--warning-color); color: var(--warning-color); }
    [data-testid="stError"] { background-color: rgba(220,53,69,0.1); border-left: 5px solid var(--error-color); color: var(--error-color); }
    
    /* Inputs e Selectboxes */
    div[data-testid="stForm"] {
        background-color: var(--card-background);
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid var(--border-color);
    }

    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div>div>div:first-child {
        border-radius: 8px;
        border: 1px solid var(--border-color);
        padding: 10px 15px;
        background-color: var(--input-background);
        transition: border-color 0.2s, box-shadow 0.2s;
        color: var(--text-color);
    }
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stSelectbox>div>div>div>div>div:first-child:focus {
        border-color: var(--highlight-blue);
        box-shadow: 0 0 0 0.15rem rgba(31, 119, 180, 0.25);
        outline: none;
    }
    
    /* Estilo para desabilitar o autocomplete nos campos de texto */
    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    textarea:-webkit-autofill,
    textarea:-webkit-autofill:hover,
    textarea:-webkit-autofill:focus,
    select:-webkit-autofill,
    select:-webkit-autofill:hover,
    select:-webkit-autofill:focus {
        -webkit-box-shadow: 0 0 0px 1000px var(--card-background) inset !important;
        -webkit-text-fill-color: var(--text-color) !important;
    }

    /* Dashboard Metrics */
    [data-testid="stMetric"] {
        background-color: var(--card-background);
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid var(--border-color);
        text-align: center;
    }
    [data-testid="stMetric"] label {
        color: var(--text-muted);
        font-weight: normal;
        font-size: 1.0em;
        margin-bottom: 5px;
    }
    [data-testid="stMetric"] div[data-testid="stMarkdownContainer"] h1 {
        color: var(--highlight-blue);
        font-size: 2.2em;
        margin: 0;
        font-weight: 700;
    }

    /* Login Page */
    .login-background {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-color: var(--app-background);
        display: flex; align-items: center; justify-content: center; flex-direction: column;
        background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" opacity="0.1"><circle cx="50" cy="50" r="40" fill="%23007bff"/></svg>');
        background-size: 150px 150px;
    }
    .login-watermark {
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        opacity: 0.15;
        z-index: 0; max-width: 80%; height: auto;
        filter: grayscale(100%) brightness(200%);
    }
    .login-card {
        background-color: var(--card-background);
        padding: 30px; border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15); width: 100%; max-width: 420px;
        text-align: center; z-index: 1;
        border: 1px solid var(--border-color);
    }
    .login-logo-card { width: 100%; max-width: 300px; margin-bottom: 20px; }
    .login-title {
        font-size: 2.2em; font-weight: bold; color: var(--primary-dark);
        text-transform: uppercase; margin-bottom: 10px;
        letter-spacing: 1px;
    }
    .login-subtitle { font-size: 1.0em; color: var(--text-muted); margin-bottom: 25px; }
    .login-input {
        width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid var(--border-color);
        border-radius: 8px; font-size: 1.0em;
        background-color: var(--input-background);
        color: var(--text-color);
    }
    .login-button button {
        width: 100%; padding: 12px; font-size: 1.1em; font-weight: bold;
        background: var(--highlight-blue); color: white; border: none; border-radius: 8px;
        transition: background-color 0.2s, transform 0.2s;
    }
    .login-button button:hover {
        background: var(--primary-medium);
        transform: translateY(-2px);
    }
    .login-button button:active {
        transform: translateY(0);
    }

    .forgot-password { margin-top: 20px; font-size: 0.9em; color: var(--text-muted); }
    .forgot-password a { color: var(--highlight-blue); text-decoration: none; font-weight: 500; }
    .forgot-password a:hover { text-decoration: underline; }

    /* Estilo da tabela */
    .ag-cell[col-id="Status"] .ag-cell-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        padding: 0;
    }
    .ag-cell[col-id="Status"] .st-ag-editor-container .stSelectbox {
        width: 100%;
    }
    .ag-cell[col-id="Status"] .stSelectbox>div>div>div>div>div:first-child>div>div>div {
        border-radius: 4px;
        padding: 4px 8px;
        font-weight: bold;
        text-align: center;
        color: white !important;
    }
    .ag-cell[col-id="Status"] .stSelectbox>div>div>div>div>div:first-child[data-testid="stSelectbox-variant-Enviada"] {
        background-color: var(--info-color);
    }
    .ag-cell[col-id="Status"] .stSelectbox>div>div>div>div>div:first-child[data-testid="stSelectbox-variant-Abastecida"] {
        background-color: var(--success-color);
    }
    .ag-cell[col-id="Status"] .stSelectbox>div>div>div>div>div:first-child[data-testid="stSelectbox-variant-Cancelada"] {
        background-color: var(--error-color);
    }
    .st-emotion-cache-12t9w-1 {
        font-size: 0.8em;
    }
    .st-emotion-cache-1wv0j3r {
        padding: 4px 8px;
    }
    """
    try:
        with open(CSS_PATH, "w", encoding="utf-8") as f:
            f.write(CUSTOM_CSS)
        return True
    except Exception:
        return False

if not os.path.exists(SETTINGS_PATH):
    create_default_settings()
if not os.path.exists(CSS_PATH):
    create_default_css()

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_settings(s):
    try:
        target = SETTINGS_PATH
        with open(target, "w", encoding="utf-8") as f:
            json.dump(s, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar os dados: {e}")
        return False

_settings = load_settings()
LOGO_PATH = _settings.get("logo_path") if _settings.get("logo_path") else DEFAULT_LOGO_PATH
if LOGO_PATH and not os.path.isabs(LOGO_PATH):
    LOGO_PATH = os.path.join(PROJECT_DIR, LOGO_PATH)

st.set_page_config(page_title="Requisições de Abastecimento - Frango Americano", layout="wide", page_icon="⛽")

USERS = {
    "Rosimere Marques": "rosimere321",
    "Antonio Edinaldo": "edinaldo321",
    "Antonio Alfredo": "alfredo321",
    "Irisvan Martins": "irisvan321",
    "ADMINISTRADOR": "ADMADMADM",
}

USER_PERMISSIONS = {
    "Antonio Edinaldo": ["requisicoes", "dashboard", "narrativas"],
    "Antonio Alfredo": ["requisicoes"],
    "Rosimere Marques": ["requisicoes"],
    "Irisvan Martins": ["requisicoes"],
    "ADMINISTRADOR": ["requisicoes", "dashboard", "narrativas", "configuracoes"]
}

# ===========================
# Funções de Estilo
# ===========================
def load_and_inject_css(css_file_path):
    """Lê um arquivo CSS e injeta os estilos na página do Streamlit."""
    if os.path.exists(css_file_path):
        with open(css_file_path, "r", encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.error(f"Arquivo CSS não encontrado: {css_file_path}")

load_and_inject_css(CSS_PATH)

# ===========================
# Funções utilitárias
# ===========================
def normalize_combustivel(c: str) -> str:
    if not isinstance(c, str):
        return ""
    if "etanol" in c.lower():
        return "Etanol"
    if "gasolina" in c.lower():
        return "Gasolina"
    if "diesel s10" in c.lower():
        return "Diesel S10"
    if "diesel s500" in c.lower():
        return "Diesel S500"
    if "arla" in c.lower():
        return "Arla"
    return c.strip()

def format_placa(placa: str) -> str:
    placa = placa.strip().upper().replace("-", "").replace(" ", "")
    if len(placa) >= 7 and placa[:3].isalpha() and placa[3].isdigit() and placa[4].isalpha() and placa[5:].isdigit():
        return f"{placa[:3]}-{placa[3]}{placa[4]}{placa[5:]}"
    if len(placa) >= 7 and placa[:3].isalpha() and placa[3:].isdigit():
        return f"{placa[:3]}-{placa[3:]}"
    return placa

def is_valid_email(email: str) -> bool:
    import re
    if not email:
        return False
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def send_email_with_pdf(to_email: str, subject: str, body: str, pdf_data: bytes, filename: str):
    settings = load_settings()
    smtp_server = settings.get("smtp_server")
    smtp_port = settings.get("smtp_port")
    smtp_user = settings.get("smtp_user")
    smtp_password = settings.get("smtp_password")
    smtp_use_tls = settings.get("smtp_use_tls", True)

    if not all([smtp_server, smtp_port, smtp_user, smtp_password, to_email]):
        st.error("Configurações de SMTP incompletas. Verifique a página 'Configurações'.")
        return False
    
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))
    part = MIMEApplication(pdf_data, _subtype="pdf")
    part.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(part)

    try:
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
            if smtp_use_tls:
                server.starttls()
        
        with server:
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {e}. Verifique as configurações de SMTP e a senha do aplicativo (se for o caso).")
        return False

# ===========================
# Geração de PDF
# ===========================
def generate_request_pdf(payload: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    if payload.get("logo_path") and os.path.exists(payload["logo_path"]):
        try:
            img = Image(payload["logo_path"], width=110, height=50)
            story.append(img)
            story.append(Spacer(1, 8))
        except Exception:
            pass

    empresa = payload.get("empresa", "Frango Americano")
    data_envio = datetime.now().strftime("%d/%m/%Y %H:%M")
    header_style = ParagraphStyle('HeaderStyle', parent=styles['Title'], alignment=0, fontSize=14)
    header = Paragraph(f"<b>{empresa}</b> — {data_envio}", header_style)
    story.append(header)
    story.append(Spacer(1, 12))

    placa = payload.get("placa", "").upper()
    title = Paragraph(f"Requisição de Abastecimento          {placa}", styles['Heading2'])
    story.append(title)
    story.append(Spacer(1, 12))

    meta = [
        ["Data da Requisição:", payload.get("data", "")],
        ["Posto fornecedor:", payload.get("posto", "")],
        ["Referente do veículo:", payload.get("tipo_posto", "")],
        ["Placa:", payload.get("placa", "")],
        ["Motorista:", payload.get("motorista", "")],
        ["Supervisor:", payload.get("supervisor", "")],
        ["Setor:", payload.get("setor", "")],
        ["Subsetor:", payload.get("subsetor", "")],
        ["Cidade:", payload.get("cidade", "")],
    ]

    if payload.get("km_atual") not in (None, "", 0):
        meta.append(["Quilometragem atual (no momento):", str(payload.get("km_atual", ""))])
    if payload.get("litros") not in (None, ""):
        meta.append(["Quantidade solicitada (L):", str(payload.get("litros", ""))])
    if payload.get("valor_total") not in (None, "", 0):
        meta.append(["Valor total:", f"R$ {float(payload.get('valor_total')):,.2f}"])
    if payload.get("combustivel"):
        meta.append(["Combustivel:", payload.get("combustivel", "")])

    tbl = Table(meta, colWidths=[160, 330])
    tbl.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.grey),
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica')
    ]))
    story.append(tbl)
    story.append(Spacer(1, 16))

    story.append(Paragraph("<b>Justificativa / Observações</b>", styles['Heading3']))
    justificativa = Paragraph((payload.get("justificativa") or "").replace("\n","<br/>"), styles['Normal'])
    story.append(justificativa)
    story.append(Spacer(1, 50))

    story.append(Paragraph(f"Requisição solicitada por: {payload.get('solicitante','')}", styles['Normal']))
    story.append(Spacer(1, 25))
    story.append(Paragraph("Assinatura do condutor: ____________________________", styles['Normal']))
    story.append(Spacer(1, 25))
    story.append(Paragraph("Quilometragem atual: _________________________"))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# ===========================
# Funções de persistência de dados
# ===========================
def load_data(filename=DATA_FILE_PATH):
    """Carrega os dados de um arquivo CSV, se ele existir."""
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename)
            df['data'] = pd.to_datetime(df['data'], errors='coerce')
            df['DataUso'] = pd.to_datetime(df['DataUso'], errors='coerce')
            df['total_litros'] = pd.to_numeric(df['total_litros'], errors='coerce')
            df['valor_total'] = pd.to_numeric(df['valor_total'], errors='coerce')
            df['Odometro'] = pd.to_numeric(df['Odometro'], errors='coerce')
            df['KmUso'] = pd.to_numeric(df['KmUso'], errors='coerce')
            df['total_litros'] = df['total_litros'].fillna(0)
            df['valor_total'] = df['valor_total'].fillna(0)
            df['Odometro'] = df['Odometro'].fillna(0)
            df['KmUso'] = df['KmUso'].fillna(0)
            if 'Cidade' not in df.columns:
                df['Cidade'] = ""
            return df
        except Exception as e:
            st.error(f"Erro ao carregar os dados: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

def save_data(df, filename=DATA_FILE_PATH):
    """Salva o DataFrame em um arquivo CSV."""
    try:
        df.to_csv(filename, index=False)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar os dados: {e}")
        return False

# ===========================
# Páginas da Aplicação
# ===========================
def pagina_requisicoes():
    if "requisicoes" not in USER_PERMISSIONS.get(st.session_state.get("current_user"), []):
        st.warning("Você não tem permissão para acessar esta página.")
        return

    col_main_title, col_button = st.columns([4, 1])
    with col_main_title:
        st.markdown("<div class='app-card title-bar'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        with col1:
            if LOGO_PATH and os.path.exists(LOGO_PATH):
                st.image(LOGO_PATH, width=140)
        with col2:
            st.markdown("<h2 style='margin:0'>Requisição de abastecimento</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_button:
        if not st.session_state.get("show_new_req_form", False):
            st.markdown("<div style='padding-top: 15px;'>", unsafe_allow_html=True)
            if st.button("+ Nova Requisição"):
                st.session_state.show_new_req_form = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.session_state.get("show_new_req_form", False):
        st.markdown("### Nova Requisição")
        
        POSTOS_LIST = ["R A Mendes", "Toca Da Onça", "Petronorte", "Linhares", "Posto Minas Gerais", "Boa Vista", "Medeiros", "Posto Americano", "Posto Milena", "NR Comercio Comb.", "Auto Posto Netinho", "Posto Oriente", "Posto R.S.F.", "Rede K"]
        
        with st.form("form_nova_req", clear_on_submit=False):
            colA, colB, colC = st.columns(3)
            with colA:
                placa = st.text_input("Placa", max_chars=8, help="O hífen será adicionado automaticamente.", autocomplete="off")
                condutor = st.text_input("Condutor", autocomplete="off")
                supervisor = st.session_state.get('current_user')
                st.info(f"{supervisor}")
                setor = st.selectbox("Setor", ["Abatedouro", "Fábrica Tocantinópolis", "Granjas de produção", "Incubatório", "Granjas Matrizes", "CD Paraíso", "Fábrica de Araguaína"])
                subsetor = st.selectbox("Subsetor", ["Congelados", "Transporte de funcionários", "Campo", "Pega de frango", "Integração"])
                email_posto = st.text_input("E-mail do Posto", autocomplete="off")
            with colB:
                tipo_posto = st.selectbox("Referente do veículo", ["Próprio", "Terceiro"])
                litros = st.number_input("Quantidade (L)", min_value=0.0, step=0.1, value=0.0)
                tanque_cheio = st.checkbox("Tanque cheio")
                combustivel = st.selectbox("Combustível", ["Gasolina", "Etanol", "Diesel S10", "Diesel S500", "Arla"])
                posto = st.selectbox("Posto", POSTOS_LIST)
            with colC:
                data_req = st.date_input("Data da requisição", value=datetime.today(), disabled=True)
                cidade = st.text_input("Cidade", autocomplete="off")
                referente = st.text_area("Observações / Justificativa", height=80)

            col_submit, col_cancel = st.columns([1, 1])
            with col_submit:
                enviar = st.form_submit_button("Enviar e-mail de requisição")
            with col_cancel:
                cancelar = st.form_submit_button("Cancelar")

            if cancelar:
                st.session_state.show_new_req_form = False
                st.rerun()
            
            if enviar:
                required_fields = {
                    "Placa": placa, "Condutor": condutor, "Email do Posto": email_posto,
                    "Posto": posto, "Setor": setor, "Subsetor": subsetor,
                    "Referente do veículo": tipo_posto, "Combustível": combustivel,
                    "Observações / Justificativa": referente, "Cidade": cidade
                }
                
                if not tanque_cheio:
                    required_fields["Quantidade (L)"] = litros

                missing_fields = [field for field, value in required_fields.items() if not value or value == 0.0]
                
                if missing_fields:
                    st.error(f"Por favor, preencha todos os campos obrigatórios: {', '.join(missing_fields)}")
                elif email_posto and not is_valid_email(email_posto):
                    st.error("O e-mail do posto não é válido.")
                else:
                    placa_formatada = format_placa(placa)
                    combustivel_norm = normalize_combustivel(combustivel)
                    payload = {
                        "empresa": "Frango Americano", "logo_path": LOGO_PATH if LOGO_PATH else None,
                        "data": data_req.strftime("%Y-%m-%d"), "posto": posto.strip(),
                        "email_posto": email_posto.strip(), "tipo_posto": tipo_posto,
                        "placa": placa_formatada, "motorista": condutor.strip(), "supervisor": supervisor.strip(),
                        "setor": setor.strip(), "subsetor": subsetor.strip(),
                        "litros": litros if not tanque_cheio else None, "valor_total": None, "km_atual": None,
                        "combustivel": combustivel_norm, "justificativa": referente.strip(),
                        "solicitante": condutor.strip(), "cidade": cidade.strip()
                    }
                    
                    try:
                        pdf_bytes = generate_request_pdf(payload)
                        st.session_state["pdf_data"] = pdf_bytes
                        st.session_state["pdf_filename"] = f"requisicao_{placa_formatada}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
                        
                        if send_email_with_pdf(
                            to_email=email_posto.strip(),
                            subject=f"Requisição de Abastecimento - {placa_formatada}",
                            body="<p>Prezado(a) Posto,</p><p>Segue em anexo a requisição de abastecimento.</p><p>Atenciosamente,</p><p>Equipe Frango Americano</p>",
                            pdf_data=pdf_bytes,
                            filename=st.session_state["pdf_filename"]
                        ):
                            new_id = st.session_state.df_abastecimentos['id'].max() + 1 if not st.session_state.df_abastecimentos.empty else 1
                            
                            new_req = {
                                "id": int(new_id),
                                "Placa": placa_formatada, "valor_total": 0.0,
                                "total_litros": litros if not tanque_cheio else None, "data": data_req.strftime("%Y-%m-%d"),
                                "Referente": referente.strip(), "Odometro": None,
                                "Posto": posto.strip(), "Combustivel": normalize_combustivel(combustivel),
                                "Condutor": condutor.strip(), "Unidade": "", "Setor": setor.strip(),
                                "Status": "Enviada", "Subsetor": subsetor.strip(),
                                "Observacoes": referente.strip(), "TanqueCheio": 1 if tanque_cheio else 0,
                                "DataUso": None, "KmUso": None, "EmailPosto": email_posto.strip(),
                                "TipoPosto": tipo_posto, "Supervisor": supervisor.strip(),
                                "Cidade": cidade.strip()
                            }
                            
                            st.session_state.df_abastecimentos = pd.concat([st.session_state.df_abastecimentos, pd.DataFrame([new_req])], ignore_index=True)
                            
                            save_data(st.session_state.df_abastecimentos)

                            st.success("✅ Requisição salva e e-mail enviado com sucesso!")
                            st.session_state.show_new_req_form = False
                            st.rerun()
                        else:
                            st.error("Não foi possível enviar o e-mail. A requisição não foi salva.")

                    except Exception as e:
                        st.error(f"Erro ao gerar PDF ou enviar e-mail: {e}")
                        st.info("A requisição não foi salva. Verifique a instalação do reportlab e as configurações de SMTP.")
                        st.session_state["pdf_data"] = None

    else:
        st.markdown("### Histórico de Requisições")
        if st.session_state.df_abastecimentos.empty:
            st.info("Nenhuma requisição registrada ainda.")
            return

        df = st.session_state.df_abastecimentos.copy()
        
        df['DataUso'] = pd.to_datetime(df['DataUso'], errors='coerce')
        df['valor_total'] = pd.to_numeric(df['valor_total'], errors='coerce')
        df['total_litros'] = pd.to_numeric(df['total_litros'], errors='coerce')
        df['Odometro'] = pd.to_numeric(df['Odometro'], errors='coerce')
        df['data'] = pd.to_datetime(df['data'], errors='coerce').dt.strftime("%Y-%m-%d")
        
        df['Quantidade'] = np.where(
            df['TanqueCheio'].astype(int) == 1,
            "Tanque cheio",
            df['total_litros'].astype(str)
        )

        df['Supervisor'] = df.apply(lambda r: r.get('Supervisor') or "", axis=1)
        
        is_admin = st.session_state.get('current_user') == "ADMINISTRADOR"

        status_options = {
            "Enviada": "Enviada", 
            "Abastecida": "Abastecida", 
            "Cancelada": "Cancelada"
        }
        
        df_display = df.copy()
        df_display = df_display.drop(columns=['Referente', 'Unidade', 'TanqueCheio', 'KmUso', 'EmailPosto', 'TipoPosto', 'Supervisor'], errors='ignore')

        df_display['DataUso'] = df_display['DataUso'].dt.strftime("%d/%m/%Y")
        
        df_display['Ações'] = ""

        column_config_dict = {
            "id": st.column_config.NumberColumn("ID", disabled=True, width="small"),
            "data": st.column_config.DateColumn("Data Req.", format="DD/MM/YYYY", disabled=True, width="small"),
            "Placa": st.column_config.TextColumn("Placa", disabled=True, width="small"),
            "Condutor": st.column_config.TextColumn("Condutor", disabled=True),
            "Supervisor": st.column_config.TextColumn("Supervisor", disabled=True),
            "Setor": st.column_config.TextColumn("Setor", disabled=True),
            "Subsetor": st.column_config.TextColumn("Subsetor", disabled=True),
            "Cidade": st.column_config.TextColumn("Cidade", disabled=True),
            "total_litros": st.column_config.NumberColumn("Litros", format="%.2f L", disabled=True, width="small"),
            "valor_total": st.column_config.NumberColumn("Valor", format="R$ %.2f", disabled=not is_admin, width="small"),
            "Combustivel": st.column_config.TextColumn("Combustível", disabled=True, width="small"),
            "Posto": st.column_config.TextColumn("Posto", disabled=True, width="small"),
            "Status": st.column_config.SelectboxColumn("Status", options=list(status_options.keys()), disabled=not is_admin, width="small"),
            "Odometro": st.column_config.NumberColumn("Km", disabled=not is_admin, width="small"),
            "DataUso": st.column_config.DateColumn("Data Uso", format="DD/MM/YYYY", disabled=not is_admin, width="small"),
            "Observacoes": st.column_config.TextColumn("Observações", disabled=not is_admin, width="medium"),
        }

        edited_df = st.data_editor(
            df_display,
            column_config=column_config_dict,
            hide_index=True,
            use_container_width=True,
            disabled=(not is_admin)
        )

        if is_admin:
            if not edited_df.equals(df_display):
                st.session_state.df_abastecimentos = edited_df
                save_data(st.session_state.df_abastecimentos)
                st.toast("✅ Registros atualizados com sucesso!")
                st.rerun()

            st.markdown("---")
            st.markdown("### Ações de Administrador")
            st.warning("Estas ações são permanentes e só devem ser executadas por um administrador.")

            with st.form("admin_actions_form"):
                st.markdown("Selecione os IDs das requisições para exclusão:")
                ids_to_delete = st.text_input("IDs (separados por vírgula)", autocomplete="off")
                
                col_actions = st.columns(2)
                with col_actions[0]:
                    delete_button = st.form_submit_button("Excluir Selecionados")
                with col_actions[1]:
                    cancel_button_admin = st.form_submit_button("Cancelar Selecionados")

                if delete_button:
                    if ids_to_delete:
                        ids_list = [int(i.strip()) for i in ids_to_delete.split(',') if i.strip().isdigit()]
                        st.session_state.df_abastecimentos = st.session_state.df_abastecimentos[~st.session_state.df_abastecimentos['id'].isin(ids_list)].reset_index(drop=True)
                        save_data(st.session_state.df_abastecimentos)
                        st.success(f"Requisição(ões) com IDs {ids_list} excluída(s) permanentemente.")
                        st.rerun()
                    else:
                        st.warning("Nenhum ID inserido para exclusão.")
                
                if cancel_button_admin:
                    if ids_to_delete:
                        ids_list = [int(i.strip()) for i in ids_to_delete.split(',') if i.strip().isdigit()]
                        st.session_state.df_abastecimentos.loc[st.session_state.df_abastecimentos['id'].isin(ids_list), 'Status'] = 'Cancelada'
                        save_data(st.session_state.df_abastecimentos)
                        st.success(f"Requisição(ões) com IDs {ids_list} cancelada(s).")
                        st.rerun()
                    else:
                        st.warning("Nenhum ID inserido para cancelamento.")


def pagina_dashboard():
    if "dashboard" not in USER_PERMISSIONS.get(st.session_state.get("current_user"), []):
        st.warning("Você não tem permissão para acessar esta página.")
        return
        
    st.header("📊 Dashboard de Abastecimentos")
    if LOGO_PATH and os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=120)

    if st.session_state.df_abastecimentos.empty:
        st.info("Nenhum dado registrado ainda.")
        return
        
    df = st.session_state.df_abastecimentos.copy()
    
    df.columns = [c.strip() for c in df.columns]
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    df = df.dropna(subset=['data'])
    
    df['mes_ano'] = df['data'].dt.to_period('M').astype(str)
    
    total_litros = df['total_litros'].sum() if 'total_litros' in df.columns else 0.0
    total_valor = df['valor_total'].sum() if 'valor_total' in df.columns else 0.0
    n_veiculos = df["Placa"].nunique() if 'Placa' in df.columns else 0

    k1, k2, k3 = st.columns(3)
    with k1: st.metric("🚗 Veículos distintos", int(n_veiculos))
    with k2: st.metric("🛢 Total de litros", f"{total_litros:,.2f}")
    with k3: st.metric("💰 Valor total gasto", f"R$ {total_valor:,.2f}")
    
    st.markdown("---")

    st.subheader("Consumo de Combustível por Mês")
    consumo_por_mes = df.groupby('mes_ano')['total_litros'].sum().reset_index()
    fig1 = px.bar(consumo_por_mes, x='mes_ano', y='total_litros', 
                  labels={'mes_ano': 'Mês/Ano', 'total_litros': 'Total de Litros'},
                  color_discrete_sequence=[_settings.get("highlight_blue", "#1F77B4")])
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Litros Consumidos por Veículo (Top 10)")
    consumo_por_placa = df.groupby('Placa')['total_litros'].sum().nlargest(10).reset_index()
    fig2 = px.pie(consumo_por_placa, values='total_litros', names='Placa', 
                  title='Consumo por Placa', hole=.3,
                  color_discrete_sequence=px.colors.sequential.Bluyl)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Consumo por Tipo de Combustível")
    consumo_por_comb = df.groupby('Combustivel')['total_litros'].sum().reset_index()
    fig3 = px.bar(consumo_por_comb, x='Combustivel', y='total_litros',
                  labels={'Combustivel': 'Combustível', 'total_litros': 'Total de Litros'},
                  color_discrete_sequence=[_settings.get("primary_medium", "#003b63")])
    st.plotly_chart(fig3, use_container_width=True)

def generate_narrative(df):
    """Gera uma narrativa analítica simulando uma IA."""
    narrativas = []
    
    total_litros = df['total_litros'].sum() if 'total_litros' in df.columns else 0
    total_valor = df['valor_total'].sum() if 'valor_total' in df.columns else 0
    narrativas.append(f"Análise geral: O volume total de combustível consumido foi de **{total_litros:,.2f} litros**, com um custo total de **R$ {total_valor:,.2f}**.")
    
    if not df.empty and 'Placa' in df.columns:
        top_placa = df.groupby('Placa')['total_litros'].sum().idxmax()
        top_consumo = df.groupby('Placa')['total_litros'].sum().max()
        narrativas.append(f"Principais veículos: O veículo de placa **{top_placa}** foi o maior consumidor, com um total de **{top_consumo:,.2f} litros**.")
        
    if not df.empty and 'data' in df.columns:
        df_monthly = df.set_index('data').resample('M')['total_litros'].sum()
        if not df_monthly.empty:
            pico_mes = df_monthly.idxmax()
            pico_consumo = df_monthly.max()
            narrativas.append(f"Tendências de consumo: O pico de consumo ocorreu em **{pico_mes.strftime('%B de %Y')}**, com um total de **{pico_consumo:,.2f} litros**.")
    
    if not df.empty and 'total_litros' in df.columns:
        media_litros = df['total_litros'].mean()
        narrativas.append(f"Eficiência: A média de litros por requisição é de aproximadamente **{media_litros:,.2f} litros**.")
        
    return narrativas

def pagina_narrativas():
    if "narrativas" not in USER_PERMISSIONS.get(st.session_state.get("current_user"), []):
        st.warning("Você não tem permissão para acessar esta página.")
        return
        
    st.header("🧠 Narrativas")
    if LOGO_PATH and os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=120)

    if st.session_state.df_abastecimentos.empty:
        st.info("Sem dados para gerar narrativas.")
        return
    
    df = st.session_state.df_abastecimentos.copy()
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    
    df_filtered = df.dropna(subset=['data'])
    
    narratives = generate_narrative(df_filtered)
    
    st.markdown("### Insights Analíticos")
    for narrative in narratives:
        st.markdown(f"- {narrative}")

def pagina_configuracoes():
    if "configuracoes" not in USER_PERMISSIONS.get(st.session_state.get("current_user"), []):
        st.warning("Você não tem permissão para acessar esta página.")
        return
    
    st.header("⚙️ Configurações")
    st.markdown("Preencha as configurações abaixo para SMTP, remetente e logo.")
    settings = load_settings()
    with st.form("form_settings"):
        smtp_server = st.text_input("SMTP Server", value=settings.get("smtp_server", "smtp.gmail.com"), autocomplete="off")
        smtp_port = st.number_input("SMTP Port", min_value=1, max_value=65535, value=int(settings.get("smtp_port", 587)))
        smtp_user = st.text_input("SMTP User (e-mail remetente)", value=settings.get("smtp_user", ""), autocomplete="off")
        
        st.markdown(
            "⚠️ **Atenção**: Para contas do Google (Gmail), a senha deve ser uma **senha de aplicativo**."
            " A senha normal não funciona devido a políticas de segurança."
        )
        st.markdown(
            "🔗 [Clique aqui para gerar uma senha de aplicativo do Google](https://myaccount.google.com/apppasswords)"
        )
        smtp_password = st.text_input("SMTP Password (Senha de aplicativo)", value=settings.get("smtp_password", ""), type="password", autocomplete="new-password")
        smtp_use_tls = st.checkbox("Usar TLS (Recomendado para a maioria dos servidores)", value=settings.get("smtp_use_tls", True))
        salvar = st.form_submit_button("Salvar configurações")
        
        if salvar:
            if not smtp_server or not smtp_user or not smtp_password:
                st.error("Por favor, preencha todos os campos obrigatórios (servidor, usuário e senha).")
            else:
                new = {
                    "smtp_server": smtp_server,
                    "smtp_port": smtp_port,
                    "smtp_user": smtp_user,
                    "smtp_password": smtp_password,
                    "smtp_use_tls": smtp_use_tls,
                }
                ok = save_settings(new)
                if ok:
                    st.success("Configurações salvas com sucesso.")
                    _settings.update(new)
                else:
                    st.error("Erro ao salvar configurações.")
    
    if st.button("Voltar para Requisições"):
        st.session_state.view_mode = "requisicoes"
        st.rerun()

def _get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    return ""

def login_page():
    st.markdown('<div class="login-background">', unsafe_allow_html=True)
    if os.path.exists(LOGO_PATH):
        st.markdown(f'<img src="data:image/png;base64,{_get_base64_image(LOGO_PATH)}" class="login-watermark">', unsafe_allow_html=True)
    
    st.image(LOGO_PATH, width=315)
    st.markdown('<h2 class="login-title">FAÇA LOGIN</h2>', unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Usuário", placeholder="Digite seu nome", label_visibility="collapsed", autocomplete="off")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha", label_visibility="collapsed", autocomplete="new-password")
        submit_button = st.form_submit_button("Entrar", type="primary")

    if submit_button:
        if USERS.get(username) == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.toast(f"Bem-vindo(a), {username}! Você acessou o sistema com sucesso.")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")
            st.session_state.logged_in = False
    
    forgot_password_link = "paulodetarso.to@frangoamericano.com"
    st.markdown(f'<p class="forgot-password">Esqueceu sua senha? <a href="mailto:{forgot_password_link}">Clique aqui</a></p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.toast("Você saiu do sistema.")
    st.rerun()

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "df_abastecimentos" not in st.session_state:
        st.session_state.df_abastecimentos = load_data()
        if st.session_state.df_abastecimentos.empty:
            initial_data = {
                "id": [], "Placa": [], "valor_total": [], "total_litros": [], "data": [], "Referente": [],
                "Odometro": [], "Posto": [], "Combustivel": [], "Condutor": [], "Unidade": [], "Setor": [],
                "Status": [], "Subsetor": [], "Observacoes": [], "TanqueCheio": [], "DataUso": [],
                "KmUso": [], "EmailPosto": [], "TipoPosto": [], "Supervisor": [], "Cidade": []
            }
            st.session_state.df_abastecimentos = pd.DataFrame(initial_data)
            save_data(st.session_state.df_abastecimentos)

    if "show_new_req_form" not in st.session_state:
        st.session_state.show_new_req_form = False

    if not st.session_state.logged_in:
        login_page()
        return

    st.sidebar.markdown(f'<div class="sidebar-logo-wrapper"><img src="data:image/png;base64,{_get_base64_image(LOGO_PATH)}" width="100"></div>', unsafe_allow_html=True)
    st.sidebar.title("Menu")
    
    current_user = st.session_state.get('current_user')
    allowed_pages = USER_PERMISSIONS.get(current_user, [])

    if "requisicoes" in allowed_pages:
        button_class = "current" if st.session_state.get("view_mode") == "requisicoes" else ""
        if st.sidebar.button("⛽ Requisições", key="btn_req"):
            st.session_state.view_mode = "requisicoes"
    if "dashboard" in allowed_pages:
        button_class = "current" if st.session_state.get("view_mode") == "dashboard" else ""
        if st.sidebar.button("📊 Dashboard", key="btn_dash"):
            st.session_state.view_mode = "dashboard"
    if "narrativas" in allowed_pages:
        button_class = "current" if st.session_state.get("view_mode") == "narrativas" else ""
        if st.sidebar.button("🧠 Narrativas", key="btn_nar"):
            st.session_state.view_mode = "narrativas"
    if "configuracoes" in allowed_pages:
        button_class = "current" if st.session_state.get("view_mode") == "configuracoes" else ""
        if st.sidebar.button("⚙️ Configurações", key="btn_conf"):
            st.session_state.view_mode = "configuracoes"

    if st.sidebar.button("Sair", key="btn_logout"):
        logout()
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"Seja bem vindo ao controle de abastecimentos, **{current_user}** !")

    if "view_mode" not in st.session_state or st.session_state.view_mode not in allowed_pages:
        st.session_state.view_mode = allowed_pages[0] if allowed_pages else "requisicoes"

    if st.session_state.view_mode == "requisicoes":
        pagina_requisicoes()
    elif st.session_state.view_mode == "dashboard":
        pagina_dashboard()
    elif st.session_state.view_mode == "narrativas":
        pagina_narrativas()
    elif st.session_state.view_mode == "configuracoes":
        pagina_configuracoes()

if __name__ == "__main__":
    main()
