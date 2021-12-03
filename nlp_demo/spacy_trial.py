import os
from collections import defaultdict

import pandas as pd
from pandas.io.json import json_normalize
from spacy import displacy
from tabulate import tabulate

from nlp_demo.initialize_nlp import nlp
# from nlp_demo.spell_check import get_spell_check_and_return
from nlp_demo.input_str import get_input_string
from nlp_demo.utils import analyze_text, analyse_text_more, get_lemma, get_lemma_from_doc, get_sent_analysis, \
    get_ner_analysis, remove_stop_words, remove_punct

sent_parquet_file_path = os.getcwd() + "/" + os.path.join("nlp_demo/data", f"sent.parquet")
ner_parquet_file_path = os.getcwd() + "/" + os.path.join("nlp_demo/data", f"ner.parquet")
doc_sent_parquet_file_path = os.getcwd() + "/" + os.path.join("nlp_demo/data", f"doc_sent.parquet")
analyzed_parquet_file_path = os.getcwd() + "/" + os.path.join("nlp_demo/data", f"analyzed.parquet")

df = {}
df["ner"] = {}
df["sent"] = {}
df["noun_chunks"] = {}
df["df_doc_sent_token"] = {}

remove_greeting_words = ["Hi", "Hey", "hello", "good morning", "good afternoon", "good evening"]
remove_name = ["parent 1", "parent 2", "parent 3", "parent 4", "parent 5", "moderator", "administrator"]
result = defaultdict(lambda: defaultdict(list))

def get_noun_chunks(doc):
    noun_chunks_list = []
    for sent_index, sent in enumerate(doc.sents):
        for chunk in nlp(str(sent)).noun_chunks:
            noun_chunks_list.append([sent_index, chunk.text])

    columns = ["sent_index", "chunks"]
    df1 = pd.DataFrame(columns=columns, data=noun_chunks_list)
    df1.set_index('sent_index')
    return df1


def analyse_statement(stmt, entity='default'):
    analysed_df = {}
    if isinstance(stmt, pd.Series):
        if stmt['person']:
            entity = stmt['person']

        if stmt['text']:
            stmt = stmt['text']

    stmt = stmt.lower()
    doc = nlp(stmt)

    lemma_doc = get_lemma_from_doc(doc)

    for w in remove_greeting_words:
        stmt = stmt.replace(w, "")

    for w in remove_name:
        stmt = stmt.replace(w, "")

    without_stop_word = remove_stop_words(nlp(stmt))
    without_punct_word = remove_punct(without_stop_word)

    if str(without_punct_word) != "":


        df_doc_sent_token, df_lemma_token, df_no_stop_word_token = analyse_text_more(doc)
        df_doc_sent_token = df_doc_sent_token[df_doc_sent_token['pos_'].isin(["ADP", "ADV", "NOUN", "NUM", "PROPN", "VERB"])]

        df["ner"][entity] = get_ner_analysis(doc, lemma_doc)
        df['sent'][entity] = get_sent_analysis(doc)
        df['noun_chunks'][entity] = get_noun_chunks(doc)
        df['df_doc_sent_token'][entity] = df_doc_sent_token

        # df['sent'].to_parquet(sent_parquet_file_path)
        # df['ner'].to_parquet(ner_parquet_file_path)
        # df_doc_sent_token.to_parquet(doc_sent_parquet_file_path)

        analysed_df = analyze_dfs(df['sent'], df['ner'], df['df_doc_sent_token'], df['noun_chunks'])

    # analysed_df.to_parquet(analyzed_parquet_file_path)

    return analysed_df

def analyze_dfs(sent_df, ner_df, token_df, chunks):
    for entity, value in ner_df.items():
        result[entity]['value_count'].append(value[value['is_stop'] == False]['ner'].value_counts())

    for entity, value in sent_df.items():
        result[entity]['sentiment'].append(value.loc[:, ["polarity", "subjectivity"]])
        result[entity]['pres'].append(value.loc[:, ["Pres"]])
        result[entity]['past'].append(value.loc[:, ["Past"]])

    # df = json_normalize(result, record_path=['default'], meta=['value_count', 'sentiment', 'pres', 'past'])
    return result


if __name__ == "__main__":

    stmt = get_input_string()
    print(analyse_statement(stmt))
    # doc = nlp(stmt)
    # analyze_text(doc)
    # get_lemma(doc)
    # get_ent(doc)

    # doc = get_spell_check_and_return(doc)

    final_result = [
        {
            "stmt": 0,
            "entity": "",
            "tags": ["CAUSE"],
            "noun_chunks": [],
            "sentiment": 0.4
        }
    ]

    # print(get_all_sentiment_data(doc, lemma_doc))

    # displacy.serve(doc, style="ent")

    result = {
        "hospital": {
            "count": 1,
            "positive": 1,
            "negative": 3,
            "past": {
                "list": ["taken", "to abc hospital"],
            },
            "present": {
                "list": ["taken"],
            },
            "all_statement_occured": ["I was taken to hospital"]
        },
        "covid": 2,
        "child": 3,

    }

    # TODO: if person is taen to hospital, then that means it is negative. For tag "hospital", we will consider it as negative

    # POS:
    # important:
    # ADP, ADV, NOUN, NUM, PROPN, VERB
    #
    # use but don't analyse:
    # PART
    #
    # ignore:
    # ADV, AUX, CONJ, CCONJ, DET, INTJ, PRON, PUNCT, SCONJ, SYM, X, SPACE
    #
