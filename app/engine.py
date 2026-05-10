import pandas as pd
import pulp
import os
from sentence_transformers import SentenceTransformer, util

# Carrega o modelo de embeddings globalmente para otimizar o tempo de inferência da API
modelo_ia = SentenceTransformer('all-MiniLM-L6-v2')

def montar_squad_ia(descricao_projeto: str, vagas: int, orcamento_maximo: float) -> dict:
    """
    Avalia o banco de talentos e retorna a combinação ideal de profissionais,
    maximizando a similaridade semântica (NLP) e respeitando as restrições lineares.
    """
    caminho_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_csv = os.path.join(caminho_base, 'data', 'devs.csv')
    
    try:
        df = pd.read_csv(caminho_csv)
    except FileNotFoundError:
        return {"status": "Erro", "mensagem": "Base de dados não encontrada."}

    # Geração de embeddings e cálculo de similaridade de cosseno
    habilidades_devs = df['Habilidades'].tolist()
    embeddings_devs = modelo_ia.encode(habilidades_devs)
    embedding_projeto = modelo_ia.encode([descricao_projeto])
    
    similaridades = util.cos_sim(embedding_projeto, embeddings_devs)[0].tolist()
    df['Score_IA'] = similaridades

    # Modelagem do problema de otimização linear
    problema = pulp.LpProblem("Otimizacao_Squad", pulp.LpMaximize)
    escolhas = pulp.LpVariable.dicts("Dev", df.index, cat='Binary')

    # Função objetivo: maximizar o score total de afinidade
    problema += pulp.lpSum([df['Score_IA'][i] * escolhas[i] for i in df.index])
    
    # Restrições do modelo
    problema += pulp.lpSum([escolhas[i] for i in df.index]) == vagas
    problema += pulp.lpSum([df['Custo_Hora'][i] * escolhas[i] for i in df.index]) <= orcamento_maximo

    # Resolução silenciosa do solver
    problema.solve(pulp.PULP_CBC_CMD(msg=False))

    if pulp.LpStatus[problema.status] != 'Optimal':
        return {
            "status": "Erro",
            "mensagem": "Impossível atender aos requisitos com as restrições fornecidas."
        }

    # Estruturação da resposta (Payload)
    squad_selecionado = []
    custo_total = 0

    for i in df.index:
        if escolhas[i].varValue == 1.0:
            squad_selecionado.append({
                "nome": df['Nome'][i],
                "habilidades": df['Habilidades'][i],
                "score_afinidade": float(df['Score_IA'][i]),
                "custo_hora": float(df['Custo_Hora'][i])
            })
            custo_total += float(df['Custo_Hora'][i])

    return {
        "status": "Sucesso",
        "vagas_solicitadas": vagas,
        "orcamento_maximo": float(orcamento_maximo),
        "custo_total_squad": custo_total,
        "membros": squad_selecionado
    }