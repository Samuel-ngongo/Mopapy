
import streamlit as st
import pandas as pd
import numpy as np
import os
import datetime

st.set_page_config(page_title="Previsão Aviator", layout="wide")

def carregar_dados():
    if os.path.exists("historico.csv"):
        return pd.read_csv("historico.csv")
    return pd.DataFrame(columns=["Timestamp", "Valor"])

def salvar_dado(valor):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    novo_dado = pd.DataFrame([[now, valor]], columns=["Timestamp", "Valor"])
    historico = carregar_dados()
    historico = pd.concat([historico, novo_dado], ignore_index=True)
    historico.to_csv("historico.csv", index=False)

def analise_basica(df):
    if len(df) < 3:
        return "Insira mais dados para uma análise precisa.", None
    ultimos = df["Valor"].tail(10)
    media = ultimos.mean()
    tendencia = "Alta" if ultimos.iloc[-1] > media else "Baixa"
    alerta = ""
    if (ultimos > 2.5).sum() >= 3:
        alerta = "ATENÇÃO: Múltiplos voos acima de 2.5x nas últimas rodadas."
    elif ultimos.iloc[-1] < 1.5 and ultimos.iloc[-2] < 1.5:
        alerta = "Possível chance de subida. Aguarde confirmação."
    return f"Tendência atual: {tendencia}. Média: {media:.2f}.", alerta

aba = st.sidebar.radio("Menu", ["Previsões", "Histórico", "Exportar Dados", "Estratégias"])

dados = carregar_dados()

if aba == "Previsões":
    st.title("Previsão Aviator Inteligente")
    valor = st.number_input("Digite o valor da rodada (ex: 2.35):", min_value=0.01, format="%.2f")
    if st.button("Adicionar"):
        salvar_dado(valor)
        st.success("Valor salvo com sucesso.")

    st.subheader("Análise Inteligente")
    msg, alerta = analise_basica(dados)
    st.info(msg)
    if alerta:
        st.warning(alerta)

elif aba == "Histórico":
    st.title("Histórico de Rodadas")
    st.dataframe(dados.tail(50), use_container_width=True)

elif aba == "Exportar Dados":
    st.title("Exportar Histórico")
    csv = dados.to_csv(index=False).encode("utf-8")
    st.download_button("Baixar CSV", csv, "historico_aviator.csv", "text/csv")

elif aba == "Estratégias":
    st.title("Sugestões Estratégicas")
    st.markdown('''
    - **Após 2 ou mais rodadas abaixo de 1.5**, aguarde possível subida.
    - **Se aparecer 3 ou mais rodadas acima de 2.5**, a chance de queda é alta.
    - **Evite rodadas logo após um número muito alto (ex: "30x" ou mais)**.
    - **Estabeleça metas e limites para não tomar decisões por impulso.**
    ''')
    