import os

import pandas as pd
import pypandoc
from pypandoc.pandoc_download import download_pandoc
# see the documentation how to customize the installation path
# but be aware that you then need to include it in the `PATH`
download_pandoc()

def extract_text(doc_filename, calling_from_streamlit=False):
    if calling_from_streamlit == True:
        with open(os.getcwd() + "/" + os.path.join("nlp_demo/data", doc_filename.name), "wb") as f:
            f.write(doc_filename.getbuffer())

        doc_filename = os.getcwd() + "/" + os.path.join("nlp_demo/data", doc_filename.name)

    # print(doc_filename)
    new_file_name = f"{doc_filename.split('/')[-1].split('.')[0]}.txt"
    outfile_name = f"{os.getcwd()}/{os.path.join('nlp_demo/data')}/{new_file_name}"
    output = pypandoc.convert_file(doc_filename, 'plain', outputfile=outfile_name)
    assert output == ""

    characters = []

    f = open(outfile_name)
    character = set()
    speaker = ""
    spoken_word = ""
    for i in f.readlines():
        i = i.replace("\n", "")
        if i == "":
            continue

        if i[0] == "(":
            speaker = ""
            spoken_word = ""
            continue

        if i[0] == "[":
            speaker = ""
            spoken_word = ""
            continue

        if i[-1] == ":" and len(i) < 20:
            character.add(i[:-1])
            speaker = i[:-1]

        if i[:-1] in character:
            continue
        else:
            spoken_word = i
            characters.append([speaker, spoken_word])
            # print([speaker, spoken_word])
            speaker = ""
            spoken_word = ""

    # print(characters)

    final_conversations = []
    for i, j in characters:
        if i == "":
            final_conversations[-1][1] += f" {j}"
        else:
            final_conversations.append([i, j])

    # print(final_conversations)

    final_conversations_1 = []
    for i, j in final_conversations:
        if "[" in j and "]" in j:
            start_index = j.index("[")
            end_index = j.index("]")
            j = j[:start_index] + j[end_index + 1:]

        final_conversations_1.append([i, j])

    # print(final_conversations_1)
    return final_conversations_1

def save_df(doc_filename, calling_from_streamlit=False):
    chat_text_df = pd.DataFrame(data=extract_text(doc_filename=doc_filename, calling_from_streamlit=calling_from_streamlit), columns=["person", "text"])
    if calling_from_streamlit:
        doc_filename = doc_filename.name

    new_file_name = f"{doc_filename.split('/')[-1].split('.')[0]}.txt"
    parquet_file_path = os.getcwd() + "/" + os.path.join("nlp_demo/data", f"{new_file_name[:-4]}.parquet")
    chat_text_df.to_parquet(parquet_file_path)
    return parquet_file_path


if __name__ == "__main__":
    # doc_filename = "../Data/FocusGroups/Gaming_Group1.docx"
    doc_filename = "../../csv_data/Gaming_Group1.docx"
    save_df(doc_filename)
