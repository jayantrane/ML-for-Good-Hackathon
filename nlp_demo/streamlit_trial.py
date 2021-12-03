import streamlit as st
import pandas as pd
import numpy as np
from nlp_demo.meeting_chat.extract_meeting_text import save_df
from nlp_demo.spacy_trial import analyse_statement

if 'current_line' not in st.session_state:
    st.session_state.current_line = 1

st.session_state.result_dict = {}

uploaded_file = st.file_uploader("Upload chat file")
print(uploaded_file)

if uploaded_file is not None:
    chat_df_path = save_df(uploaded_file, True)
    chat_text_df = pd.read_parquet(chat_df_path)
    st.write("Given chat data")


    # st.dataframe(chat_text_df)

    # COLUMNS_SELECTED = st.multiselect('Select options', df.columns.to_list())
    # ROWS_SELECTED = st.multiselect('Select options', chat_text_df.columns.to_list())
    # print(ROWS_SELECTED)
    def highlight_current_row(s):
        output = ['background-color: #FFFF99'] * st.session_state.current_line
        output.extend(['background-color: #90ee90'] * (len(s) - st.session_state.current_line))
        return output


    st.dataframe(chat_text_df.style.apply(highlight_current_row, axis=0))

    increment = st.button('Read Next Chat')
    if increment:
        st.session_state.current_line += 1

    increment = st.button('Read All Chat')
    if increment:
        st.session_state.current_line = False

    if st.session_state.current_line:
        df = analyse_statement(chat_text_df.loc[st.session_state.current_line, ['person', 'text']])
    else:
        df = analyse_statement(chat_text_df.loc[:, ['person', 'text']])

    st.write(df)
    # st.dataframe(df)
    # def color_survived(val):
    #     color = 'green' if val else 'red'
    #     return f'background-color: {color}'

    # st.dataframe(chat_text_df.style.applymap(color_survived, subset=['Survived']))

#
# dataframe = pd.DataFrame(
#     np.random.randn(10, 20),
#     columns=('col %d' % i for i in range(20))
# )
#
# st.dataframe(dataframe.style.highlight_max(axis=0))

#
# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=['a', 'b', 'c'])
#
# st.line_chart(chart_data)
#
# x = st.slider('x')  # 👈 this is a widget
# st.write(x, 'squared is', x * x)
#
# st.text_input("Your name", key="name")
#
# # You can access the value at any point with:
# st.session_state.name
#
# if st.checkbox('Show dataframe'):
#     chart_data = pd.DataFrame(
#         np.random.randn(20, 3),
#         columns=['a', 'b', 'c'])
#
#     chart_data
#
# df = pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
# })
#
# option = st.selectbox(
#     'Which number do you like best?',
#     df['first column'])
#
# 'You selected: ', option
#
#
# def add(a, b):
#     c = a + b
#
#     return c
#
#
# if st.button('add'):
#     result = add(1, 2)
#     st.write('result: %s' % result)


#
# id, name, country, occ, race, age, .... ,  Target: worried, impact
#
# Age:
# 1-10 - 1
# 11-20 - 2
# 21-40 - 3
#
# country
# {
#     "cold": ['ireland', canada. us],
#     "hot" : ""
# }
#
# school - weight - 0.2
#
# working - 0.5




