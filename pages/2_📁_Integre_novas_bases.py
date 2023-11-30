
import streamlit as st


st.title('📁 Integre novas bases de dados')

st.markdown('''---''')
st.subheader('Gostaria de integrar novos arquivos?')
st.file_uploader('Carregue arquivos a ser integrados:', accept_multiple_files=True, type=['csv', 'xlsx', 'txt'])