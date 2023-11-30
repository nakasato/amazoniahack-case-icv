import streamlit as st
import utils as db
import streamlit.components.v1 as components
from openai import OpenAI



PROMPT_INSIGHTS = '''Você é um especialista em conservação da Amazônia, em especial da região no estado de Mato Grosso, Brasil.
Sua missão é ajudar experts do IBAMA a identificar informações de madeira extraída ilegalmente.

Cite 5 informações que podem ser extraídas da seguinte tabela que podem ser relevantes para detectar fraude na extração de madeiras. 

Dê alguns insights acionáveis para os experts.

Seja claro e direto.

Tabela: {}
'''

st.set_page_config(layout='wide')

st.title('🧑‍🔬️ Minhas análises')
st.markdown('''
            Aqui você tem liberdade para fazer suas **próprias consultas SQL e análises**. Seus resultados são analisados em tempo real pelo GPT-4.
            ''')
st.markdown('''---''')

col1, col2 = st.columns(spec=(1, 1), gap='medium')
db_tables = db.get_table_names()

col2.subheader('🗃 Tabelas disponíveis no banco de dados')
tname = col2.selectbox('Selecione as tabelas que gostaria de visualizar', db_tables)
col2.markdown(f'Amostra da tabela **{tname}** selecionada:')
df = db.read_sql(f'''select * from "{tname}" limit 5;''')
col2.dataframe(df.head())

col1.subheader('📊 Faça sua própria consulta')
input_sql = col1.text_area('Entre com sua própria consulta (Postgres SQL):', 
                            help='''Por exemplo: SELECT * FROM "<minha_tabela>" LIMIT 10;''', 
                            height=200)
if input_sql:
    user_df = db.read_sql(input_sql)
    col1.dataframe(user_df)

    if len(user_df) != 0:
        st.subheader('💡 Insights sobre dados suspeitos')
        with st.spinner('Nossa IA está analisando uma amostra dos seus dados...'):
            ans = db.gpt(prompt=PROMPT_INSIGHTS.format(user_df.head(100)))
            st.success(ans)

###########


st.subheader("🤖 Mais dúvidas? Converse com nossa IA!")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Como posso ajudá-lo na sua análise?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})