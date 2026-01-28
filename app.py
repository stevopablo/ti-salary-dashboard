import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Análise de Dados',
    page_icon='📊',
    layout='wide'
)

# Carregar dados
df = pd.read_csv('dados-aula-final.csv')

# Filtros
st.sidebar.header("Filtros")

anos = st.sidebar.multiselect(
    'Selecione os anos',
    df['ano'].unique(),
    default=df['ano'].unique()
)

senioridades = st.sidebar.multiselect(
    'Selecione as senioridades',
    df['senioridade'].unique(),
    default=df['senioridade'].unique()
)

contratos = st.sidebar.multiselect(
    'Selecione os contratos',
    df['contrato'].unique(),
    default=df['contrato'].unique()
)

tamanhos = st.sidebar.multiselect(
    'Selecione os tamanhos da empresa',
    df['tamanho_empresa'].unique(),
    default=df['tamanho_empresa'].unique()
)

# Filtragem
df_filtrado = df[
    (df['ano'].isin(anos)) &
    (df['senioridade'].isin(senioridades)) &
    (df['contrato'].isin(contratos)) &
    (df['tamanho_empresa'].isin(tamanhos))
]


st.title("📊 Dashboard de Análise de Salários em TI")
st.subheader("Principais análises")

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_usuarios = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]
else:
    salario_medio = salario_maximo = total_usuarios = 0
    cargo_mais_frequente = "Nenhum dado"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_usuarios:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---")
st.subheader("Gráficos")


col_graf1, col_graf2 = st.columns(2)

# gráfico top 10 cargos
with col_graf1:
    if not df_filtrado.empty:
        top_cargos = (
            df_filtrado
            .groupby('cargo')['usd']
            .mean()
            .nlargest(10)
            .sort_values()
            .reset_index()
        )

        fig = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title='Top 10 cargos por salário médio (USD)'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Sem dados para o gráfico.")

# Gráfico tipo de contrato
with col_graf2:
    if not df_filtrado.empty:
        remoto = df_filtrado['remoto'].value_counts().reset_index()
        remoto.columns = ['tipo_trabalho', 'quantidade']

        fig = px.pie(
            remoto,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5
        )
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Sem dados para o gráfico.")


st.subheader("🌍 Salário médio por cargo e país")

if not df_filtrado.empty:
    cargo_padrao = [df_filtrado['cargo'].mode()[0]]
else:
    cargo_padrao = []

cargo_selecionado = st.multiselect(
    'Cargos',
    df['cargo'].unique(),
    default=cargo_padrao
)

if not df_filtrado.empty and cargo_selecionado:
    df_ds = df_filtrado[df_filtrado['cargo'].isin(cargo_selecionado)]

    media_pais = (
        df_ds
        .groupby('residencia_iso3')['usd']
        .mean()
        .reset_index()
    )

    fig = px.choropleth(
        media_pais,
        locations='residencia_iso3',
        color='usd',
        color_continuous_scale='RdYlGn',
        labels={'usd': 'Salário médio (USD)'},
        title='Salário médio por país'
    )

    fig.update_layout(height=800, title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Selecione pelo menos um cargo.")

st.subheader("Evolução salarial ao longo dos anos")

if not df_filtrado.empty:
    salario_ano = df_filtrado.groupby('ano')['usd'].mean().reset_index()

    fig = px.line(
        salario_ano,
        x='ano',
        y='usd',
        markers=True,
        title='Evolução do salário médio ao longo dos anos'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Sem dados para o gráfico de evolução salarial.")
    
    
    
st.subheader(" Salário médio por tipo de contrato")

if not df_filtrado.empty:
    salario_contrato = (
            df_filtrado
            .groupby('contrato')
            ['usd']
            .mean()
            .reset_index()
            )

    fig = px.bar(
        salario_contrato,
        x='contrato',
        y='usd',
        title='Salário médio por tipo de contrato'
    )
    st.plotly_chart(fig, use_container_width=True)




st.subheader(" Top 10 países com maiores salários médios")

if not df_filtrado.empty:
    top_paises = (
        df_filtrado
        .groupby('residencia_iso3')['usd']
        .mean()
        .nlargest(10)
        .reset_index()
    )

    fig = px.bar(
        top_paises,
        x='usd',
        y='residencia_iso3',
        orientation='h',
        color='residencia_iso3',
        title='Top 10 países por salário médio',
    )
    st.plotly_chart(fig, use_container_width=True)