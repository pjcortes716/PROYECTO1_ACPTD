import dash
from dash import dcc  # dash core components
from dash import html # dash html components
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from scipy.stats import t
import math
import os
import plotly.graph_objs as go
#importamos las librerias para la red bayesiana
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
#importamos los datos ya limpios de heart_desease
heart_desease=pd.read_csv(str(os.getcwd())+"/"+"datos_para_red")
#construimos la red, con los nodos:
modelo=BayesianNetwork([('E','A'),('E','H'),('C','EC'),('S','EC'),('T','EC'),('A','EC'),
                        ('H','EC'),('EC','RE'),('EC','HR'),('EC','P'),('EC','AI'),('EC','SER'),
                        ('EC','F'),('EC','D'),('S','D')])

#Datos
heart_disease=pd.read_csv(str(os.getcwd())+"/"+"datos_para_grafica")
datosMaximaFrecuenciaCardiaca=heart_disease.loc[:,["ENFERMEDAD_CARD","MAX_HEART_R"]]
datosMaximaFrecuenciaCardiacaSano=datosMaximaFrecuenciaCardiaca[["ENFERMEDAD_CARD","MAX_HEART_R"]][datosMaximaFrecuenciaCardiaca["ENFERMEDAD_CARD"]=="Sano"]
datosMaximaFrecuenciaCardiacaEnfermo=datosMaximaFrecuenciaCardiaca[["ENFERMEDAD_CARD","MAX_HEART_R"]][datosMaximaFrecuenciaCardiaca["ENFERMEDAD_CARD"]=="Enfermo"]
datosColesterol=heart_disease.loc[:,["ENFERMEDAD_CARD","COLESTEROL"]]
datosColesterolSano=datosColesterol[["ENFERMEDAD_CARD","COLESTEROL"]][datosColesterol["ENFERMEDAD_CARD"]=="Sano"]
datosColesterolEnfermo=datosColesterol[["ENFERMEDAD_CARD","COLESTEROL"]][datosColesterol["ENFERMEDAD_CARD"]=="Enfermo"]
datosPresionSanguinea=heart_disease.loc[:,["ENFERMEDAD_CARD","PRESION_SAN"]]
datosPresionSanguineaSano=datosPresionSanguinea[["ENFERMEDAD_CARD","PRESION_SAN"]][datosPresionSanguinea["ENFERMEDAD_CARD"]=="Sano"]
datosPresionSanguineaEnfermo=datosPresionSanguinea[["ENFERMEDAD_CARD","PRESION_SAN"]][datosPresionSanguinea["ENFERMEDAD_CARD"]=="Enfermo"]
datosDolorPecho=heart_disease.loc[:,["ENFERMEDAD_CARD","DOLOR_PECHO"]]
datosDolorPechoSano=datosDolorPecho[["ENFERMEDAD_CARD","DOLOR_PECHO"]][datosDolorPecho["ENFERMEDAD_CARD"]=="Sano"]
datosDolorPechoEnfermo=datosDolorPecho[["ENFERMEDAD_CARD","DOLOR_PECHO"]][datosDolorPecho["ENFERMEDAD_CARD"]=="Enfermo"]
#Estadisticas
mediaMuestralFreqSano=datosMaximaFrecuenciaCardiacaSano["MAX_HEART_R"].mean()
mediaMuestralFreqEnfermo=datosMaximaFrecuenciaCardiacaEnfermo["MAX_HEART_R"].mean()
mediaMuestralColesterolSano=datosColesterolSano["COLESTEROL"].mean()
mediaMuestralColesterolEnfermo=datosColesterolEnfermo["COLESTEROL"].mean()
dfFreqSano=datosMaximaFrecuenciaCardiacaSano["MAX_HEART_R"].count()-1
dfFreqEnfermo=datosMaximaFrecuenciaCardiacaEnfermo["MAX_HEART_R"].count()-1
dfColesterolSano=datosColesterolSano["COLESTEROL"].count()-1
dfColesterolEnfermo=datosColesterolEnfermo["COLESTEROL"].count()-1
tFreqSano=t.ppf(1-0.0001/2,dfFreqSano,loc=0, scale=1)
tFreqEnfermo=t.ppf(1-0.0001/2,dfFreqEnfermo,loc=0, scale=1)
tColesterolSano=t.ppf(1-0.0001/2,dfColesterolSano,loc=0, scale=1)
tColesterolEnfermo=t.ppf(1-0.0001/2,dfColesterolEnfermo,loc=0, scale=1)
varianzaMuestralFreqSano=datosMaximaFrecuenciaCardiacaSano["MAX_HEART_R"].var()
varianzaMuestralFreqEnfermo=datosMaximaFrecuenciaCardiacaEnfermo["MAX_HEART_R"].var()
varianzaMuestralColesterolSano=datosColesterolSano["COLESTEROL"].var()
varianzaMuestralColesterolEnfermo=datosColesterolEnfermo["COLESTEROL"].var()
mediaMuestralPresionSano=datosPresionSanguineaSano["PRESION_SAN"].mean()
mediaMuestralPresionEnfermo=datosPresionSanguineaEnfermo["PRESION_SAN"].mean()
dfPresionSano=datosPresionSanguineaSano["PRESION_SAN"].count()-1
dfPresionEnfermo=datosPresionSanguineaEnfermo["PRESION_SAN"].count()-1
tPresionSano=t.ppf(1-0.0001/2,dfPresionSano,loc=0, scale=1)
tPresionEnfermo=t.ppf(1-0.0001/2,dfPresionEnfermo,loc=0, scale=1)
varianzaMuestralPresionSano=datosPresionSanguineaSano["PRESION_SAN"].var()
varianzaMuestralPresionEnfermo=datosPresionSanguineaEnfermo["PRESION_SAN"].var()
mediaMuestralDolorPechoSano=(datosDolorPechoSano["DOLOR_PECHO"].astype(int)).mean()
mediaMuestralDolorPechoEnfermo=(datosDolorPechoEnfermo["DOLOR_PECHO"].astype(int)).mean()
dfDolorPechoSano=datosDolorPechoSano["DOLOR_PECHO"].count()-1
dfDolorPechoEnfermo=datosDolorPechoEnfermo["DOLOR_PECHO"].count()-1
tDolorPechoSano=t.ppf(1-0.0001/2,dfDolorPechoSano,loc=0, scale=1)
tDolorPechoEnfermo=t.ppf(1-0.0001/2,dfDolorPechoEnfermo,loc=0, scale=1)
varianzaMuestralDolorPechoSano=(datosDolorPechoSano["DOLOR_PECHO"].astype(int)).var()
varianzaMuestralDolorPechoEnfermo=(datosDolorPechoEnfermo["DOLOR_PECHO"].astype(int)).var()
#Intervalos
upperICFreqSano=mediaMuestralFreqSano+tFreqSano*math.sqrt(varianzaMuestralFreqSano/(dfFreqSano+1))
lowerICFreqSano=mediaMuestralFreqSano-tFreqSano*math.sqrt(varianzaMuestralFreqSano/(dfFreqSano+1))
upperICFreqEnfermo=mediaMuestralFreqEnfermo+tFreqEnfermo*math.sqrt(varianzaMuestralFreqEnfermo/(dfFreqEnfermo+1))
lowerICFreqEnfermo=mediaMuestralFreqEnfermo-tFreqEnfermo*math.sqrt(varianzaMuestralFreqEnfermo/(dfFreqEnfermo+1))
upperICColesterolSano=mediaMuestralColesterolSano+tColesterolSano*math.sqrt(varianzaMuestralColesterolSano/(dfColesterolSano+1))
lowerICColesterolSano=mediaMuestralColesterolSano-tColesterolSano*math.sqrt(varianzaMuestralColesterolSano/(dfColesterolSano+1))
upperICColesterolEnfermo=mediaMuestralColesterolEnfermo+tColesterolEnfermo*math.sqrt(varianzaMuestralColesterolEnfermo/(dfColesterolEnfermo+1))
lowerICColesterolEnfermo=mediaMuestralColesterolEnfermo-tColesterolEnfermo*math.sqrt(varianzaMuestralColesterolEnfermo/(dfColesterolEnfermo+1))
upperICPresionSano=mediaMuestralPresionSano+tPresionSano*math.sqrt(varianzaMuestralPresionSano/(dfPresionSano+1))
lowerICPresionSano=mediaMuestralPresionSano-tPresionSano*math.sqrt(varianzaMuestralPresionSano/(dfPresionSano+1))
upperICPresionEnfermo=mediaMuestralPresionEnfermo+tPresionEnfermo*math.sqrt(varianzaMuestralPresionEnfermo/(dfPresionEnfermo+1))
lowerICPresionEnfermo=mediaMuestralPresionEnfermo-tPresionEnfermo*math.sqrt(varianzaMuestralPresionEnfermo/(dfPresionEnfermo+1))
upperICDolorPechoSano=math.floor(mediaMuestralDolorPechoSano+tDolorPechoSano*math.sqrt(varianzaMuestralDolorPechoSano/(dfPresionSano+1)))
lowerICDolorPechoSano=math.floor(mediaMuestralDolorPechoSano-tDolorPechoSano*math.sqrt(varianzaMuestralDolorPechoSano/(dfPresionSano+1)))
upperICDolorPechoEnfermo=round(mediaMuestralDolorPechoEnfermo+tDolorPechoEnfermo*math.sqrt(varianzaMuestralDolorPechoEnfermo/(dfPresionEnfermo+1)))
lowerICDolorPechoEnfermo=math.floor(mediaMuestralDolorPechoEnfermo-tDolorPechoEnfermo*math.sqrt(varianzaMuestralDolorPechoEnfermo/(dfPresionEnfermo+1)))

#entrenamos la red con los datos cargados
modelo.fit(data=heart_desease,estimator=MaximumLikelihoodEstimator)



#creamos el objeto dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Heart Disease'
server = app.server

app.layout = html.Div([
    html.Div(children=[
    html.H1("Gráficas"),
    html.Label("Máxima frecuencia cardíaca"),
    dcc.Input(placeholder="Valor sin unidades",
              type="number",
              value=0,
              id="MFCGraficas"
    ),
    html.Br(),
    html.Label("Colesterol"),
    dcc.Input(placeholder="Valor sin unidades",
              type="number",
              value=0,
              id="ColesterolGraficas"
    ),
    html.Br(),
    html.Label("Presión sanguinea"),
    dcc.Input(placeholder="Valor sin unidades",
              type="number",
              value=0,
              id="PresionGraficas"
    ),
    html.Br(),
    html.Label(['Tipo de dolor en el pecho:', html.Br(),'1: Angina tipica',html.Br(), '2: Angina no tipica',html.Br(), '3: dolor no anginal',html.Br(),'4: asintomatico']),
    dcc.Input(placeholder="Valor sin unidades",
              type="number",
              value=0,
              id="TipoDolorGraficas"
    ),
    html.Div([dcc.Graph(id="graficaMFCyColesterol"),dcc.Graph(id="graficaPresionyColesterol"),dcc.Graph(id="graficaTipoDeDoloryPresion")]),
    ]
    ),
    
    html.Div(children=[html.Br(), html.Button('Generar Gráficas', id='generar', n_clicks=0,style={'font-size': '12px', 
    'width': '1985px', 'display': 'inline-block', 
    'margin-bottom': '10px', 'margin-right': '5px', 'height':'37px', 'verticalAlign': 'top'})]),
    html.Br(),
    html.Div(children=[
        html.H1("Red"),
        html.Label('Edad'),
        dcc.Dropdown(["Mayor de 60 años","Menor de 60 años"],id="edad"),
        html.Br(),
        html.Label('Sexo'),
        dcc.Dropdown(["Hombre","Mujer"],id="sexo"),
        html.Br(),
        html.Label('¿El nivel de colesterol total es superior a 200 mg/dl?'),
        dcc.Dropdown(["Si","No"],id="colesterol"),
        html.Br(),
        html.Label('¿El paciente ha sido diagnosticado diabetico?'),
        dcc.Dropdown(["Si","No"],id="diabetes"),
        html.Br(),
        html.Label('¿El paciente ha sido hipertenso (presion sanguinea mayor a 130 mm de Hg)?'),
        dcc.Dropdown(["Si","No"],id="presion"),
        html.Br(),
        html.Label('¿El paciente presenta dolor en el pecho?'),
        dcc.Dropdown(["Si","No"],id="dolor_pecho"),
        html.Br(),
        html.Label('¿En el examen de esfuerzo, el paciente presenta angina inducida?'),
        dcc.Dropdown(["Si","No"],id="angina_inducida")
        



        
    ],style={'width': '49%', 'display': 'inline-block'}),
    html.Div(children=[
        html.Label('¿Talasemia?'),
        dcc.Dropdown(["Sufre Talasemia","No sufre talasemia"],id="talasemia"),
        html.Br(),
        html.Label('Ingrese aqui el resultado de la depresion en el pico de la curva del electrocardiograma'),
        dcc.Dropdown(["Depresion de pico de ejercicio normal","Depresion de pico de ejercicio >1mm"],id="ST_depresion"),
        html.Br(),
        html.Label('La forma de la onda del electrocardiograma es normal'),
        dcc.Dropdown(["Si","No"],id="electro_card"),
        html.Br(),
        html.Label('¿La maxima frecuencia cardiaca es menor a 150?'),
        dcc.Dropdown(["Si","No"],id="max_h_rate"),
        html.Br(),
        html.Label('¿La pendiente de pico de ejercicio es creciente?'),
        dcc.Dropdown(["Si","No"],id="pendiente"),
        html.Br(),
        html.Label('¿El examen de fluoroscopia muestra algun vaso sanguineo resaltado?'),
        dcc.Dropdown(["Si","No"],id="fluor"),
        html.Br(),
        html.Label('Calcular probabilidad de enfermedad cardiaca'),
        

        
        




    ],style={'width': '49%', 'display': 'inline-block'}),
    html.Div(children=[html.Br(), html.Button('Calcular probabilidad de enfermedad cardiaca', id='calcular', n_clicks=0,style={'font-size': '12px', 
    'width': '1985px', 'display': 'inline-block', 
    'margin-bottom': '10px', 'margin-right': '5px', 'height':'37px', 'verticalAlign': 'top'})])
   
])
@app.callback(
    [Output("graficaMFCyColesterol","figure"), Output("graficaPresionyColesterol","figure"), Output("graficaTipoDeDoloryPresion","figure")],
    [Input("generar","n_clicks")],
    [State("MFCGraficas", "value"),State("ColesterolGraficas", "value"),State("PresionGraficas", "value"),State("TipoDolorGraficas", "value")]
)
def actualizarGraficaMFCyColesterol(n_clicks, MFC, Colesterol, Presion, TipoDolor):
    if n_clicks==0:
        scatterSano1=go.Scatter(x=datosColesterolSano["COLESTEROL"], y=datosMaximaFrecuenciaCardiacaSano["MAX_HEART_R"], mode="markers", marker=dict(color="blue"), name="Saludables")
        scatterEnfermo1=go.Scatter(x=datosColesterolEnfermo["COLESTEROL"], y=datosMaximaFrecuenciaCardiacaEnfermo["MAX_HEART_R"], mode="markers", marker=dict(color="red"), name= "Enfermos")
        layoutGraph1=go.Layout(title="Scatter de la Máxima Frecuencia Cardiaca y Colesterol", xaxis=dict(title="Colesterol [añadir unidades]"), yaxis=dict(title="Maxima Frecuencia Cardiaca [añadir unidades]"))
        rectSano1=go.Scatter(x=[lowerICColesterolSano, lowerICColesterolSano, upperICColesterolSano, upperICColesterolSano, lowerICColesterolSano], y=[lowerICFreqSano, upperICFreqSano, upperICFreqSano, lowerICFreqSano, lowerICFreqSano], fill="toself", name= "Valor Esperado Saludables")
        rectEnfermo1=go.Scatter(x=[lowerICColesterolEnfermo, lowerICColesterolEnfermo, upperICColesterolEnfermo, upperICColesterolEnfermo, lowerICColesterolEnfermo], y=[lowerICFreqEnfermo, upperICFreqEnfermo, upperICFreqEnfermo, lowerICFreqEnfermo, lowerICFreqEnfermo], fill="toself", name="Valor Esperado Enfermos")
        graph1=go.Figure(data=[scatterSano1, scatterEnfermo1, rectSano1, rectEnfermo1], layout=layoutGraph1)
        scatterSano2=go.Scatter(x=datosColesterolSano["COLESTEROL"], y=datosPresionSanguineaSano["PRESION_SAN"], mode="markers", marker=dict(color="blue"), name="Saludables")
        scatterEnfermo2=go.Scatter(x=datosColesterolEnfermo["COLESTEROL"], y=datosPresionSanguineaSano["PRESION_SAN"], mode="markers", marker=dict(color="red"), name= "Enfermos")
        layoutGraph2=go.Layout(title="Scatter de la Presión Sanguinea y Colesterol", xaxis=dict(title="Colesterol [añadir unidades]"), yaxis=dict(title="Presión Sanguinea [añadir unidades]"))
        rectSano2=go.Scatter(x=[lowerICColesterolSano, lowerICColesterolSano, upperICColesterolSano, upperICColesterolSano, lowerICColesterolSano], y=[lowerICPresionSano, upperICPresionSano, upperICPresionSano, lowerICPresionSano, lowerICPresionSano], fill="toself", name= "Valor Esperado Saludables")
        rectEnfermo2=go.Scatter(x=[lowerICColesterolEnfermo, lowerICColesterolEnfermo, upperICColesterolEnfermo, upperICColesterolEnfermo, lowerICColesterolEnfermo], y=[lowerICPresionEnfermo, upperICPresionEnfermo, upperICPresionEnfermo, lowerICPresionEnfermo, lowerICPresionEnfermo], fill="toself", name="Valor Esperado Enfermos")
        graph2=go.Figure(data=[scatterSano2, scatterEnfermo2, rectSano2, rectEnfermo2], layout=layoutGraph2)
        scatterSano3=go.Scatter(x=datosPresionSanguineaSano["PRESION_SAN"], y=datosDolorPechoSano["DOLOR_PECHO"], mode="markers", marker=dict(color="blue"), name="Saludables")
        scatterEnfermo3=go.Scatter(x=datosPresionSanguineaEnfermo["PRESION_SAN"], y=datosDolorPechoEnfermo["DOLOR_PECHO"], mode="markers", marker=dict(color="red"), name= "Enfermos")
        layoutGraph3=go.Layout(title="Scatter de la Presión Sanguinea y el tipo de Dolor de Pecho", xaxis=dict(title="Presion sanguinea [añadir unidades]"), yaxis=dict(title="Tipo de dolor de pecho [añadir unidades]"))
        rectSano3=go.Scatter(x=[lowerICPresionSano, lowerICPresionSano, upperICPresionSano, upperICPresionSano, lowerICPresionSano], y=[lowerICDolorPechoSano, upperICDolorPechoSano, upperICDolorPechoSano, lowerICDolorPechoSano, lowerICDolorPechoSano], fill="toself", name= "Valor Esperado Saludables")
        rectEnfermo3=go.Scatter(x=[lowerICPresionEnfermo, lowerICPresionEnfermo, upperICPresionEnfermo, upperICPresionEnfermo, lowerICPresionEnfermo], y=[lowerICDolorPechoEnfermo, upperICDolorPechoEnfermo, upperICDolorPechoEnfermo, lowerICDolorPechoEnfermo, lowerICDolorPechoEnfermo], fill="toself", name="Valor Esperado Enfermos")
        graph3=go.Figure(data=[scatterSano3, scatterEnfermo3, rectSano3, rectEnfermo3], layout=layoutGraph3)
        
    else:
        scatterSano1=go.Scatter(x=datosColesterolSano["COLESTEROL"], y=datosMaximaFrecuenciaCardiacaSano["MAX_HEART_R"], mode="markers", marker=dict(color="blue"), name="Saludables")
        scatterEnfermo1=go.Scatter(x=datosColesterolEnfermo["COLESTEROL"], y=datosMaximaFrecuenciaCardiacaEnfermo["MAX_HEART_R"], mode="markers", marker=dict(color="red"), name= "Enfermos")
        layoutGraph1=go.Layout(title="Scatter de la Máxima Frecuencia Cardiaca y Colesterol", xaxis=dict(title="Colesterol [añadir unidades]"), yaxis=dict(title="Maxima Frecuencia Cardiaca [añadir unidades]"))
        rectSano1=go.Scatter(x=[lowerICColesterolSano, lowerICColesterolSano, upperICColesterolSano, upperICColesterolSano, lowerICColesterolSano], y=[lowerICFreqSano, upperICFreqSano, upperICFreqSano, lowerICFreqSano, lowerICFreqSano], fill="toself", name= "Valor Esperado Saludables")
        rectEnfermo1=go.Scatter(x=[lowerICColesterolEnfermo, lowerICColesterolEnfermo, upperICColesterolEnfermo, upperICColesterolEnfermo, lowerICColesterolEnfermo], y=[lowerICFreqEnfermo, upperICFreqEnfermo, upperICFreqEnfermo, lowerICFreqEnfermo, lowerICFreqEnfermo], fill="toself", name="Valor Esperado Enfermos")
        puntoPaciente1=go.Scatter(x=[Colesterol],y=[MFC], mode="markers", marker=dict(symbol="x",color="black",size=10), name="Paciente Actual")
        graph1=go.Figure(data=[scatterSano1, scatterEnfermo1, puntoPaciente1, rectSano1, rectEnfermo1], layout=layoutGraph1)
        scatterSano2=go.Scatter(x=datosColesterolSano["COLESTEROL"], y=datosPresionSanguineaSano["PRESION_SAN"], mode="markers", marker=dict(color="blue"), name="Saludables")
        scatterEnfermo2=go.Scatter(x=datosColesterolEnfermo["COLESTEROL"], y=datosPresionSanguineaSano["PRESION_SAN"], mode="markers", marker=dict(color="red"), name= "Enfermos")
        layoutGraph2=go.Layout(title="Scatter de la Presión Sanguinea y Colesterol", xaxis=dict(title="Colesterol [añadir unidades]"), yaxis=dict(title="Presión Sanguinea [añadir unidades]"))
        rectSano2=go.Scatter(x=[lowerICColesterolSano, lowerICColesterolSano, upperICColesterolSano, upperICColesterolSano, lowerICColesterolSano], y=[lowerICPresionSano, upperICPresionSano, upperICPresionSano, lowerICPresionSano, lowerICPresionSano], fill="toself", name= "Valor Esperado Saludables")
        rectEnfermo2=go.Scatter(x=[lowerICColesterolEnfermo, lowerICColesterolEnfermo, upperICColesterolEnfermo, upperICColesterolEnfermo, lowerICColesterolEnfermo], y=[lowerICPresionEnfermo, upperICPresionEnfermo, upperICPresionEnfermo, lowerICPresionEnfermo, lowerICPresionEnfermo], fill="toself", name="Valor Esperado Enfermos")
        puntoPaciente2=go.Scatter(x=[Colesterol],y=[Presion], mode="markers", marker=dict(symbol="x",color="black",size=10), name="Paciente Actual")
        graph2=go.Figure(data=[scatterSano2, scatterEnfermo2,puntoPaciente2 ,rectSano2, rectEnfermo2], layout=layoutGraph2)
        scatterSano3=go.Scatter(x=datosPresionSanguineaSano["PRESION_SAN"], y=datosDolorPechoSano["DOLOR_PECHO"], mode="markers", marker=dict(color="blue"), name="Saludables")
        scatterEnfermo3=go.Scatter(x=datosPresionSanguineaEnfermo["PRESION_SAN"], y=datosDolorPechoEnfermo["DOLOR_PECHO"], mode="markers", marker=dict(color="red"), name= "Enfermos")
        layoutGraph3=go.Layout(title="Scatter de la Presión Sanguinea y el tipo de Dolor de Pecho", xaxis=dict(title="Presion sanguinea [añadir unidades]"), yaxis=dict(title="Tipo de dolor de pecho [añadir unidades]"))
        rectSano3=go.Scatter(x=[lowerICPresionSano, lowerICPresionSano, upperICPresionSano, upperICPresionSano, lowerICPresionSano], y=[lowerICDolorPechoSano, upperICDolorPechoSano, upperICDolorPechoSano, lowerICDolorPechoSano, lowerICDolorPechoSano], fill="toself", name= "Valor Esperado Saludables")
        rectEnfermo3=go.Scatter(x=[lowerICPresionEnfermo, lowerICPresionEnfermo, upperICPresionEnfermo, upperICPresionEnfermo, lowerICPresionEnfermo], y=[lowerICDolorPechoEnfermo, upperICDolorPechoEnfermo, upperICDolorPechoEnfermo, lowerICDolorPechoEnfermo, lowerICDolorPechoEnfermo], fill="toself", name="Valor Esperado Enfermos")
        puntoPaciente3=go.Scatter(x=[Presion],y=[TipoDolor], mode="markers", marker=dict(symbol="x",color="black",size=10), name="Paciente Actual")
        graph3=go.Figure(data=[scatterSano3, scatterEnfermo3,puntoPaciente3, rectSano3, rectEnfermo3], layout=layoutGraph3)
    return graph1,graph2,graph3


        
    
    


#@app.callback(
#    Output('graph-with-slider', 'figure'),
#    [Input('dropdown', 'value')])
#def update_figure(country):
#    afg=df[df["country"]==country]
#    fig = px.line(afg, x="year", y="pop", title='Population in '+country,labels={"year":"year","pop":"population (Millions of people)"})
#    return fig






    #filtered_df = df[df.year == selected_year]

    #fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp", 
    #                 size="pop", color="continent", hover_name="country", 
    #                 log_x=True, size_max=55,
     #                labels={
      #               "pop": "Population",
       #              "gdpPercap": "GDP per cápita",
        #             "lifeExp": "Life Expectancy",
         ##           },
           #          title="Life expectancy vs. GDP per cápita across the years")

    #fig.update_layout(transition_duration=500)
#    return fig

#@app.callback(Output('graph-gdp', 'figure'),
#    [Input('dropdown', 'value')])
#def second_figure(country):
#    afg=df[df["country"]==country]
#    fig=px.line(afg, x="year", y="gdpPercap", title='GDP per capita of '+country,labels={"year":"year","gdpPercap":"Gross domestic product per capita"})
#    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
