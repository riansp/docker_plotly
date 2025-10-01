## Check out the dashboard here! 
    -> http://127.0.0.1:8050/ if running in local
    -> click the open port and fill your port so click OK, if error copy the url and open in new broswer


import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px


# df = pd.read_csv(r"C:\Users\rianp\Downloads\LuxuryLoanPortfolio.csv")
# path = os.path.join("data", "LuxuryLoanPortfolio.csv")
df = pd.read_csv("data/LuxuryLoanPortfolio.csv")
df["funded_date"] = pd.to_datetime(df["funded_date"], errors="coerce")
df = df.dropna(subset=["funded_date"])
df["funded_year"] = df["funded_date"].dt.year


def df_summary(df):
    summary = { "Total Loan Balance": df["loan balance"].sum(),
                "Total Funded Amount" : df["funded_amount"].sum(),
                "Avg Interest Rate" : df["interest rate"].mean(),
                "Total Borrowers": df["borrower_id"].nunique() if "borrower_id" in df.columns else len(df)
               }
    return summary

def bar_chart(df):
    return df.groupby("purpose", as_index=False)["funded_amount"].sum()

def pie_chart(df):
    return df["BUILDING CLASS CATEGORY"].value_counts().reset_index().rename(
        columns={"index": "Category", "BUILDING CLASS CATEGORY": "Count"}
        )

def pie_chart(df):
    return df["BUILDING CLASS CATEGORY"].value_counts().reset_index().rename(
        columns={
            "BUILDING CLASS CATEGORY": "Category", 
            "count": "Count"  
        }
    )
    
def line_chart(df):
    monthly_balance = (
        df.groupby(df["funded_date"].dt.to_period("M"))["loan balance"].sum().reset_index()
    )
    monthly_balance["funded_date"] = monthly_balance["funded_date"].astype(str)
    return monthly_balance

def make_card(title, value, decimals=0):
    fmt = f"{{:,.{decimals}f}}"
    return html.Div([
        html.H4(title, style={"marginBottom": "5px", "color": "#888"}),
        html.H2(fmt.format(value), style={"margin": 0, "color": "#333"})
    ], style={
        "padding": "20px",
        "margin": "10px",
        "backgroundColor": "white",
        "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
        "flex": "1",
        "textAlign": "center"
    })


app = dash.Dash(__name__)
app.title = "Luxury Loan Dashboard"

app.layout = html.Div([
    html.H1("Luxury Loan Portfolio Dashboard", style={"textAlign": "center"}),
    html.Div(id="summary_cards", style={"display": "flex", "flexWarp": "warp"}),

    html.Div([
        html.Div([
            html.Label("Year: "),
            dcc.Dropdown(
                id="year_filter",
                options=[{"label": y, "value": y} for y in sorted(df["funded_year"].unique())],
                value=None,
                multi=False,
                placeholder="Select Year"
            ),
        ], style={"width": "45%", "display": "inline-block"}),

        html.Div([
            html.Label("City: "),
            dcc.Dropdown(
                id="city_filter",
                options=[{"label": c, "value": c} for c in sorted(df["CITY"].unique())],
                value=None,
                multi=False,
                placeholder="Select City"              
            ),
        ], style={"width": "45%", "display": "inline-block", "marginLeft": "5%"}),
        ], style={"marginBottom": "20px", "marginTop": "20px"}),

    html.Div([
        dcc.Graph(id="line_chart", style={"width": "55%", "display": "inline-block", "height" : "400px"}),
        dcc.Graph(id="donut_chart", style={"width": "60%", "display": "inline-block", "height" : "400px", "marginLeft": "2%"}),
    ], style={"display": "flex", "justifyContent": "space-between"}),


    dcc.Graph(id="bar_chart", style={"width": "100%", "height" : "400px"}),


], style={"fontFamily": "Arial", "backgroundColor": "#E0E4E7", "padding": "20px", "maxWidth": "1600px", "height": "900px", "margin": "0 auto"})


@app.callback(
    [Output("summary_cards", "children"),
     Output("line_chart", "figure"),
     Output("donut_chart", "figure"),
     Output("bar_chart", "figure")],
    [Input("year_filter", "value"),
    Input("city_filter", "value")]
)

def dashboard(selected_year, selected_city):
    dff = df.copy()

    if selected_year:
        dff = dff[dff["funded_year"] == selected_year]
    if selected_city:
        dff = dff[dff["CITY"] == selected_city]
    
    summary = df_summary(dff)
    cards = [
        make_card("Total Loan Balance", summary["Total Loan Balance"]),
        make_card("Total Funded Amount", summary["Total Funded Amount"]),
        make_card("Avg Interest Rate", summary["Avg Interest Rate"], decimals=3),
        make_card("Total Borrowers", summary["Total Borrowers"]),
        ]
    

    ## chart 1 : loan balance trend
    chart1 = px.line(line_chart(dff), x="funded_date", y="loan balance",
                title="Loan Balance Trend Over Time")
    chart1.update_traces(hovertemplate="%{x}: %{y:,.0f}")

    ## chart 2 : building class category
    chart2 = px.pie(pie_chart(dff), names="Category", values="Count",
              title="Building Class Category Distribution",
              hole=0.4)
    chart2.update_traces(hovertemplate="%{label}: %{value:, }")

    ## chart 3 : funded amount by purpose
    chart3 = px.bar(bar_chart(dff), x="purpose", y="funded_amount",
              title="Total Funded Amount by Purpose")
    chart3.update_traces(hovertemplate="%{x}: %{y:,.0f}")

    return cards, chart1, chart2, chart3


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8050, debug=True)


