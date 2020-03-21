import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from random import randint

#Gráficos relacionados a um país
def covid_19_country(country='Brazil',extra=0):

    #cria os datasets já organizados    
    confirmed, deaths, recovered = treatment(country)
    
    #cria a figura para plotar o grafico com 3 linhas e uma coluna
    fig = make_subplots(rows=3, cols=1,
                        subplot_titles=("Confirmed", "Deaths", "recovered"))
    #fator de aumento caso não se tenha certeza dos valores divulgados
    if extra == 1:
        for k in (1.05,1.10,1.20,1.30,1.50):
            fig.add_trace(go.Scatter(x=list(confirmed.index), 
                           y=list(confirmed.values*k),
                           mode='lines+markers',
                           name='{}'.format(k)), row=1,col=1)
    
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

#Função para extrapolar os casos    
def extrapolate(country='Brazil',plus=1,future=30):

    #cria os datasets já organizados    
    confirmed, deaths, recovered = treatment(country)
    
    #Chama a função para listar apenas quando começar a aparecer casos confirmados e começar a contagem de dias
    c_data, dc = lists(confirmed)
    d_data, dd = lists(deaths)
    r_data, dr = lists(recovered)
    
    #cria a imagem para ser plotada com 3 linhas e 1 coluna
    fig = make_subplots(rows=3, cols=1,
                        subplot_titles=("Confirmed", "Deaths", "recovered"))
        
    #adiciona o grafico de confirmados do país a imagem
    fig.add_trace(go.Scatter(x=dc, 
                           y=c_data,
                           mode='lines+markers',
                           name=country), row=1,col=1)
    #adiciona o grafico de fatais do país a imagem
    fig.add_trace(go.Scatter(x=dd, 
                           y=d_data,
                           mode='lines+markers',
                           name=country), row=2,col=1)
        #adiciona o grafico de recuperados do país a imagem
    fig.add_trace(go.Scatter(x=dr, 
                           y=r_data,
                           mode='lines+markers',
                           name=country), row=3,col=1)
    
    try:
        #Extrapola confirmados
        extrapolator_c,future_c, media = extrapoletor(c_data,dc,future,plus)
        media = round((media-1)*100)
        fig.add_trace(go.Scatter(x=future_c, 
                           y=extrapolator_c,
                           mode='lines+markers',
                           name='Confirmed {}%'.format(media)), row=1,col=1)
        #Extrapola fatais
        extrapolator_d, future_d, media = extrapoletor(d_data,dd,future,plus)
        media = round((media-1)*100)
        fig.add_trace(go.Scatter(x=future_d, 
                           y=extrapolator_d,
                           mode='lines+markers',
                           name='Deaths {}%'.format(media)), row=2,col=1)
        #Extrapola recuperados
        extrapolator_r, future_r, media = extrapoletor(r_data,dr,future,plus)
        media = round((media-1)*100)
        fig.add_trace(go.Scatter(x=future_r, 
                           y=extrapolator_r,
                           mode='lines+markers',
                           name='Recovereds {}%'.format(media)), row=3,col=1)
    except:
        print("Não tem dados suficientes ainda")
    #coloca o gráfico em base logarítmica
    fig.update_layout(xaxis_type="log", yaxis_type="log")
    #salva a imagem
    fig.write_html('fig_extrapolate.html', auto_open=True)

        
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

       
#Extrapola aumentando com a média de aumento dos casos nos ultimos 4 dias
def extrapoletor(data,days,future,plus=1):
    media = (((data[-1]/data[-2])-1) + ((data[-2]/data[-3])-1) + ((data[-3]/data[-4])-1)+ ((data[-4]/data[-5])-1))/4
    media = media * plus
    media += 1
    today = data[-1]
    extra = [today]
    for x in range(len(days)-1,len(days)+future):
        i = today*media
        extra.append(i)
        today = i
    day = list(range(len(days)-1,len(days)+future))
    return extra, day , media
        
        
        
    
    
    
    
    


    

