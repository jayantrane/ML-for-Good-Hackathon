import nltk
from nltk.corpus import wordnet
from spacy.matcher import Matcher
from nlp_demo.initialize_nlp import nlp

matcher = Matcher(nlp.vocab)

rule_list = [
    "parent",
    "child",
    "family",


    "school",
    "classes",
    "tuition",
    "friends",
    "office",
    "office work",
    "online",
    "offline",
    "online class",


    "teenage",
    "senior",
    "junior",
    "young",
    "old",

    "health",
    "environment",
    "vaccination",
    "hospital",
    "mortal",

    "social media",
    "communication",
    "meeting",
    "home",

    "clean",
    "wash",

    "problem",
    "issue",
    "income",
    "money",
    "entertainment",
    # "time",
    "government",
    "security",
    "safety",

    "pandemic",
    "disease",
    "healthcare",

    "death",
    "retire",
    "layoff",

    "spend",

    "economic",
    "political",
    "social",

    "spread",
    "virus",
    "symptoms",
    "cause",
    "ill",

    "science",
    "location",

    "employment",
    "recruitment",
    "employ",
    "recruit",
    "job",
    "internship",

    "apartment",
    "physical",
    "mental",
    "psychological",

    "teacher",
]





def get_unique_list_with_order_maintained(given_list):
    result_list = []
    for l in given_list:
        if l not in result_list:
            result_list.append(l)

    return result_list

def get_synonymns_of_rule(rule_name):
    synonyms = []
    antonyms = []
    print("===================  find synonyms and antonyms ===========================")
    for syn in wordnet.synsets(rule_name):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

    unique_synonyms_list = get_unique_list_with_order_maintained(synonyms)
    print(unique_synonyms_list)
    print(get_unique_list_with_order_maintained(antonyms))
    return unique_synonyms_list


def create_rule_dict_for_scapy_from_given_rule(rule_names):
    for rule_name in rule_names:
        result_list = []
        rule_token_list = get_synonymns_of_rule(rule_name)
        # rule_token_list = rule_token_list[:len(rule_token_list)//2]  # NOTE: This is not necessary as it is remove important words also.
        for token in rule_token_list:
            token_list = token.split(" ")
            deep_token = []
            for t in token_list:
                # if len(token_list) > 1:
                #     append({"LOWER": "hello"})
                deep_token.append({"LEMMA": t})
            # result_list.append([{, {"OP": "*"}, {"LOWER": "world"}])

            final_deep_token = []
            if len(deep_token) > 1:
                for d in deep_token:
                    final_deep_token.append(d)
                    if len(final_deep_token) % 2 != 0:
                        final_deep_token.append({"OP": "*"})
            else:
                final_deep_token = deep_token

            result_list.append(final_deep_token)

        if result_list:
            matcher.add(rule_name.upper(), result_list)


create_rule_dict_for_scapy_from_given_rule(rule_list)
