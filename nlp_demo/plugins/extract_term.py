from pyate import combo_basic, weirdness, term_extractor

# Note the scores in it to 


def get_terms_from_text(stmt):
    print("")
    print("========= Term Extractor  (Working) (how is the impact of word in that statement) ==============")
    print(combo_basic(stmt).sort_values(ascending=False))
    print("&&&&&&&&")
    print(weirdness(stmt).sort_values(ascending=False))
    print("&&&&&&&&")
    print(term_extractor(stmt).sort_values(ascending=False))
    print("&&&&&&&&")
    # print(cvalue(stmt).sort_values(ascending=False).head(5))
    # print("&&&&&&&&")