

def get_all_sentiment_data(doc, lemma_doc):
    print("")
    print("========= Sentiment Analysis (Working) ==============")
    print(f"{doc._.polarity} {lemma_doc._.polarity}")
    print(f"{doc._.subjectivity} {lemma_doc._.subjectivity}")
    print(f"{doc._.assessments} {lemma_doc._.assessments}")

def get_sentiment(sent):
    return sent._.polarity, sent._.subjectivity, sent._.assessments
