from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from annotated_text import annotated_text
from yargy_tools import make_grams_production, make_morph_pipeline, \
    slice_text, get_parser, grams_dict, grams_dict_1
from yargy import rule, Parser

# """
# # Welcome to Streamlit!
#
# Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:
#
# If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
# forums](https://discuss.streamlit.io).
#
# In the meantime, below is an example of what you can do with just a few lines of code:
# """

if 'productions' not in st.session_state:
    st.session_state.productions = []
st.session_state.submit = False
st.set_page_config(layout='wide')

count = st.number_input('count of tokens', min_value=1, max_value=10, step=1)
if count:
    cols = st.columns(count)
    for i, col in enumerate(cols):
        type = col.selectbox('token type', ['', 'exact_words', 'grams'], key=f"toke_type#{i}")
        if type == 'exact_words':
            terms = col.text_input("terms", key=f"terms#{i}")
            if col.button('add', key=f"addpipline#{i}"):
                st.session_state.productions.append(make_morph_pipeline(terms))
                print(st.session_state.productions)
        elif type == 'grams':
            grams = col.multiselect(
                'gram types',
                grams_dict_1.keys(),
                key=f"grams#{i}")
            operator = col.radio('operator', ['or', 'and'], key=f"operator#{i}")
            or_operator = operator == 'or'
            repeatable = col.checkbox('repeatable', key=f"repeatable#{i}")
            optional = col.checkbox('optional', key=f"optional#{i}")

            # productions.append(make_grams_production(grams, repeatable, optional, or_operator))
            if col.button('add', key=f"addgram#{i}"):
                print(or_operator, repeatable, optional)
                st.session_state.productions.append(make_grams_production(grams, repeatable, optional, or_operator))
                print(st.session_state.productions)
    if st.button('Create parser'):
        print(st.session_state.productions)
        TECHNOLOGY = rule(*st.session_state.productions)
        st.session_state.parser = Parser(TECHNOLOGY)
    if 'parser' in st.session_state:
        text = st.text_input('Input')
        if st.button('Parse'):
            matches = st.session_state.parser.findall(text)
            matches = sorted(matches, key=lambda _: _.span)
            spans = [_.span for _ in matches]
            chunks = slice_text(text, spans)
            print(matches)
            annotated_text(*chunks)


# parser = get_parser()
# text = st.text_input('somethinng')
# if st.button('parse'):
#     matches = parser.findall(text)
#     matches = sorted(matches, key=lambda _: _.span)
#     spans = [_.span for _ in matches]
#     chunks = slice_text(text, spans)
#     print(chunks)
#     annotated_text(*chunks)
