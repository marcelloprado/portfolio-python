import json
import os
import re
import smtplib
import urllib.request
from collections import Counter
from datetime import datetime
from email.message import EmailMessage

from flask import Flask, render_template, request

app = Flask(__name__)


def carregar_env():
    """Carrega variáveis do arquivo .env (se existir) sem sobrescrever as do sistema."""
    caminho = os.path.join(app.root_path, ".env")
    if not os.path.exists(caminho):
        return
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            chave, valor = linha.split("=", 1)
            os.environ.setdefault(chave.strip(), valor.strip().strip('"').strip("'"))


carregar_env()

# Caminhos resolvidos a partir da raiz da aplicação: assim o app roda
# corretamente independente do diretório de onde foi iniciado (gunicorn, IIS, etc).
ARQUIVO_PROJETOS = os.path.join(app.root_path, "json", "projetos.json")
PASTA_CERTIFICADOS = os.path.join(app.root_path, "static", "assets", "imagens", "certificados")

EXTENSOES_IMAGEM = (".png", ".jpg", ".jpeg", ".webp")


def carregar_projetos():
    """Carrega a lista de projetos do JSON."""
    with open(ARQUIVO_PROJETOS, "r", encoding="utf-8") as f:
        return json.load(f)


def formatar_titulo_certificado(nome):
    """Transforma o nome do arquivo de um certificado em um título legível.

    Exemplos:
        "Lógica de programação_ mergulhe em JS" -> "Lógica de programação: mergulhe em JS"
        "1,2 - Entra21-Python-Back-end"         -> "Entra21 Python Back end (parte 1 de 2)"
    """
    # Certificados divididos em páginas usam o prefixo "<parte>,<total> - ".
    sufixo = ""
    partes = re.match(r"^(\d+),(\d+)\s*-\s*(.+)$", nome)
    if partes:
        sufixo = f" (parte {partes.group(1)} de {partes.group(2)})"
        nome = partes.group(3)

    # No nome do arquivo o "_" substitui os ":" que o Windows não aceita.
    titulo = nome.replace("_", ":").replace("-", " ")
    titulo = re.sub(r"\s{2,}", " ", titulo).strip()

    return titulo[:1].upper() + titulo[1:] + sufixo


def carregar_certificados():
    """Lê a pasta de certificados e devolve os itens já ordenados e com título legível.

    Os arquivos usam o padrão "<numero> - <nome do curso>.jpg". O número define a
    ordem cronológica; ordenar como texto colocaria o 10 antes do 2.
    """
    if not os.path.isdir(PASTA_CERTIFICADOS):
        return []

    certificados = []
    for arquivo in os.listdir(PASTA_CERTIFICADOS):
        if not arquivo.lower().endswith(EXTENSOES_IMAGEM):
            continue

        nome = os.path.splitext(arquivo)[0]
        numerado = re.match(r"^(\d+)\s*-\s*(.+)$", nome)

        if numerado:
            ordem = int(numerado.group(1))
            titulo = formatar_titulo_certificado(numerado.group(2))
        else:
            ordem = 999  # sem numeração: vai para o fim da lista
            titulo = formatar_titulo_certificado(nome)

        certificados.append({"arquivo": arquivo, "titulo": titulo, "ordem": ordem})

    return sorted(certificados, key=lambda c: (c["ordem"], c["titulo"]))


@app.context_processor
def variaveis_globais():
    """Disponibiliza valores usados pelo layout em todos os templates."""
    return {"ano_atual": datetime.now().year}


@app.route("/")
def home():
    lista_projetos = carregar_projetos()
    destaques = [p for p in lista_projetos if p.get("destaque")][:3]

    return render_template(
        "home.html",
        destaques=destaques,
        total_projetos=len(lista_projetos),
        total_certificados=len(carregar_certificados()),
    )


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


@app.route("/projetos")
def projetos():
    lista_projetos = carregar_projetos()

    # Filtros da galeria: cada tecnologia com quantos projetos a utilizam,
    # das mais usadas para as menos usadas.
    contagem = Counter(tec for p in lista_projetos for tec in p.get("tecnologias", []))
    tecnologias = [
        {"nome": nome, "contagem": total}
        for nome, total in sorted(contagem.items(), key=lambda item: (-item[1], item[0]))
    ]

    return render_template("projetos.html", projetos=lista_projetos, tecnologias=tecnologias)


@app.route("/certificados")
def certificados():
    return render_template("certificado.html", certificados=carregar_certificados())


EMAIL_VALIDO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_contato(dados):
    """Retorna um dicionário {campo: mensagem de erro} com os problemas encontrados."""
    erros = {}
    if len(dados["nome"]) < 2:
        erros["nome"] = "Informe seu nome."
    if not EMAIL_VALIDO.match(dados["email"]):
        erros["email"] = "Informe um e-mail válido."
    if len(dados["mensagem"]) < 10:
        erros["mensagem"] = "Escreva uma mensagem com pelo menos 10 caracteres."
    elif len(dados["mensagem"]) > 3000:
        erros["mensagem"] = "A mensagem pode ter no máximo 3000 caracteres."
    return erros


def enviar_email_contato(dados):
    """Envia a mensagem do formulário: pelo Resend se houver RESEND_API_KEY, senão por SMTP."""
    if os.environ.get("RESEND_API_KEY"):
        enviar_email_resend(dados)
    else:
        enviar_email_smtp(dados)


def enviar_email_resend(dados):
    """Envia pela API HTTPS do Resend (o Render gratuito bloqueia as portas SMTP)."""
    corpo = {
        "from": os.environ.get("EMAIL_REMETENTE", "Portfólio <onboarding@resend.dev>"),
        "to": [os.environ["EMAIL_DESTINO"]],
        "reply_to": dados["email"],
        "subject": f"[Portfólio] Mensagem de {dados['nome']}",
        "text": f"Nome: {dados['nome']}\nE-mail: {dados['email']}\n\n{dados['mensagem']}",
    }
    requisicao = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(corpo).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {os.environ['RESEND_API_KEY']}",
            "Content-Type": "application/json",
            "User-Agent": "portfolio-python",
        },
        method="POST",
    )
    # Erros HTTP (chave inválida, remetente não verificado...) viram OSError via HTTPError.
    with urllib.request.urlopen(requisicao, timeout=15):
        pass


def enviar_email_smtp(dados):
    """Envia a mensagem do formulário por SMTP usando as variáveis de ambiente."""
    usuario = os.environ["SMTP_USUARIO"]
    senha = os.environ["SMTP_SENHA"]
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    porta = int(os.environ.get("SMTP_PORTA", "587"))
    destino = os.environ.get("EMAIL_DESTINO", usuario)

    email = EmailMessage()
    email["Subject"] = f"[Portfólio] Mensagem de {dados['nome']}"
    email["From"] = usuario
    email["To"] = destino
    email["Reply-To"] = dados["email"]
    email.set_content(f"Nome: {dados['nome']}\nE-mail: {dados['email']}\n\n{dados['mensagem']}")

    with smtplib.SMTP(host, porta, timeout=15) as servidor:
        servidor.starttls()
        servidor.login(usuario, senha)
        servidor.send_message(email)


@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "GET":
        return render_template("contato.html", dados={}, erros={})

    dados = {
        "nome": request.form.get("nome", "").strip(),
        "email": request.form.get("email", "").strip(),
        "mensagem": request.form.get("mensagem", "").strip(),
    }

    # O campo "site" fica escondido: só robôs de spam o preenchem.
    if request.form.get("site"):
        return render_template("contato.html", dados={}, erros={}, status="enviado")

    erros = validar_contato(dados)
    if erros:
        return render_template("contato.html", dados=dados, erros=erros), 400

    try:
        enviar_email_contato(dados)
    except (KeyError, OSError, smtplib.SMTPException) as erro:
        app.logger.error("Falha ao enviar e-mail de contato: %s", erro)
        return render_template("contato.html", dados=dados, erros={}, status="falha"), 500

    return render_template("contato.html", dados={}, erros={}, status="enviado")


@app.route("/projeto/<id>")
def projeto_detalhe(id):
    lista_projetos = carregar_projetos()
    projeto = next((p for p in lista_projetos if p["id"] == id), None)

    if not projeto:
        return render_template("404.html"), 404

    # Demais projetos, para sugerir uma próxima leitura no fim da página.
    outros = [p for p in lista_projetos if p["id"] != id][:3]

    return render_template("projetoViews.html", projeto=projeto, outros=outros)


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)

    # ^ Para inicializar o ambiente virtual - .venv\Scripts\activate
    # ^ Arquivo principal do Flask para rodar o portfólio - python app.py