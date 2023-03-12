import dash
from dash import dcc  # dash core components
from dash import html # dash html components
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
#importamos las librerias para la red bayesiana
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
#importamos los datos ya limpios de heart_desease
heart_desease=pd.read_csv("datos_para_red")
#construimos la red, con los nodos:
modelo=BayesianNetwork([('E','A'),('E','H'),('C','EC'),('S','EC'),('T','EC'),('A','EC'),
                        ('H','EC'),('EC','RE'),('EC','HR'),('EC','P'),('EC','AI'),('EC','SER'),
                        ('EC','F'),('EC','D'),('S','D')])
#entrenamos la red con los datos cargados
modelo.fit(data=heart_desease,estimator=MaximumLikelihoodEstimator)
#creamos el elemento infer
infer = VariableElimination(modelo)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#creamos el objeto dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Heart Disease'
server = app.server

app.layout = html.Div([
    html.Div(children=[
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
        #html.Label('Calcular probabilidad de enfermedad cardiaca'),
        html.Div(id="probabilidad")
        

        
        




    ],style={'width': '49%', 'display': 'inline-block'}),
    html.Div(children=[html.Br(), html.Button('Calcular probabilidad de enfermedad cardiaca', id='calcular', n_clicks=0,style={'font-size': '12px', 
    'width': '1985px', 'display': 'inline-block', 
    'margin-bottom': '10px', 'margin-right': '5px', 'height':'37px', 'verticalAlign': 'top'})])
   
])


@app.callback(
    Output('probabilidad', 'children'),
    [Input('calcular','n_clicks'),
    Input('edad','value'),
    Input('sexo','value'),
    Input('colesterol','value'),
    Input('diabetes','value'),
    Input('presion','value'),
    Input('dolor_pecho','value'),
    Input('angina_inducida','value'),
    Input('talasemia','value'),
    Input('ST_depresion','value'),
    Input('electro_card','value'),
    Input('max_h_rate','value'),
    Input('pendiente','value'),
    Input('fluor','value'),
   ])
def estimar_enfermedad_card(n_clicks,edad,sexo,colesterol,diabetes,presion,dolor_pecho,angina_inducida,talasemia,
ST_depresion,electro_card,max_h_rate,pendiente,fluor):
    if n_clicks==0:#inicializa el mensaje en vacio
        return "Ingrese la informacion del paciente en las casillas y de clic en el boton de calcular"
    else:
        evidencia={}#creamos un diccionario vacio para la evidencia
        #verificamos el valor de la edad
        if edad=="Mayor de 60 años":
            evidencia["E"]=1
        elif edad=="Menor de 60 años":
            evidencia["E"]=0
        #verificamos el sexo
        if sexo=="Hombre":
            evidencia["S"]=1
        elif sexo=="Mujer":
            evidencia["S"]=0
        #verificamos colesterol:
        if colesterol=="Si":
            evidencia["C"]=1
        elif colesterol=="No":
            evidencia["C"]=0
        #verificamos la diabetes:
        if diabetes=="Si":
            evidencia["A"]=1
        elif diabetes=="No":
            evidencia["A"]=0
        #verificamos la presion arterial:
        if presion=="Si":
            evidencia["P"]=1
        elif presion=="No":
            evidencia["P"]=0
        #verificamos el dolor de pecho:
        if dolor_pecho=="Si":
            evidencia["D"]=1
        elif dolor_pecho=="No":
            evidencia["D"]=0
        #verificamos la angina inducida
        if angina_inducida=="Si":
            evidencia["AI"]=1
        elif angina_inducida=="No":
            evidencia["AI"]=0
        #verificamos la talasemia
        if talasemia=="Sufre Talasemia":
            evidencia["T"]=1
        elif talasemia=="No sufre talasemia":
            evidencia["T"]=0
        #verificamos st_depresion
        if ST_depresion=="Depresion de pico de ejercicio normal":
            evidencia["SER"]=0
        elif ST_depresion=="Depresion de pico de ejercicio >1mm":
            evidencia["SER"]=1
        #verificamos la forma de la onda del electrocardiograma:
        if electro_card=="Si":
            evidencia.setdefault("RE", 0)
            #evidencia['RE']==0
        elif electro_card=="No":
            evidencia.setdefault("RE", 1)
            #evidencia['RE']==1
        #verificamos la maxima frecuencia cardiaca
        if max_h_rate=="Si":
            evidencia["HR"]=0
        elif max_h_rate=="No":
            evidencia["HR"]=1
        #verificamos la pendiente del electro:
        if pendiente=="Si":
            evidencia["P"]=0
        elif pendiente=="No":
            evidencia["P"]=1
        #verificmos el examen de fluoresencia:
        if fluor=="Si":
            evidencia["F"]=1
        elif fluor=="No":
            evidencia["F"]=0
        #hacemos la inferencia de la probabilidad
        caso_a = infer.query(["EC"] , evidence =evidencia)
        print(evidencia)
        print(caso_a)
        respuesta="La probabilidad de que el paciente tenga una enfermedad cardiaca es de {}".format(caso_a.values[1])
        return respuesta
        






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
