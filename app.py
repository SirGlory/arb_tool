import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import dash_auth
import requests
import pandas as pd
from luno_python.client import Client

luno_bid_price = 0
luno_ask_price = 0
valr_bid_price = 0
valr_ask_price = 0

USERNAME_PASSWORD_PAIRS = [['ovex','tom']]



# Data Fetch___________________LUNO_______________________
def getData1():
    global luno_bid_price
    c = Client(api_key_id='k2dmhxm8fxc3c', api_key_secret='r-dpNkeG6YMWNYtDh1WBOGQKhe6yBMj9rCNP0QrlAuQ')
    try:
        res1 = c.get_order_book(pair='XBTZAR')
    except Exception as e:
        print(e)

    df1 = pd.DataFrame.from_dict(res1["bids"])
    df1 = df1[:41]
    df1 = df1.apply(pd.to_numeric)
    df1['cumVol'] = df1['volume'].cumsum()
    df1['percent'] = abs((df1['price'] - df1['price'].iloc[0]) / df1['price'].iloc[0] * 100)
    df1 = df1[['price', 'percent', 'cumVol', 'volume'][::-1]]
    df1 = df1.round(5)
    df1['percent'] = df1['percent'].round(3)
    luno_bid_price = df1['price'].iloc[0]
    return df1.to_dict('records')

def getData2():
    global luno_ask_price
    c = Client(api_key_id='k2dmhxm8fxc3c', api_key_secret='r-dpNkeG6YMWNYtDh1WBOGQKhe6yBMj9rCNP0QrlAuQ')
    try:
      res2 = c.get_order_book(pair='XBTZAR')
    except Exception as e:
      print(e)

    df2 = pd.DataFrame.from_dict(res2["asks"])
    df2 = df2[:41]
    df2 = df2.apply(pd.to_numeric)
    df2['cumVol'] = df2['volume'].cumsum()
    df2['percent'] = abs((df2['price']-df2['price'].iloc[0]) / df2['price'].iloc[0]*100)
    df2 = df2[['price','percent','cumVol','volume']]
    df2 = df2.round(5)
    df2['percent'] = df2['percent'].round(3)
    luno_ask_price = df2['price'].iloc[0]
    return df2.to_dict('records')


# Data Fetch_____________________VALR_______________________
def getData3():
    global valr_bid_price
    url = 'https://api.valr.com/v1/public/BTCZAR/orderbook'
    res3 = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    data3 = res3.json()
    df3 = pd.DataFrame.from_dict(data3["Bids"])

    df3 = df3[['orderCount','quantity','price']]
    df3 = df3.apply(pd.to_numeric)
    df3['cumVol'] = df3['quantity'].cumsum()
    df3['percent'] = abs((df3['price']-df3['price'].iloc[0]) / df3['price'].iloc[0]*100)
    df3 = df3[['orderCount','quantity','cumVol','percent','price']]
    df3 = df3.round(5)
    df3['percent'] = df3['percent'].round(3)
    valr_bid_price = df3['price'].iloc[0]
    return df3.to_dict('records')

def getData4():
    global valr_ask_price
    url = 'https://api.valr.com/v1/public/BTCZAR/orderbook'
    res4 = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    data4 = res4.json()
    df4 = pd.DataFrame.from_dict(data4["Asks"])
    df4 = df4[['orderCount','quantity','price']]
    df4 = df4.apply(pd.to_numeric)
    df4['cumVol'] = df4['quantity'].cumsum()
    df4['percent'] = abs((df4['price']-df4['price'].iloc[0]) / df4['price'].iloc[0]*100)
    df4 = df4[['orderCount','quantity','cumVol','percent','price'][::-1]]
    df4 = df4.round(5)
    df4['percent'] = df4['percent'].round(3)
    valr_ask_price = df4['price'].iloc[0]
    return df4.to_dict('records')

# print("-------")
# print("Bids")
# print(df3.head(40))
# print("-------")
# print("Datatypes")
# print(df3.dtypes)
# print("-------")
# print("Asks")
# print(df4.head(40))
# print("-------")
# print("Datatypes")
# print(df4.dtypes)
# print("-------")

tblcols1=[{'name': 'Vol', 'id': 'volume'},
         {'name': 'cumVol', 'id': 'cumVol'},
         {'name': '%', 'id': 'percent'},
         {'name': 'Price', 'id': 'price'}]

tblcols3=[{'name': 'Count', 'id': 'orderCount'},
         {'name': 'Vol', 'id': 'quantity'},
         {'name': 'cumVol', 'id': 'cumVol'},
         {'name': '%', 'id': 'percent'},
         {'name': 'Price', 'id': 'price'}]



# Launch App_____________________________________________________
app = dash.Dash()
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
app.server

# App Layout_____________________________________________________
app.layout = html.Div([
            dcc.Interval(
                id='interval-component',
                interval=1000,  # 1000 milliseconds = 1 second       #<--------- Time Interval
                n_intervals=0
            ),

    # LUNO Table
            html.Div([
                html.H3("LUNO Bids", style={'text-align':'center'}),
                dash_table.DataTable(
                    id='table1',
                    columns=tblcols1,
                    data=getData1(),
                    style_table={'minWidth': '100%'},
                    style_cell={
                        # all three widths are needed
                        'minWidth': '20px', 'width': '50px', 'maxWidth': '100px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    }
                ),
            ],style={'width':'15%','display':'inline-block'}),

            html.Div([
                html.H3("LUNO_Asks", style={'text-align':'center'}),
                dash_table.DataTable(
                    id='table2',
                    columns=tblcols1[::-1],
                    data=getData2(),
                    style_table={'minWidth': '100%'},
                    style_cell={
                        # all three widths are needed
                        'minWidth': '20px', 'width': '50px', 'maxWidth': '100px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    }
                ),
            ],style={'width':'15%','display':'inline-block'}),


    # VALR Table

            html.Div([
                html.H3("VALR Bids", style={'text-align':'center'}),
                dash_table.DataTable(
                    id='table3',
                    columns=tblcols3,
                    data=getData3(),
                    style_table={'minWidth': '100%'},
                    style_cell={
                        # all three widths are needed
                        'minWidth': '20px', 'width': '50px', 'maxWidth': '100px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    }
                ),
            ], style={'width': '15%', 'display': 'inline-block', 'marginLeft': 15}),

            html.Div([
                html.H3("VALR Asks", style={'text-align':'center'}),
                dash_table.DataTable(
                    id='table4',
                    columns=tblcols3[::-1],
                    data=getData4(),
                    style_table={'minWidth': '100%'},
                    style_cell={
                        # all three widths are needed
                        'minWidth': '20px', 'width': '50px', 'maxWidth': '100px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    }
                ),
            ], style={'width': '15%', 'display': 'inline-block'}),

        # Arbitrage Stats
            html.Div([
                html.H3("Arbitrage Stats", style={'text-align':'left'}),
                html.Div([
                    html.Pre(
                        id='delta_luno_valr',
                        children='Arbitrage Spread='
                    ),
                    html.Pre(
                        id='delta_valr_luno',
                        children='Arbitrage Spread='
                    ),
                ]),
            ], style={'width': '30', 'display': 'inline-block', 'marginLeft': 15}),

    ],style={'backgroundColor':'white','margin': 10})

@app.callback(
        dash.dependencies.Output('table1','data'),
        [dash.dependencies.Input('interval-component', 'n_intervals')])
def updateTable(n):
     return getData1()

@app.callback(
        dash.dependencies.Output('table2','data'),
        [dash.dependencies.Input('interval-component', 'n_intervals')])
def updateTable(n):
     return getData2()

@app.callback(
        dash.dependencies.Output('table3','data'),
        [dash.dependencies.Input('interval-component', 'n_intervals')])
def updateTable(n):
     return getData3()

@app.callback(
        dash.dependencies.Output('table4','data'),
        [dash.dependencies.Input('interval-component', 'n_intervals')])
def updateTable(n):
     return getData4()

@app.callback(Output('delta_luno_valr', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    delta_lv = valr_ask_price - luno_bid_price
    percent_lv = delta_lv/luno_bid_price*100
    return 'Price Delta: Luno Bid to Valr Ask = R {} or {} %'.format(delta_lv,percent_lv.round(3))

@app.callback(Output('delta_valr_luno', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    delta_vl = luno_ask_price - valr_bid_price
    percent_vl = delta_vl/valr_bid_price
    return 'Price Delta: Valr Bid to Luno Ask = R {} or {} %'.format(delta_vl,percent_vl.round(3))


if __name__ == '__main__':
    app.run_server()