import folium
from folium.plugins    import MarkerCluster
import numpy as np
import pandas as pd
from PIL import Image
import plotly.express as px
import streamlit as st
from streamlit_folium  import folium_static


st.set_page_config(layout='wide')

@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    
    return data

def sidebar_features(data):
    image = Image.open('image_sidebar.jpg')
    st.sidebar.image(image, use_column_width=True)
    st.sidebar.header('Feito por : Thomas Karsten')
    # Contatos
    st.sidebar.markdown("Contatos :")
    st.sidebar.markdown("- [Linkedin](https://www.linkedin.com/in/thomas-karsten/)")
    st.sidebar.markdown("- [Github](https://github.com/thomaskarsten90)")

    
    return data

def pages_sidebar(data):
    pages = st.sidebar.selectbox("Selecione a Página:",
                ("Introdução", "Visualização dos Dados", "Hipóteses de Negócio", "Conclusão"))
    
    # Pagina principal
    if pages == "Introdução":
        st.title ('Projeto de Análise de Dados')
        st.markdown('''O Objetivo deste projeto é gerar insights com base na análise exploratória dos dados da House Rocket.''')
        st.markdown('---')
        st.title('Sobre a House Rocket')
        st.markdown('''A House Rocket é uma empresa fictícia cujo o modelo de negócio é comprar imóveis abaixo do preço médio praticado no mercado e vender esses imóveis com melhores margens de lucro.''')
        st.markdown('---')
        st.title('Qual o valor em R$ gerado por este projeto?')
        st.markdown(f' - O custo total da aquisição dos imóveis sugeridos por este projeto de análise é de de R$ 4.079.586.744,00')
        st.markdown(f' - A receita total gerada com a venda de todos os imóveis sugeridos por este projeto de análise é de R$ 4.766.745.551,20')
        st.markdown(f' - O lucro total obtido com a venda de todos os imóveis sugeridos por este projeto de análise é de R$ 687.158.807,20')

    # Página Visualização dos Dados
    if pages == "Visualização dos Dados":
        st.title ('Visualização dos Dados')
        st.markdown('Ao clicar no cabeçalho de cada coluna, é possível ordenar de forma ascendente ou decrescente')
        st.write (data)

        st.title ('Visão Geral da Região')
        st.markdown('Selecione o Mapa que deseja visualizar na barra ao lado')

        # Mapa 1 
        is_check = st.sidebar.checkbox('Mostrar Mapa com Todo o Portfólio')
        if is_check:
            st.header('Portfolio')

            density_map = folium.Map(location=[data['lat'].mean(),
                                data['long'].mean()],
                                default_zoom_start=15)

            marker_cluster = MarkerCluster().add_to(density_map)
            for name, row in data.iterrows():
                    folium.Marker([row['lat'], row['long']],
                        popup= 'Vendida por: R${0} em:{1}. Características: {2} m², {3} Quartos, {4} Banheiros, Condição do Imóvel:{5}'. format(row['price'],
                                row['date'],
                                row['m²_living'],
                                row['bedrooms'],
                                row['bathrooms'],
                                row['condition_type']) ).add_to(marker_cluster)

            folium_static(density_map)

    
        #Mapa 2
        is_check3 = st.sidebar.checkbox('Mostrar Mapa com Nível do imóvel')
        if is_check3:
            st.header('Mapa de Nível dos imóveis com base no valor')
            houses = data [['id', 'lat','long','price', 'level']].copy()

            fig= px.scatter_mapbox(houses,
                                lat='lat',
                                lon='long',
                                size= 'price',
                                color='level',
                                size_max=15,
                                zoom=9)

            fig.update_layout (mapbox_style='open-street-map')
            fig.update_layout(height=600, margin={'r':0,'t':0,'l':0,'b':0})
            st.plotly_chart(fig)

        # Filtro de quantidade de Banheiros e Quartos
        f_bedrooms = st.sidebar.selectbox('Número de Quartos',
                                       sorted(set(data['bedrooms'].unique())))
        f_bathrooms = st.sidebar.selectbox('Número de Banheiro',
                                       sorted(set(data['bathrooms'].unique())))                                  
        f_floors = st.sidebar.selectbox('Pisos',
                                      sorted(set(data['floors'].unique())))
        c1,c2,c3 = st.columns(3)

        # Casas por quartos
        c1.header('Imóveis por Quarto')
        c1.markdown('Selecione a quantidade de Quartos na barra ao lado')
        df = data[data['bedrooms']<f_bedrooms]
        fig = px.histogram(df,x='bedrooms', nbins=19)
        c1.plotly_chart (fig, use_container_width=True)

        # Casas por banheiros
        c2.header('Imóveis por Banheiro')
        c2.markdown('Selecione a quantidade de Banheiros na barra ao lado')
        df = data[data['bathrooms']<f_bathrooms]
        fig = px.histogram(df,x='bathrooms', nbins=19)
        c2.plotly_chart (fig, use_container_width=True)

        # Filtro de quantidade de casas com cada andar
        c3.header('Imóveis por piso')
        c3.markdown('Selecione a quantidade de Pisos na barra ao lado')
        df = data[data['floors']<f_floors]
        fig = px.histogram(df,x='floors', nbins=19)
        c3.plotly_chart (fig, use_container_width=True)   
    
        c1,c2,c3 = st.columns(3)

        #Análise Descritiva
        num_attributes = data.select_dtypes (include=['int64', 'float64'])
        media = pd.DataFrame( num_attributes.apply(np.mean))
        mediana = pd.DataFrame( num_attributes.apply(np.median))
        std = pd.DataFrame( num_attributes.apply(np.std))
        max_= pd.DataFrame( num_attributes.apply(np.max))
        min_= pd.DataFrame( num_attributes.apply(np.min))

        df1 = pd.concat([max_,min_,media,mediana,std],axis=1).reset_index()

        df1.columns = ['Attributes','max','min','mean','median','std']

        st.header('Análise Descritiva')
        st.dataframe(df1,height=550)

    # Página Hipóteses de Negócio
    if pages == "Hipóteses de Negócio":
        # Hipótese 1
        st.markdown("<h1 style='text-align: center; color: black;'>Hipóteses de Negócio</h1>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        c1.subheader('Hipótese 1:  Imóveis com vista para a água são em média 30% mais caros')
        h1 = data[['price', 'waterfront', 'm²_lot']].groupby('waterfront').mean().reset_index()
        h1['waterfront'] = h1['waterfront'].astype(str)
        fig1 = px.bar(h1, x='waterfront', y='price', color='waterfront', labels={"waterfront": "Visão para água",
                                                                                "price": "Preço"},
                                                                                template='simple_white')

        fig1.update_layout(showlegend=False)
        c1.plotly_chart(fig1, use_container_width=True)

        h1_percentual = (h1.loc[1,'price'] / h1.loc[0,'price'] -1) * 100
        c1.markdown(f'Falso. Imóveis com vista para a água são, em média, {h1_percentual:.2f}% mais caros.')

        # Hipótese 2
        c2.subheader('Hipótese 2: Imóveis com data de construção menor que 1970 são em média 50% mais baratos')
        h2 = data[['price', 'built']].groupby('built').mean().reset_index()

        fig2 = px.bar(h2, x='built', y='price', color='built', labels={"built": "Ano de Construção",
                                                                        "price": "Preço"},
                                                                        template='simple_white')

        fig2.update_layout(showlegend=False)
        c2.plotly_chart(fig2, use_container_width=True)

        h2_percentual = (h2.loc[1,'price'] / h2.loc[0,'price'] -1) * 100
        c2.markdown(f'Falso. Imóveis com data de construção inferior a 1970 são, em média, {h2_percentual:.2f}% mais baratos.')

        # Hipótese 3
        c3, c4 = st.columns(2)

        c3.subheader('Hipótese 3: Imóveis sem porão possuem área total, em média, 50% maior do que imóveis com porão.')
        h3 = data[['basement', 'm²_lot']].groupby('basement').mean().reset_index()
        fig3 = px.bar(h3, x='basement', y='m²_lot', color='basement', labels={"basement": "Porão",
                                                                              "m²_lot": "m²"},
                                                                              template='simple_white')
        fig3.update_layout(showlegend=False)
        c3.plotly_chart(fig3, use_container_width=True)

        h3_percentual = (h3.loc[1,'m²_lot'] / h3.loc[0,'m²_lot'] -1) * 100
        c3.markdown(f'Falso. Imóveis sem porão possuem área total, em média, {h3_percentual:.2f}% maior do imóveis com porão.')

        # Hipótese 4
        c4.subheader('Hipótese 4: O crescimento do preço dos imóveis YoY (Ano a Ano) é de 10%')
        h4 = data[['price', 'year']].groupby('year').mean().reset_index()
        fig4 = px.line(h4, x='year', y='price', color_discrete_sequence=['teal'], template='simple_white',
                        labels={'year': 'Ano', 'price': 'Preço'})

        c4.plotly_chart(fig4, x='year', y='price', use_container_width=True)

        h4_percentual = (h4.loc[1,'year'] / h4.loc[0,'year'] -1) * 100
        c4.markdown(f'Falso. O crescimento do preço dos imóveis YoY (Ano a Ano) é de {h4_percentual:.2f}%.')

        # Hipótese 5
        c5, c6 = st.columns(2)

        c5.subheader('Hipótese 5: O crescimento do preço dos imóveis MoM (Mês a Mês) é de 15%.')
        h5 = data[['price', 'month']].groupby('month').sum().reset_index()
        fig5 = px.line(h5, x='month', y='price', color_discrete_sequence=['teal'], template='simple_white',
                    labels={'month': 'Mês', 'price': 'Preço'})

        c5.plotly_chart(fig5, x='month', y='price', use_container_width=True)

        h5_percentual = (h5.loc[1,'price'] / h5.loc[0,'price'] -1) * 100
        c5.markdown(f'Falso. O crescimento do preço dos imóveis MoM (Mês a Mês) é de {h5_percentual:.2f}%.')

        # Hipótese 6
        c6.subheader('Hipótese 6: Imóveis com condição BOA e REGULAR vendem mais do que imóveis com condição RUIM.')
        h6 = data[['condition_type', 'price']].groupby('condition_type').mean().reset_index()
        fig6 = px.bar(h6, x='condition_type', y='price', color='condition_type', labels={"condition_type": "Condição do Imóvel",
                                                                          "price": "Preço"},
                                                                          template='simple_white')
        fig6.update_layout(showlegend=False)
        c6.plotly_chart(fig6, use_container_width=True)

        h6_percentual1 = (h6.loc[0,'price'] / h6.loc[1,'price'] -1) * 100
        h6_percentual2 = (h6.loc[1,'price'] / h6.loc[2,'price'] -1) * 100
        c6.markdown(f'Verdadeiro, como podemos observar no gráfico, imóveis com condição BOA, vendem {h6_percentual1:.2f}% a mais do que imóveis com condição REGULAR e imóveis com condição REGULAR, vendem {h6_percentual2:.2f}% a mais do que imóveis com condição RUIM.')

        # Hipótese 7
        c7, c8 = st.columns(2)

        c7.subheader('Hipótese 7: Imóveis com vista para a água são, em média, 25% maiores.')
        h7 = data[['m²_lot', 'waterfront']].groupby('waterfront').mean().reset_index()
        fig7 = px.bar(h7, x='waterfront', y='m²_lot', color='m²_lot', labels={"waterfront": "Visão para água",
                                                                            "m²_lot": "m²"},
                                                                            template='simple_white')

        fig7.update_layout(showlegend=False)
        c7.plotly_chart(fig7, use_container_width=True)

        h7_percentual = (h7.loc[1,'m²_lot'] / h7.loc[0,'m²_lot'] -1) * 100
        c7.markdown(f'Falso. Imóveis com vista para a água são, em média, {h7_percentual:.2f}% maior do que imóveis sem vista para a água.')

        # Hipótese 8
        c8.subheader('Hipótese 8: Os imóveis no Outono são 5% mais caros do que no inverno.')
        h8 = data[['season', 'price']].groupby('season').mean().reset_index()
        fig8 = px.bar(h8, x='season', y='price', color='season', labels={"season": "Estação",
                                                                     "price": "Preço"},
                                                                     template='simple_white')
        fig8.update_layout(showlegend=False)
        c8.plotly_chart(fig8, use_container_width=True)

        h8_percentual = (h8.loc[0,'price'] / h8.loc[3,'price'] -1) * 100
        c8.markdown(f'Falso. Os imóveis no Outono são, em média, {h8_percentual:.2f}% mais caros do que no inverno.')

        # Hipótese 7
        c9, c10 = st.columns(2)

        c9.subheader('Hipótese 9: Imóveis com mais de 3 quartos vendem mais do que imóveis de 2 quartos.')
        h9 = data[['bedrooms', 'price']].groupby('bedrooms').mean().reset_index()
        fig9 = px.bar(h9, x='bedrooms', y='price', color='bedrooms', labels={"bedrooms": "Número de Quartos",
                                                                                     "price": "Preço"},
                                                                                     template='simple_white')

        fig9.update_layout(showlegend=False)
        c9.plotly_chart(fig9, use_container_width=True)

        h9_percentual = (h9.loc[1,'price'] / h9.loc[0,'price'] -1) * 100
        c9.markdown(f'Verdadeiro. Os imóveis com mais de 3 quartos, vendem {h9_percentual:.2f}% a mais do que imóveis com 2 ou menos quartos.')
   
        # Hipótese 8
        c10.subheader('Hipótese 10: Imóveis com metragem maior que 100m² vendem mais.')
        h10 = data[['footage', 'price']].groupby('footage').mean().reset_index()
        fig10 = px.bar(h10, x='footage', y='price', color='footage', labels={"footage": "Metragem",
                                                                         "price": "Preço"},
                                                                         template='simple_white')
        fig10.update_layout(showlegend=False)
        c10.plotly_chart(fig10, use_container_width=True)

        h10_percentual = (h10.loc[0,'price'] / h10.loc[1,'price'] -1) * 100
        c10.markdown(f'Verdadeiro. Os imóveis com área maior que 100m², vendem {h10_percentual:.2f}% a mais do que imóveis com área menor que 100m².')

    # Página Conclusão
    if pages == "Conclusão":
        #Questão de Negócio 1
        st.markdown("<h1 style='text-align: center; color: black;'>1 - Quais são os imóveis que a House Rocket deveria comprar e por qual preço?</h1>", unsafe_allow_html=True)
    
        st.markdown(' - O mapa a seguir mostra todos os imóveis sugeridos, ou não, para compra (É possível filtrar na barra lateral a direita).')
        st.markdown(' - O relatório foi feito com base no preço médio da região e condição do imóvel.')
        st.markdown(' - Exemplo: Imóvel com preço de venda abaixo da média de preço da região e com condição Regular ou Boa, a sugestão é comprar.')

            # Mapa
        is_check = st.checkbox('Mostrar Mapa com Status (Comprar e Não comprar)')
        if is_check:
            mapa_status = data [['id', 'lat', 'long','price', 'status']]. copy()

            fig = px.scatter_mapbox(mapa_status,
                            lat='lat',
                            lon='long',
                            color='status',
                            size='price',
                            size_max=15,
                            zoom=9)

            fig.update_layout(mapbox_style='open-street-map')
            fig.update_layout(height=600, margin={'r':0,'l':0,'b':0,'t':0})
            st.plotly_chart(fig)

        
        # Visualização do resultado
        st.subheader('DataFrame com todas as sugestões de compra')
        comprar = data[data['status'] == 'Comprar']

        result = comprar[['id', 'price', 'price_median', 'status']]
        result

        # Questão de negócio 2
        st.markdown("<h1 style='text-align: center; color: black;'>2 - Uma vez o imóvel comprado, qual o melhor momento para vendê-lo e por qual preço?</h1>", unsafe_allow_html=True)
        st.markdown(' - Se o preço de compra, for maior que a mediana da região por sazonalidade, o preço de venda deve ser igual ao preço de compra acrescido 10%')
        st.markdown(' - Se o preço de compra, for menor que a mediana da região por sazonalidade, o preço de venda deve ser o preço de compra acrescido 30%')
        st.markdown(' - Abaixo, você verá um DataFrame com todos os imóveis sugeridos para venda, indicando a melhor estação para vender o imóvel e o valor sugerido para venda.')

        data = comprar[comprar['status'] == 'Comprar']

        df1 = data [['price', 'season', 'zipcode']]. groupby(['zipcode','season']).median().reset_index()
        df1 = df1.rename(columns={'price':'price_median_season'})

        df2 = pd.merge(df1,data, on='zipcode', how='inner')
        df2 = df2.rename(columns={'season_x':'season'})

        # Visualização do melhor valor a ser vendido cada imóvel.
        for i, row in df2.iterrows():
            if (row['price'] >= row['price_median_season']):
                df2.loc[i,'sale'] = row['price']*1.10
            else:
                df2.loc[i, 'sale'] = row['price']*1.30

        # Visualização do lucro a ser obtido por venda.
        df2['profit'] = df2['sale'] - df2['price']
        
        # Visualização da melhor estação para vender o imóvel.
        df3 = df2[df2['status'] == 'Comprar']

        df3 = df3[['id', 'price', 'zipcode', 'price_median', 'season', 'price_median_season', 
                    'condition_type', 'status', 'sale', 'profit']].sort_values(['id','profit'])

        df3 = df3.drop_duplicates(subset=['id'], keep='first')

        melhor_est = df3[['id','season','sale']]
        melhor_est

        return None
 

if __name__ == '__main__':
    # ETL
    # data extration
    path = 'hr_clean.csv'    
    data = get_data(path)


    # transformation
    sidebar_features(data)

    pages_sidebar(data)