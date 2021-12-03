import json

import pandas as pd
from nlp_demo import define_rules
from nlp_demo.initialize_nlp import nlp
from nlp_demo.plugins.check_sentiment import get_sentiment


def analyze_text(doc):
    print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

    # Find named entities, phrases and concepts
    for entity in doc.ents:
        print(entity.text, entity.label_)


def analyse_text_more(doc):
    lemma = get_lemma(doc)
    print(lemma)
    ent = get_ent(doc)
    print(ent)
    print(f"Noun Chunks - {list(doc.noun_chunks)}")
    print(f"Noun Chunks - {list(doc.noun_chunks)}")
    new_str, replaced_noun_chunk = replace_string_with_simple_noun_against_noun_chunks(doc)
    print(new_str)
    print("-------------------------")

    doc = nlp(new_str)
    new_str = keep_single_pronoun_or_noun_in_doc(doc)

    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)

    print("+++++++++++++++++++++++++")

    for token in doc:
        print(token.text, token.dep_, token.head.text, token.head.pos_, [child for child in token.children])
    print("==========================")

    columns = ["text", "pos_", "tag_", "dep_", "morph", "head_text", "head_pos_", "head_tag_", "head_dep_", "morph", "child", "sent_index"]
    doc_sent_token_list = []
    for sent_index, sent in enumerate(doc.sents):
        for token in nlp(str(sent)):
            doc_sent_token_list.append([token.text, token.pos_, token.tag_, token.dep_, token.morph, token.head.text, token.head.pos_, token.head.tag_, token.head.dep_, token.morph, [child for child in token.children], sent_index])

    df_doc_sent_token = pd.DataFrame(columns=columns, data=doc_sent_token_list)

    print("==========================")

    df_doc_sent_token[df_doc_sent_token["pos_"] == 'PRON']
    df_doc_sent_token[df_doc_sent_token["pos_"] == 'ADJ']
    df_doc_sent_token[df_doc_sent_token["dep_"] == 'prep']
    df_doc_sent_token[(df_doc_sent_token["dep_"] == 'prep') & (df_doc_sent_token["head_dep_"] == 'ROOT')] # been without school, cramped in apartment, is to me
    df_doc_sent_token[(df_doc_sent_token["dep_"] == 'prep') & (df_doc_sent_token["head_dep_"] == 'ROOT') & (df_doc_sent_token["pos_"] == 'ADP') & (df_doc_sent_token["head_pos_"] == 'AUX')] # been without school, is to me


    lemma_token_list = []
    lemma_doc = get_lemma_from_doc(doc)
    for token in lemma_doc:
        lemma_token_list.append([token.text, token.pos_, token.tag_, token.dep_, token.morph, token.head.text, token.head.pos_, token.head.tag_, token.head.dep_, token.morph, [child for child in token.children], ""])

    df_lemma_token = pd.DataFrame(columns=columns, data=lemma_token_list)

    print("==========================")

    lemma_token_list = []
    lemma_doc = get_lemma_from_doc(doc)
    without_stop_word = remove_stop_words(lemma_doc)
    for token in without_stop_word:
        lemma_token_list.append([token.text, token.pos_, token.tag_, token.dep_, token.morph, token.head.text, token.head.pos_, token.head.tag_, token.head.dep_, token.morph, [child for child in token.children], ""])

    df_no_stop_word_token = pd.DataFrame(columns=columns, data=lemma_token_list)


    print(df_lemma_token)

    return df_doc_sent_token, df_lemma_token, df_no_stop_word_token

def remove_stop_words(doc):
    # remove stop words
    new_doc = []
    for word in doc:
        if word.is_stop == False:
            new_doc.append(word)

    print(f"Sentence without stop word: {new_doc}")
    new_doc = nlp(" ".join([str(i) for i in new_doc]))
    return  new_doc

def remove_punct(doc):
    # remove stop words
    new_doc = []
    for word in doc:
        if word.is_punct == False:
            new_doc.append(word)

    print(f"Sentence without punct: {new_doc}")
    new_doc = nlp(" ".join([str(i) for i in new_doc]))
    return  new_doc

def get_lemma(doc):
    data = {}
    for e in doc:
        data[e.text] = [e.lemma_]

    return data

def get_lemma_from_doc(doc):
    lemma_stmt = " ".join([token.lemma_ for token in doc])
    lemma_doc = nlp(lemma_stmt)
    print(lemma_doc)
    return lemma_doc

def get_ent(doc):
    return [("", ent.label_, ent.start, ent.end, ent._.negex, ent.text, False, get_sentence_from_word_index(doc, ent.start, ent.end, ent.text)[1]) for ent in doc.ents]

# def get_ent(doc):
#     data = {}
#     for e in doc.ents:
#         data[e.text] = [e.label_, e._.negex]
#
#     return data

def replace_string_with_simple_noun_against_noun_chunks(doc):
    replaced_noun_chunk = {}
    # old_string = str(doc)
    new_str = str(doc)
    for n in doc.noun_chunks:
        last_word = str(n).split(' ')[-1]
        new_str = new_str.replace(str(n), last_word)
        replaced_noun_chunk[str(n)] = last_word

    return new_str, replaced_noun_chunk

def keep_single_pronoun_or_noun_in_doc(doc):
    propn_found = False
    new_str = ""
    # here we are not taking into account for multiple person in the same doc. We are considering that only single person exists
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
        if not propn_found:
            new_str += token.text
            if token.pos_ not in ['PROPN', 'NOUN']:
                pass


def get_sentence_from_word_index(doc, word_start_index, word_end_index, text):
    index = 0
    sent_index = 0
    sent = ""
    for s in doc.sents:
        sent = s
        for i in s:
            length_of_word = word_end_index - word_start_index
            if word_start_index == index and str(doc[word_start_index:word_start_index + length_of_word]) == text:
                return sent, sent_index

            index += 1

        sent_index += 1

def get_sentence_to_analyse(doc):
    sent_index = 0
    final_data = []
    for s in doc.sents:
        sent_index += 1
        # ent_list = get_ent(s)
        final_data.append([sent_index - 1, str(s)])

    return final_data


def get_ner_analysis(doc, lemma_doc):
    ner_list = []
    start_list = []
    matches = define_rules.matcher(lemma_doc)

    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        print(match_id, string_id, start, end, span.text)
        if start not in start_list:  # This is to get the unique list
            start_list.append(start)
            # columns are match_id, ..., sentence and index of sentence
            # sent_text = get_sentence_from_word_index(doc, start)[0]
            sent_index = get_sentence_from_word_index(doc, start, end, span.text)[1]

            if span.end - span.start > 1:
                is_stop = False
            else:
                is_stop = [token.is_stop for token in nlp(str(span))][0]

            ner_list.append([match_id, string_id, start, end, span._.negex, span.text, is_stop, sent_index])

    ent_list = get_ent(lemma_doc)
    ner_list.extend(ent_list)
    # get the sentence where this matcher found and store it as corresponding data

    columns = ["match_id", "ner", "word_start_index", "word_end_index", "negative", "phrase", "is_stop", "sent_index"]
    df= pd.DataFrame(columns=columns, data=ner_list)
    return df


def get_sent_analysis(doc):
    given_date = ""
    category = {
        "entity": set(),  # name of person or whatever it is referring
        "Past": {"event": set()},  # past event according to person
        "Pres": {"event": set()},  # present event according to person
        "future": {"event": set()},  # future event according to person
        "org": set(),  # people mentioned about hospital or medicial or some institution
        "neg": set()
    }

    sent_list = get_sentence_to_analyse(doc)
    columns = ["sent_index", "sent_text"]
    df = pd.DataFrame(columns=columns, data=sent_list)
    df.set_index("sent_index")

    for sent_index, s in enumerate(doc.sents):
        noun_chunks_list = list(s.noun_chunks)
        noun_chunks_list_str = list(map(lambda x: str(x), s.noun_chunks))
        print(f"Noun chunks - {noun_chunks_list_str}")
        past = ""
        pres = ""
        entity = ""
        org = ""
        negative_stmt = ""
        ent = s.ents
        for e in s.as_doc().ents:  # nlp(s).ents
            print(e.text, e.start_char, e.end_char, e.label_, e._.negex)
            if e.label_ == 'ORG':
                category['org'].add(e.text)
                org = e.text
            if e.label_ == 'DATE':
                given_date = e.text

            negative_stmt = e._.negex  # show this statement as red if True

        for i, d in enumerate(s):
            print(d, d.morph.get("Tense"))
            # print(f"{d} {d.pos_}")
            if d.pos_ in ['NOUN', 'PROPN'] and d.lemma_ == str(d) and d.dep_ == 'nsubjpass':
                category['entity'].add(d)
                entity = d
            if str(d) not in noun_chunks_list_str:
                # if d.pos_ == 'VERB':
                print(d, d.morph.get("Tense"))
                if "Past" in d.morph.get("Tense"):
                    category['Past']['event'].add((d, given_date, negative_stmt))
                    if not d.is_stop:
                        past = d
                if "Pres" in d.morph.get("Tense"):
                    category['Pres']['event'].add((d, given_date, negative_stmt))
                    if not d.is_stop:
                        pres = d


                # if d.head.pos_ == "VERB":
                #     d.text
                # print(ent[i].text, ent[i]._.negex, d)
                print("=====")

        sentiment_data = get_sentiment(s)
        df.loc[sent_index, 'org'] = org
        df.loc[sent_index, 'negative_stmt'] = negative_stmt
        df.loc[sent_index, 'entity'] = entity
        df.loc[sent_index, 'Past'] = str(past)
        df.loc[sent_index, 'Pres'] = str(pres)
        df.loc[sent_index, 'sent_index'] = sent_index
        df.loc[sent_index, 'polarity'] = sentiment_data[0]
        df.loc[sent_index, 'subjectivity'] = sentiment_data[1]
        df.loc[sent_index, 'assessment'] = json.dumps(sentiment_data[2])

    return df