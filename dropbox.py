import streamlit as st 
import pandas as pd
import numpy as np 
import sys
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO


st.title('Data Processing')
st.write('Importe aqui os dados da sua tabéla')

df = st.file_uploader('Upload a CSV/ txt/ excel  ile')
if df is not None:
    tabela= pd.read_csv(df, sep = "\t", encoding= 'UTF-16', skiprows= 2, skipfooter= 3, dtype='float', decimal=',')
    tabela.fillna(0, inplace=True)
# tirando a coluna de Temperatura 
    tabela.drop(['Temperature(¡C)'], axis= 'columns', inplace = True)

    st.write(tabela)



#subistituindo NaN por zero 
#tabela.dropna(axis=1, how='all', inplace= True)


    controle_p = st.multiselect('Select the cels that are positive controls', options =[i for i in tabela.columns if i != 'Wavelength'], max_selections= 2)
    controle_n = st.multiselect('Select the cels that are negative controls', options =[i for i in tabela.columns if i not in [*controle_p, 'Wavelength']], max_selections= 2)

#media dos controles
    if controle_p and controle_n is not None:
        tabela['media_controle_p'] = (tabela[controle_p[0]] + tabela[controle_p[1]])/2
        tabela['media_controle_n'] = (tabela[controle_n[0]] + tabela[controle_n[1]])/2

        tabela['Ratio_controle'] = tabela['media_controle_p'] - tabela['media_controle_n']  

        maior_pico_ratio_controle = tabela.loc[(tabela['Wavelength'].values > 630) & (tabela['Wavelength'].values < 680)]['Ratio_controle'].max()




        resultado = []
        for i in tabela.columns:
            if i not in [*controle_n, *controle_p, 'Wavelength']:
                tabela['Ratio_tratamento'] = tabela[i] - tabela['media_controle_n']
                maior_pico_ratio_tratamento = tabela.loc[(tabela['Wavelength'].values > 630) & (tabela['Wavelength'].values < 680)]['Ratio_tratamento'].max()
                if maior_pico_ratio_tratamento > maior_pico_ratio_controle: 
                    resultado.append((i , 'Positivo'))

                else:
                    resultado.append((i, 'Negativo'))


#st.write(resultado)
            
#with open("/home/pedro/Dropbox/pedro_programas/mestrado/data_processing/html_roberto.html", 'r') as html:
#    html_data = html.read()



#st.components.v1.html(html_data, scrolling=True, height=500)



        placa_df = pd.DataFrame(index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                            columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
        index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

        for z in index:
            for e in columns:
                b = z+e
                placa_df.loc[z, e] = b

#fazendo o dicionario para fazer o replace das céluilas do data frame
        pos = []
        res = []
        for l in resultado:
            pos.append(l[0])
            res.append(l[1])

        dicionario = dict(zip(pos, res))
    

#print(pos)

#st.write(dicionario)

        for z in index:
            for e in columns:
                b = z+e
                if b in pos:
                    placa_df.loc[z, e] = dicionario[b]
                else:
                    placa_df.loc[z, e] = 'Controle'
            

        def color_cells(val):
            if  val == 'Positivo':
                color = 'white'
                return 'background-color: red'; 'color: %s' % color
            elif val == 'Controle':
                color = 'white'
                return 'background-color: blue'; 'color: %s' % color
            else:
                color = 'white'
                return 'background-color: green'; 'color: %s' % color


    
        styled_df = placa_df.style.applymap(color_cells)

        st.write('Segue a baixo o resultado do teste as células verdes são os resultados negativos:')
        st.dataframe(styled_df)
##mudando a cor das letras do dataframe pra ficar mais bonit
   
        coluna_gráfico = st.multiselect('select the cells u wanna plot', options =[i for i in tabela.columns if i not in [*controle_p, 'Wavelength']], max_selections= 2)

# definindo a figura no matplot lib
        if coluna_gráfico is not None:

            fig, ax = plt.subplots(figsize = (25,15))
#adicionanfo as linhas na figura em branco (ax)
#definir eixo x e y; definir qual é a tabela no data; label = legenda; linewidth = grossura da linha; ax = ax quer dizer que o eixo da coluna esta no eixo da figura 
            sns.lineplot(x = 'Wavelength',
                         y = 'media_controle_p',
                         data = tabela,
                         label = 'Controle Media Positivo',
                         linewidth = 5.5,
                         ax = ax)
            sns.lineplot(x = 'Wavelength',
                         y = 'media_controle_n',
                         label = 'Controle Media Negativo',
                         linewidth = 5.5,
                         data = tabela,
                         ax = ax)
            sns.lineplot(x = 'Wavelength',
                         y = coluna_gráfico[0],
                         label = f'{coluna_gráfico[0]} Media',
                         linewidth = 5.5,
                         data = tabela,
                         ax = ax)
            sns.lineplot(x = 'Wavelength',
                         y = coluna_gráfico[1],
                         label = f'{coluna_gráfico[1]} Media',
                         linewidth = 5.5,
                         data = tabela,
                         ax = ax)

            ax.set_ylim(-10, 600)

            ax.set_xlabel("Wavelength",fontsize=30)
            ax.set_ylabel("",fontsize=20)

            ax.legend(fontsize = 25)

            plt.tick_params(labelsize=25)

            
            st.pyplot(fig)
        else:
            pass
    else:
        pass    
else:
    pass 

# Inserir em cada célula, a letra e nmumero : A1, A2, A3, ... H12 ####feito
# Fazer o replace da lista "resultado" no dataframe criado acima
# Estiliazar o dataframer conforme https://docs.streamlit.io/develop/api-reference/data/st.column_config/st.column_config.listcolumn
# Colorir o Dataframe conforme st.dataframe(df.style.highlight_max(axis=0))