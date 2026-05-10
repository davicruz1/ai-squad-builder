from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.engine import montar_squad_ia

class SquadRequest(BaseModel):
    descricao: str
    vagas: int
    orcamento: float

app = FastAPI(
    title="AI Squad Builder API",
    description="API REST para alocação inteligente de recursos usando NLP e Programação Linear.",
    version="1.0.0"
)

@app.get("/")
def health_check():
    """Endpoint de verificação de status (Health Check)."""
    return {"status": "Online", "mensagem": "API operacional."}

@app.post("/montar-squad")
def api_montar_squad(requisicao: SquadRequest):
    """
    Processa a requisição de montagem de squad baseada em descrição, vagas e orçamento.
    """
    resultado = montar_squad_ia(
        descricao_projeto=requisicao.descricao,
        vagas=requisicao.vagas,
        orcamento_maximo=requisicao.orcamento
    )
    
    if resultado["status"] == "Erro":
        raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    return resultado