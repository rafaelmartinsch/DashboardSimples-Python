import streamlit as st #bibioteca que serve para constuir a pagina e servidor para visualização de dados.
import pandas as pd #manipulação de dados
import plotly.express as px #biblioteca para plotar os gráficos

# Dashboard Com uma visão mensal
#faturamento por unidade… 
# tipo de produto mais vendido, contribuição por filial,
#Desempenho das forma de pagamento…
#Como estão as avaliações das filiais? 

#definir o layout da pagina
st.set_page_config(layout="wide")

#leitura do arquivo, converter a conluna de data e ordernar por data
df = pd.read_csv("data.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df=df.sort_values("Date")


#Criar um array para o filtro por mês 
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês", df["Month"].unique())
#filtra no conjunto de dados os meses do array
df_filtered = df[df["Month"] == month]

#definir o layout or grid 
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

#criar gráfico de barradas total por cidade e inserir na coluna 1
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)


fig_prod = px.bar(df_filtered, x="Date", y="Product line", 
                  color="City", title="Faturamento por tipo de produto",
                  orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)


city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total",
                   title="Faturamento por filial")
col3.plotly_chart(fig_city, use_container_width=True)

#grafico de pizza 
fig_kind = px.pie(df_filtered, values="Total", names="Payment",
                   title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_kind, use_container_width=True)

#use_container_width serve para garantir que o gráfico se limite dentro do card.
city_total = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(df_filtered, y="Rating", x="City",
                   title="Avaliação")
col5.plotly_chart(fig_rating, use_container_width=True)

df