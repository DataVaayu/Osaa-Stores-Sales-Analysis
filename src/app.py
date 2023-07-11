from dash import Dash, callback, Input, Output, dcc,html
import pandas as pd
import plotly.express as px

app = Dash("__name__")

server=app.server

osaa_storewise_analysis = pd.read_csv(r"store-wise-sales-osaa.csv")
vaayu_storewise_analysis = pd.read_csv(r"store-wise-sales-vaayu.csv")

osaa_storewise_analysis.fillna("no data",inplace=True)
vaayu_storewise_analysis.fillna("no data",inplace=True)

app.layout = html.Div(children=[

    html.Div([html.H1(children="1.1 Choose a Store and Category for Osaa",style={"textalign":"center","color":"rgb(0,0,0)"}),
             dcc.Dropdown(options=osaa_storewise_analysis.STORE.unique(),value="KOLKATA",id="dropdown-1-3"),
             dcc.Dropdown(options=osaa_storewise_analysis.CATEGORY.unique(),value="LEHANGA",id="dropdown-1-2"),             
             dcc.Graph(id="figure-1-2")]),
    
    html.Div([html.H1(children="1.2 Osaa Storewise Sales Analysis",style={"textalign":"center","color":"rgb(0,0,0)"}),
             dcc.Dropdown(options=osaa_storewise_analysis.columns,value=["STORE","Color"],id="dropdown-1",multi=True),
             dcc.Graph(id="figure-1")]),
    
   
       
])

@app.callback(
    Output("figure-1","figure"),
    Output("figure-1-2","figure"),
    
    Input("dropdown-1","value"),
    Input("dropdown-1-2","value"),
    Input("dropdown-1-3","value")
    
             
             )
def update_graph(value,value_1_2,value_1_3):
    
    #figure 1: Osaa drill down
    fig_1 = px.sunburst(osaa_storewise_analysis,path=value,height=700,width=1000)
    
    # figure 1_2: Top style codes in category
    
    data_fig_1_2 = osaa_storewise_analysis[(osaa_storewise_analysis['CATEGORY']==value_1_2) & (osaa_storewise_analysis['STORE']==value_1_3)]
    data_fig_1_2 = data_fig_1_2["Style Code"].value_counts()
    data_fig_1_2 = data_fig_1_2.reset_index()
    data_fig_1_2.rename(columns={"index":"Style Code","Style Code":"Count"},inplace=True)
    fig_1_2 = px.bar(data_fig_1_2.head(20),x="Style Code",y="Count",text="Count")
    
    #figure 2: Vaayu drill down
    
    
    return fig_1,fig_1_2

if __name__=="__main__":
    app.run_server(debug=True)
