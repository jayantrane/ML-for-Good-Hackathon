# import spacy
# from spacy.scorer import Scorer
#
# # Default scoring pipeline
# # scorer = Scorer()
#
# # Provided scoring pipeline
# nlp = spacy.load("en_core_web_sm")
# scorer = Scorer(nlp)
# doc = [("my name is Dilip", 11, 16)]
#
# scores = Scorer.score_token_attr(doc, "pos")
# print(scores["pos_acc"])
# print(scorer)
