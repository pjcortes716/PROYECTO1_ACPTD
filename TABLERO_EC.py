import dash
from dash import dcc  # dash core components
from dash import html # dash html components
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
#importamos las librerias para la red bayesiana
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
#importamos los datos ya limpios de heart_desease
heart_desease=pd.read_csv("datos_para_red")
#construimos la red, con los nodos:
modelo=BayesianNetwork([('E','A'),('E','H'),('C','EC'),('S','EC'),('T','EC'),('A','EC'),
                        ('H','EC'),('EC','RE'),('EC','HR'),('EC','P'),('EC','AI'),('EC','SER'),
                        ('EC','F'),('EC','D'),('S','D')])
#entrenamos la red con los datos cargados
modelo.fit(data=heart_desease,estimator=MaximumLikelihoodEstimator)
#verificamos el modelo
print(modelo.check_model())




#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#server = app.server

#app.layout = html.Div([
#    dcc.Graph(id='graph-with-slider'),
    #dcc.Slider(
    #    id='year-slider',
    #    min=df['year'].min(),
    #    max=df['year'].max(),
    #   value=df['year'].min(),
    #    marks={str(year): str(year) for year in df['year'].unique()},
    #    step=None
    #)
#    dcc.Dropdown(df.country.unique(), 'Afghanistan', id='dropdown'),
#    dcc.Graph(id='graph-gdp')
#])


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


#if __name__ == '__main__':
#    app.run_server(debug=True)
