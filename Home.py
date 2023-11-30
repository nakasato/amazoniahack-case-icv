import streamlit as st
import utils as db
import streamlit.components.v1 as components


st.set_page_config(layout='wide')

st.title('🌳 Wood Tracker')
st.markdown('''
            Bem-vindo ao Wood Tracker, um **sistema automatizado para integração e análise inteligente de dados públicos** do IBAMA, Sinaflor e Imaflora.

            O sistema permite que os usuários subam suas próprias bases de dados para análises conjuntas, além de alavancar o uso integrado de 
            **modelos de IA Generativa como GPT-4** para auxiliá-los na geração de insights acionáveis.
            ''')
st.markdown('''---''')

col1, col2 = st.columns(spec=(1, 1), gap='medium')
db_tables = db.get_table_names()

col1.subheader('📊 Analise as tabelas disponíveis no banco de dados')
tables_selected = col1.multiselect('Selecione as tabelas que gostaria de visualizar', db_tables)
if tables_selected:
    col1.subheader('Tabelas selecionadas:')
    for tname in tables_selected:
        col1.markdown(f'**{tname}:**')
        df = db.read_sql(f'''select * from "{tname}" limit 20;''')
        col1.dataframe(df)



with col2:
    st.subheader('Mapa de suspeição')
    st.markdown('''
                Visualize áreas com **potencial de irregularidades no transporte e extração de madeira**. 
                O Volume Suspeito, calculado a partir de dados geoespaciais integrados, destaca pontos de interesse.

                Detalhes sobre a **metodologia** empregada descrita no rodapé da página.
                ''')

    p = open('mapa_interativo.html')
    components.html(p.read(), height=600)

    st.markdown('''**Legenda:**
                \n- **Bolas azuis:** origem do transporte de madeira
                \n- **Regiões em vermelho:** áreas não autorizadas
                \n- **Regiões em verde:** áreas autorizadas''')

with st.expander('Metodologia para geração do mapa acima'):

    st.markdown('''Com o propósito de realizar uma integração de bases de dados visando identificar possíveis irregularidades no sistema de transporte e extração de madeira, empregamos conjuntos geoespaciais fornecidos pelo Imaflora. Estes conjuntos contêm a classificação "Autorizada" ou "Não-Autorizada" para as áreas, além dos dados provenientes do DOF - Transportes de Produtos Florestais. A partir das informações obtidas através do DOF, dispomos da quantidade de madeira transportada, bem como suas coordenadas geográficas, entre outras informações relevantes.
    Com base nesses dados, calculamos uma métrica denominada "Volume Suspeito". Essa métrica consiste essencialmente no volume total originado de um determinado ponto, multiplicado pelo fator de suspeição associado a esse ponto específico. O fator de suspeição de um ponto é determinado pela razão entre as áreas médias não autorizadas e as áreas médias autorizadas. Essa média é ponderada pelo inverso da distância entre o ponto e a área, de modo que áreas mais próximas do ponto de interesse têm uma contribuição maior para a média do que áreas distantes.
    Como resultado, desenvolvemos um mapa que visualmente destaca pontos com volumes suspeitos mais elevados, proporcionando ao usuário a capacidade de direcionar investigações mais detalhadas em áreas específicas.''')

    st.markdown('''Seja $A_i$ a i-ésima área autorizada, $d_{ik}$ a distância da k-ésima área para a i-ésima área autorizada (variáveis com * indicam áreas não autorizadas). Definimos as médias das áreas autorizadas/não autorizadas ao redor de um ponto $k$ como:''')

    st.latex(r'''
        \begin{equation}
        \langle A^* \rangle_k = \frac{\sum_{i=1}^{M} A_i^* d_{ik}^{-1}}{\sum_{i=1}^{M}d_{ik}^{-1} + \sum_{i=1}^{N}d_{ik}^{-1}}
        \end{equation}
    ''')

    st.latex(r'''
        \begin{equation}
        \langle A \rangle_k = \frac{\sum_{i=1}^{N} A_i^* d_{ik}^{-1}}{\sum_{i=1}^{M}d_{ik}^{*-1} + \sum_{i=1}^{N}d_{ik}^{-1}}
        \end{equation}
    ''')

    st.markdown('''Portanto, definimos o coeficiente suspeito do ponto k, $f_k$, como:''')

    st.latex(r'''
        \begin{equation}
        f_k = \frac{\langle A^* \rangle_k}{\langle A \rangle_k}
        \end{equation}
    ''')
        
    st.markdown('''E definimos o volume suspeito do ponto k, $V^*_k$, como:''')

    st.latex(r'''
        \begin{equation}
        V^*_k = f_k V_k
        \end{equation}
    ''')
        
    st.markdown('''onde $V_k$ é o volume total extraído do ponto k.''')

        
