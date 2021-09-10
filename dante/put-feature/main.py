import pyconll
import os
import pandas as pd

# ----------- constants
INPUT_DIRECTORY = "./to-process"
OUTPUT_CONLLU_DIRECTORY = "./processed/conllu"
OUTPUT_EXCEL_DIRECTORY = "./processed/excel"

# ----------- main job

# walks at every file inside directory
for filename in os.listdir(path=INPUT_DIRECTORY):
    print(filename)

    # reads one conllu file
    corpus_conllu = pyconll.load_from_file(
        f"{INPUT_DIRECTORY}/{filename}")

    # iterates through every token of every sentence
    # adding the feature, if necessary
    for sentence in corpus_conllu:
        # iterates through every token in current sentence
        for token in sentence:
            # if the token pos tag is E_DIGIT
            if token.upos == "E_DIGIT":
                # adds the appropriate feature
                token.feats = {'Typo': {'Yes'}}

    # saves as conllu
    with open(f"{OUTPUT_CONLLU_DIRECTORY}/{filename}", 'w', encoding='utf-8') as f:
        for sentence in corpus_conllu:
            f.write(sentence.conll())
            f.write("\n\n")

    # saves as .xlsx
    corpus_df = pd.read_csv(
        f"{OUTPUT_CONLLU_DIRECTORY}/{filename}", sep="\t", names=list('abcdefghij'), skip_blank_lines=False)
    corpus_df.to_excel(
        f"{OUTPUT_EXCEL_DIRECTORY}/{filename[0:-7]}.xlsx", index=False, header=False)
