import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from random import randint

#Gráficos relacionados a um país
def covid_19_country(country='Brazil'):

    #cria os datasets já organizados    
    confirmed, deaths, recovered = treatment(country)
    
    #cria a figura para plotar o grafico com 3 linhas e uma coluna
    fig = make_subplots(rows=3, cols=1,
                        subplot_titles=("Confirmed", "Deaths", "recovered"))
    
    #plota cada um dos gráficos
    fig.add_trace(go.Scatter(x=list(confirmed.index), 
                       y=list(confirmed.values),
                       mode='lines+markers',
                       line=dict(color='rgb(255,0,0)'),
                       name='Confirmed'), row=1,col=1)
    fig.add_trace(go.Scatter(x=list(deaths.index), 
                       y=list(deaths.values),
                       mode='lines+markers',
                       line=dict(color='rgb(79,79,79)'),
                       name='Deaths'), row=2,col=1)
    fig.add_trace(go.Scatter(x=list(recovered.index), 
                       y=list(recovered.values),
                       mode='lines+markers',
                       line=dict(color='rgb(154,205,50)'),
                       name='recovered'), row=3,col=1)
    #salva a imagem
    fig.write_html('fig{}.html'.format(country), auto_open=True)
          
#compara pela data varios países 
def covid_world(countrys=['Brazil','Japan','China','Italy','US']):
    
    
    #cria a imagem para ser plotada com 3 linhas e 1 coluna
    fig = make_subplots(rows=3, cols=1,
                        subplot_titles=("Confirmed", "Deaths", "recovered"))
    
    #cria a repetição na lista de países
    for c in countrys:
        
        #gera um codigo rgb unico para cada repetição
        red = randint(0, 255)
        green = randint(0, 255)
        blue = randint(0, 255)
        rgb = 'rgb({},{},{})'.format(red,green,blue)
        
        #cria os datasets já organizados    
        confirmed, deaths, recovered = treatment(c)
        
        #adiciona o grafico de confirmados do país a imagem
        fig.add_trace(go.Scatter(x=list(confirmed.index), 
                           y=list(confirmed.values),
                           mode='lines+markers',
                           line=dict(color=rgb),
                           name=c), row=1,col=1)
        #adiciona o grafico de fatais do país a imagem
        fig.add_trace(go.Scatter(x=list(deaths.index), 
                           y=list(deaths.values),
                           mode='lines+markers',
                           line=dict(color=rgb),
                           name=c), row=2,col=1)
        #adiciona o grafico de recuperados do país a imagem
        fig.add_trace(go.Scatter(x=list(recovered.index), 
                           y=list(recovered.values),
                           mode='lines+markers',
                           line=dict(color=rgb),
                           name=c), row=3,col=1)
    #salva a imagem
    fig.write_html('fig_world.html', auto_open=True)
    
    
#compara os dias de infecção de varios países   
def covid_19_comparation(countrys=['Brazil','Japan','China','Italy','US']): 
    
    #cria a imagem para ser plotada com 3 linhas e 1 coluna
    fig = make_subplots(rows=3, cols=1,
                        subplot_titles=("Confirmed", "Deaths", "recovered"))
    
    #cria a repetição na lista de países
    for c in countrys:
        
        #gera um codigo rgb unico para cada repetição
        red = randint(0, 255)
        green = randint(0, 255)
        blue = randint(0, 255)
        rgb = 'rgb({},{},{})'.format(red,green,blue)
        
        #cria os datasets já organizados    
        confirmed, deaths, recovered = treatment(c)
        
        #Chama a função para listar apenas quando começar a aparecer casos confirmados e começar a contagem de dias
        c_data, dc = lists(confirmed)
        d_data, dd = lists(deaths)
        r_data, dr = lists(recovered)
        
        #adiciona o grafico de confirmados do país a imagem
        fig.add_trace(go.Scatter(x=dc, 
                           y=c_data,
                           mode='lines+markers',
                           line=dict(color=rgb),
                           name=c), row=1,col=1)
        #adiciona o grafico de fatais do país a imagem
        fig.add_trace(go.Scatter(x=dd, 
                           y=d_data,
                           mode='lines+markers',
                           line=dict(color=rgb),
                           name=c), row=2,col=1)
        #adiciona o grafico de recuperados do país a imagem
        fig.add_trace(go.Scatter(x=dr, 
                           y=r_data,
                           mode='lines+markers',
                           line=dict(color=rgb),
                           name=c), row=3,col=1)
    #coloca o gráfico em base logarítmica
    fig.update_layout(xaxis_type="log", yaxis_type="log")
    #salva a imagem
    fig.write_html('fig_comparation.html', auto_open=True)
        
#cria lista com numero de casos e dia desde a primeira confirmação do caso   
def lists(df):
    
    #cria a lista para o dataset
    data = []
    
    #laço de repetição nos dados
    for x in df.index:
        
        #verifica se já tem casos confirmados
        if int(df[x]) > 0:
            
            #adiciona o valor a lista de casos
            data.append(int(df[x]))
    
    #cria uma lista com o intervalo de dias desde o primeiro caso
    days = list(range(0,len(data)))
    
    return data,days

def treatment(country):
    
    #abre os arquivos de dataset
    df1 = pd.read_csv('dat/time_series_2019-ncov-Confirmed.csv',delimiter=',')
    df2 = pd.read_csv('dat/time_series_2019-ncov-Deaths.csv',delimiter=',')
    df3 = pd.read_csv('dat/time_series_2019-ncov-Recovered.csv',delimiter=',')
    
    #filtra o país selecionado dos dataset
    confirmed = df1[df1['Country/Region']==country]
    deaths = df2[df2['Country/Region']==country]
    recovered = df3[df3['Country/Region']==country]
    
    #remove as colunas que não precisamos
    confirmed = confirmed.drop(columns=['Province/State','Country/Region','Lat','Long'])
    deaths = deaths.drop(columns=['Province/State','Country/Region','Lat','Long'])
    recovered = recovered.drop(columns=['Province/State','Country/Region','Lat','Long'])
    
    #faz um somatorio das colunas, caso tenha mais de uma linha
    confirmed = confirmed.sum()
    deaths = deaths.sum()
    recovered = recovered.sum()
    
    return confirmed, deaths, recovered
    
    
    


    

