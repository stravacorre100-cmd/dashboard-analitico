
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table, Input, Output

# ==================================
# DASHBOARD ANALÍTICO DE VENDAS
# ==================================

app = Dash(__name__)
app.title = "Dashboard Analítico de Vendas"

# Base de dados demonstrativa
dados = [
    ["V001", "2026-01-05", "Eletrônicos", "Notebook", "Norte", 2, 6000],
    ["V002", "2026-01-12", "Roupas", "Camiseta", "Nordeste", 10, 800],
    ["V003", "2026-01-18", "Casa", "Liquidificador", "Sudeste", 4, 600],
    ["V004", "2026-02-03", "Eletrônicos", "Celular", "Sul", 3, 4500],
    ["V005", "2026-02-14", "Roupas", "Calça", "Nordeste", 5, 750],
    ["V006", "2026-02-21", "Casa", "Ventilador", "Norte", 6, 900],
    ["V007", "2026-03-02", "Eletrônicos", "Notebook", "Sudeste", 1, 3000],
    ["V008", "2026-03-11", "Roupas", "Tênis", "Sul", 4, 1200],
    ["V009", "2026-03-19", "Casa", "Micro-ondas", "Nordeste", 2, 1000],
    ["V010", "2026-04-04", "Eletrônicos", "Celular", "Norte", 5, 7500],
    ["V011", "2026-04-15", "Roupas", "Camiseta", "Sudeste", 8, 640],
    ["V012", "2026-04-24", "Casa", "Liquidificador", "Sul", 3, 450],
    ["V013", "2026-05-06", "Eletrônicos", "Notebook", "Nordeste", 2, 6000],
    ["V014", "2026-05-13", "Roupas", "Calça", "Norte", 6, 900],
    ["V015", "2026-05-22", "Casa", "Ventilador", "Sudeste", 4, 600],
    ["V016", "2026-06-07", "Eletrônicos", "Celular", "Sul", 4, 6000],
    ["V017", "2026-06-16", "Roupas", "Tênis", "Nordeste", 3, 900],
    ["V018", "2026-06-26", "Casa", "Micro-ondas", "Norte", 2, 1000],
]

colunas = [
    "Pedido", "Data", "Categoria", "Produto",
    "Região", "Quantidade", "Valor"
]

df = pd.DataFrame(dados, columns=colunas)
df["Data"] = pd.to_datetime(df["Data"])
df["Mês"] = df["Data"].dt.strftime("%Y-%m")

CORES = {
    "Eletrônicos": "#0072B2",
    "Roupas": "#E69F00",
    "Casa": "#009E73"
}

app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#F5F7FA",
        "padding": "24px",
        "color": "#253247"
    },
    children=[
        html.H1(
            "Dashboard Analítico de Vendas",
            style={"textAlign": "center", "color": "#17365D"}
        ),
        html.P(
            "Análise interativa de receita, categorias e regiões.",
            style={"textAlign": "center"}
        ),

        html.Div([
            html.Label("Filtrar por região:"),
            dcc.Dropdown(
                id="filtro-regiao",
                options=[
                    {"label": r, "value": r}
                    for r in sorted(df["Região"].unique())
                ],
                multi=True,
                placeholder="Todas as regiões"
            ),
        ], style={"maxWidth": "500px", "margin": "20px auto"}),

        html.Div(id="indicadores", style={
            "display": "flex", "gap": "16px",
            "flexWrap": "wrap", "marginBottom": "24px"
        }),

        html.Div([
            dcc.Graph(id="grafico-mensal", clear_on_unhover=True),
            dcc.Graph(id="grafico-categoria"),
            dcc.Graph(id="grafico-regiao"),
        ], style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fit, minmax(320px, 1fr))",
            "gap": "16px"
        }),

        html.H2("Detalhamento dos pedidos"),
        html.P(
            "Selecione um mês ou uma categoria nos gráficos para "
            "combinar os filtros. Limpe as seleções para voltar à visão geral."
        ),

        dash_table.DataTable(
            id="tabela-vendas",
            columns=[
                {"name": "Pedido", "id": "Pedido"},
                {"name": "Data", "id": "Data"},
                {"name": "Categoria", "id": "Categoria"},
                {"name": "Produto", "id": "Produto"},
                {"name": "Região", "id": "Região"},
                {"name": "Quantidade", "id": "Quantidade"},
                {"name": "Valor (R$)", "id": "Valor", "type": "numeric",
                 "format": {"specifier": ",.2f"}}
            ],
            data=[],
            sort_action="native",
            filter_action="native",
            page_size=8,
            style_table={"overflowX": "auto"},
            style_header={
                "backgroundColor": "#17365D",
                "color": "white",
                "fontWeight": "bold"
            },
            style_cell={
                "padding": "10px",
                "textAlign": "left",
                "backgroundColor": "white",
                "minWidth": "90px"
            },
            style_data_conditional=[
                {"if": {"row_index": "odd"},
                 "backgroundColor": "#F0F4F8"}
            ]
        )
    ]
)


def cartao(titulo, valor):
    return html.Div([
        html.P(titulo, style={"margin": "0", "color": "#52647A"}),
        html.H2(valor, style={"margin": "8px 0", "color": "#17365D"})
    ], style={
        "backgroundColor": "white",
        "padding": "18px",
        "borderRadius": "10px",
        "boxShadow": "0 2px 6px #DCE2E8",
        "flex": "1",
        "minWidth": "180px"
    })


@app.callback(
    Output("indicadores", "children"),
    Output("grafico-mensal", "figure"),
    Output("grafico-categoria", "figure"),
    Output("grafico-regiao", "figure"),
    Output("tabela-vendas", "data"),
    Input("filtro-regiao", "value"),
    Input("grafico-mensal", "selectedData"),
    Input("grafico-categoria", "selectedData"),
)
def atualizar_dashboard(regioes, selecao_mes, selecao_categoria):
    filtrado = df.copy()

    if regioes:
        filtrado = filtrado[filtrado["Região"].isin(regioes)]

    meses = []
    if selecao_mes and selecao_mes.get("points"):
        meses = list({
            p.get("x") for p in selecao_mes["points"]
            if p.get("x") is not None
        })
        if meses:
            filtrado = filtrado[filtrado["Mês"].isin(meses)]

    categorias = []
    if selecao_categoria and selecao_categoria.get("points"):
        categorias = list({
            p.get("y") for p in selecao_categoria["points"]
            if p.get("y") is not None
        })
        if categorias:
            filtrado = filtrado[filtrado["Categoria"].isin(categorias)]

    receita = filtrado["Valor"].sum()
    pedidos = len(filtrado)
    ticket = receita / pedidos if pedidos else 0

    indicadores = [
        cartao("Receita total", f"R$ {receita:,.2f}"),
        cartao("Quantidade de pedidos", str(pedidos)),
        cartao("Ticket médio", f"R$ {ticket:,.2f}")
    ]

    mensal = (
        filtrado.groupby("Mês", as_index=False)["Valor"]
        .sum().sort_values("Mês")
    )
    fig_mensal = px.line(
        mensal, x="Mês", y="Valor",
        markers=True, title="Receita mensal",
        labels={"Mês": "Mês", "Valor": "Receita (R$)"}
    )
    fig_mensal.update_traces(line_color="#0072B2")
    fig_mensal.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        dragmode="select"
    )

    por_categoria = (
        filtrado.groupby("Categoria", as_index=False)["Valor"]
        .sum().sort_values("Valor", ascending=True)
    )
    fig_categoria = px.bar(
        por_categoria, x="Valor", y="Categoria",
        orientation="h", color="Categoria",
        color_discrete_map=CORES,
        title="Receita por categoria",
        labels={"Valor": "Receita (R$)", "Categoria": "Categoria"}
    )
    fig_categoria.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False, dragmode="select"
    )

    por_regiao = (
        filtrado.groupby("Região", as_index=False)["Valor"]
        .sum().sort_values("Valor", ascending=False)
    )
    fig_regiao = px.bar(
        por_regiao, x="Região", y="Valor",
        title="Receita por região",
        labels={"Região": "Região", "Valor": "Receita (R$)"}
    )
    fig_regiao.update_traces(marker_color="#56B4E9")
    fig_regiao.update_layout(
        plot_bgcolor="white", paper_bgcolor="white"
    )

    tabela = filtrado.copy()
    tabela["Data"] = tabela["Data"].dt.strftime("%d/%m/%Y")
    tabela = tabela[
        ["Pedido", "Data", "Categoria", "Produto",
         "Região", "Quantidade", "Valor"]
    ]

    return (
        indicadores,
        fig_mensal,
        fig_categoria,
        fig_regiao,
        tabela.to_dict("records")
    )


if __name__ == "__main__":
    app.run(debug=True)
