# 📌 Portfólio em Python (Flask)

🚀 Meu portfólio desenvolvido em Python + Flask, apresentando meus projetos, certificados e trajetória de forma organizada e responsiva.

🔗 Acesse online: [Portfólio](https://portfolio-python-swqi.onrender.com/)

## 🛠️ Tecnologias Utilizadas

* **Back-end:** Python (Flask, Jinja2, Werkzeug)
* **Front-end:** HTML5, CSS3, JavaScript (sem framework), Bootstrap 5
* **Dados:** os projetos vêm de um arquivo `json/projetos.json`
* **Servidor de produção:** gunicorn
* **Gerenciamento de dependências:** `requirements.txt`

## 📂 Estrutura do Projeto

```
portfolio-python
 ┣ json
 ┃ ┗ projetos.json          # fonte de dados dos projetos
 ┣ static
 ┃ ┗ assets
 ┃   ┣ css                  # um arquivo por página + style.css (design system)
 ┃   ┣ imagens
 ┃   ┗ js
 ┣ templates
 ┃ ┣ partials
 ┃ ┃ ┗ _projeto_card.html   # cartão reutilizado na home e na galeria
 ┃ ┣ base.html              # layout, navegação, rodapé e metatags
 ┃ ┣ home.html
 ┃ ┣ sobre.html
 ┃ ┣ projetos.html
 ┃ ┣ projetoViews.html
 ┃ ┣ certificado.html
 ┃ ┣ contato.html
 ┃ ┗ 404.html
 ┣ app.py
 ┣ requirements.txt
 ┗ .gitignore
```

### Como o CSS está organizado

`style.css` concentra o design system (variáveis de cor, tipografia, botões, cartões,
navegação e rodapé) e é carregado em todas as páginas junto de `menuHamburger.css`.
Cada página carrega apenas o seu próprio CSS pelo bloco `{% block styles %}`, evitando
que os estilos de uma página vazem para as outras.

## ✨ Funcionalidades

✔️ Página inicial com apresentação, estatísticas e projetos em destaque
✔️ Galeria de projetos em grade, com filtro por tecnologia e preview animado no hover
✔️ Página de detalhe por projeto, com vídeo, tecnologias e links
✔️ Página de certificados com busca e visualizador em tela cheia
✔️ Página sobre com linha do tempo da trajetória
✔️ Página 404 personalizada
✔️ Layout responsivo (mobile e desktop) com menu hamburger
✔️ Metatags de SEO e Open Graph em todas as páginas

## ➕ Como adicionar um novo projeto

Basta acrescentar um objeto em `json/projetos.json` — nenhuma alteração no código é
necessária. Os campos usados são:

| Campo              | Obrigatório | Descrição                                        |
| ------------------ | ----------- | ------------------------------------------------ |
| `id`               | sim         | Número único, usado na URL `/projeto/<id>`        |
| `titulo`           | sim         | Nome do projeto                                   |
| `texto`            | sim         | Resumo de uma linha, exibido no cartão            |
| `descricao`        | sim         | Texto completo da página de detalhe               |
| `tecnologias`      | sim         | Lista de tecnologias — alimenta os filtros        |
| `capa`             | sim         | Imagem estática do cartão                         |
| `tipo`             | não         | Front-end, Back-end ou Full-stack                 |
| `ano`              | não         | Ano do projeto                                    |
| `destaque`         | não         | `true` coloca o projeto na home                   |
| `destaques`        | não         | Lista de pontos exibida na página de detalhe      |
| `gif`              | não         | Animação exibida ao passar o mouse no cartão      |
| `video`            | não         | Demonstração em vídeo na página de detalhe        |
| `link`             | não         | URL do projeto no ar (`#` se não houver)          |
| `link-repositorio` | não         | URL do repositório (`#` se não houver)            |

## 🚀 Como rodar localmente

```bash
# Clone este repositório
git clone https://github.com/marcelloprado/portfolio-python.git
cd portfolio-python

# Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate      # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Execute o servidor Flask
python app.py
```

O site fica disponível em `http://127.0.0.1:5000`.

## 📬 Contato

📧 E-mail: marcellopradomuller@gmail.com
