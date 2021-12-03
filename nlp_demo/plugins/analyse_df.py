from dframcy import DframCy


def get_df_from_nlp(nlp, stmt):
    print("================= Print dataframe of nlp  =================")
    dframcy = DframCy(nlp)
    doc_df = dframcy.nlp
    annotation_dataframe = dframcy.to_dataframe(doc_df)
    print(annotation_dataframe)