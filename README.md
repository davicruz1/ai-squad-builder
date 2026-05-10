# 🤖 AI Squad Builder

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-FF4B4B.svg)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-F9AB00.svg)

Uma ferramenta Full-Stack para alocação inteligente de recursos humanos em projetos de tecnologia. Este sistema cruza os requisitos de uma vaga com um banco de talentos, utilizando **Inteligência Artificial (Busca Semântica)** para entender o contexto das habilidades e **Pesquisa Operacional (Programação Linear)** para otimizar o custo-benefício do time selecionado.

## 🧠 Como a Inteligência Funciona?

Diferente de sistemas baseados em busca exata de palavras (Lexical Search/TF-IDF), este projeto utiliza **NLP (Processamento de Linguagem Natural)**:
1. **Embeddings Semânticos:** Utiliza o modelo `all-MiniLM-L6-v2` (via Hugging Face `sentence-transformers`) para converter requisitos e habilidades em vetores matemáticos, compreendendo que "GCP" e "Google Cloud", por exemplo, possuem o mesmo contexto.
2. **Otimização Matemática:** Utiliza a biblioteca `PuLP` para resolver um problema da mochila (Knapsack Problem) adaptado, garantindo que o algoritmo retorne o melhor time possível (maior score de afinidade de IA) que caiba estritamente dentro do orçamento e do número de vagas estipulado.

## 🏗️ Arquitetura do Sistema

O projeto adota o padrão de separação de responsabilidades (Frontend/Backend):
* **Motor de IA (`app/engine.py`):** Processamento de dados (Pandas), Inferência de NLP e Solver de Otimização.
* **Backend API (`app/api.py`):** Uma API RESTful assíncrona construída com **FastAPI** e validada com **Pydantic**.
* **Frontend Web (`frontend.py`):** Interface interativa desenvolvida em **Streamlit**, permitindo que usuários não-técnicos interajam com o modelo de IA.

## 📂 Estrutura de Diretórios

```text
ai-squad-builder/
│
├── data/
│   └── devs.csv           # Banco de talentos (mock)
│
├── app/
│   ├── __init__.py
│   ├── engine.py          # Lógica central de IA e Otimização
│   └── api.py             # Rotas do FastAPI
│
├── frontend.py            # Interface visual do Streamlit
├── requirements.txt       # Dependências do projeto
└── README.md              # Documentação
```


## 🚀 Como Executar Localmente

### 1. Clonar e Configurar o Ambiente
Abra o terminal na pasta onde deseja salvar o projeto e execute:

```bash
git clone [https://github.com/davicruz1/ai-squad-builder.git](https://github.com/davicruz1/ai-squad-builder.git)
cd ai-squad-builder
python3 -m venv venv
source venv/bin/activate
```
### 2. Instalar as Dependências
*Nota: O projeto foi otimizado para rodar a IA apenas utilizando CPU, garantindo acessibilidade e rapidez na instalação.*

```bash
pip install -r requirements.txt
```

###3. Iniciar o Backend (FastAPI)
Em um terminal (com o venv ativado), inicie o servidor da API. Na primeira execução, o sistema fará o download do modelo NLP (~80MB).

```bash
uvicorn app.api:app --reload
```

A API estará rodando em http://127.0.0.1:8000. Você pode acessar a documentação interativa (Swagger UI) em http://127.0.0.1:8000/docs.

###4. Iniciar o Frontend (Streamlit)
Abra um segundo terminal, ative o venv novamente e inicie a interface:

```bash
streamlit run frontend.py
```
O painel abrirá automaticamente no seu navegador no endereço http://localhost:8501.

