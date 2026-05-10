import streamlit as st
import requests

st.set_page_config(page_title="AI Squad Builder", page_icon="🤖", layout="centered")

st.title("🤖 AI Squad Builder")
st.markdown("Alocação inteligente de times utilizando NLP e Otimização Matemática.")

with st.form("squad_form"):
    st.subheader("Parâmetros do Projeto")
    descricao = st.text_area("Requisitos da Vaga:", placeholder="Ex: Desenvolvedor frontend com experiência em React")
    
    col1, col2 = st.columns(2)
    with col1:
        vagas = st.number_input("Número de Vagas", min_value=1, max_value=10, value=1)
    with col2:
        orcamento = st.number_input("Orçamento Máximo (R$/h)", min_value=10.0, max_value=1000.0, value=100.0, step=10.0)
        
    submit_button = st.form_submit_button(label="Processar Otimização")

if submit_button:
    if not descricao:
        st.warning("A descrição dos requisitos é obrigatória.")
    else:
        with st.spinner("Computando similaridades e resolvendo modelo de otimização..."):
            payload = {
                "descricao": descricao,
                "vagas": int(vagas),
                "orcamento": float(orcamento)
            }
            
            try:
                # Comunicação com a API Backend local
                response = requests.post("http://127.0.0.1:8000/montar-squad", json=payload)
                
                if response.status_code == 200:
                    dados = response.json()
                    st.success("Squad otimizado com sucesso.")
                    
                    st.metric(label="Custo Estimado do Time", value=f"R$ {dados['custo_total_squad']:.2f}/h")
                    st.subheader("Profissionais Selecionados:")
                    
                    for membro in dados['membros']:
                        with st.expander(f"👤 {membro['nome']} - R$ {membro['custo_hora']}/h"):
                            st.write(f"**Stack:** {membro['habilidades']}")
                            st.write(f"**Match Semântico (IA):** {membro['score_afinidade'] * 100:.1f}%")
                            
                else:
                    erro = response.json().get("detail", "Falha na requisição.")
                    st.error(f"Erro no processamento: {erro}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Erro de conexão (ConnectionError): Verifique se o backend FastAPI está ativo.")