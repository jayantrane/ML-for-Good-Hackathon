from spacy import displacy

def display_data(doc):
    displacy.serve(doc, style="dep")