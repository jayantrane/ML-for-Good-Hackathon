import spacy
# import eng_spacysentiment
from spacy.lang.en.stop_words import STOP_WORDS
from negspacy.negation import Negex
# Load English tokenizer, tagger, parser and NER
from spacy import displacy
# from spacy_grammar.grammar import Grammar  # this is not supported in spacy 3
from spacytextblob.spacytextblob import SpacyTextBlob


# nlp_sentiment = spacy.load("spacysentiment")  # not working
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("negex"
    # , config={"ent_types":["PERSON","ORG"]}
)
nlp.add_pipe('sentencizer')
# nlp.add_pipe("contextual spellchecker")  # TODO: spellchecker taking time
# s2v = nlp.add_pipe("sense2vec")
nlp.add_pipe('spacytextblob')


# nlp.add_pipe(
#     "negex",
#     config={
#         "neg_termset":{
#             "pseudo_negations": ["might not"],
#             "preceding_negations": ["not"],
#             "following_negations":["declined"],
#             "termination": ["but","however"]
#         }
#     }
# )
