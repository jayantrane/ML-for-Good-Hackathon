from nlp_demo.initialize_nlp import nlp
import contextualSpellCheck

def get_spell_check_and_return(doc):
    nlp.add_pipe("contextual spellchecker")
    print("============= Spell check ==============")
    print(f"Spell check performed - {doc._.performed_spellCheck}")
    print(f"Suggestion - {doc._.suggestions_spellCheck}")
    doc = doc._.outcome_spellCheck
    doc = nlp(doc)
    return doc
