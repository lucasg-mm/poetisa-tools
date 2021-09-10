import pyconll
import os
import pandas as pd


excel_directory = "./to-process/excel-files"
conllu_directory = "./to-process/conllu-files"
merge_directory = "./to-process/to-merge"
processed_directory = "./processed"


def generate_conllu_to_merge():
    # walks at every file inside directory
    for filename in os.listdir(path=excel_directory):
        # loads corpus
        corpus_directory = f"{excel_directory}/{filename}"
        corpus = pd.read_excel(corpus_directory, dtype=object)

        # selects messed up rows
        messed_up_rows = corpus.loc[(corpus.iloc[:, 0].isna())
                                    & (corpus.iloc[:, 1].notna())]

        # fixes them by replacing the NaNs to "_"
        fixed_rows = messed_up_rows.fillna("_")

        # updates the original df with the fixed rows
        corpus.update(fixed_rows)

        # exports fixed file as .conllu
        corpus.to_csv(f"{conllu_directory}/{filename[0:-5]}.conllu",
                      sep="\t", header=False, index=False)


def fix_conllu_to_merge():
    # walks at every file inside directory
    for filename in os.listdir(path=conllu_directory):
        print(filename)
        corpus_conllu = pyconll.load_from_file(
            f"{conllu_directory}/{filename}")

        # iterates through every token of every sentence
        # fixing it, if necessary
        for sentence in corpus_conllu:
            counter = 1

            # gets the id of the last token
            last_token_id = str(len(sentence))

            # iterates through every token in current sentence
            for token in sentence:
                # fixes the id numbers
                token.id = str(counter)
                counter += 1

                # fixes the tag in the last column
                if token.id == last_token_id:
                    token.misc = {'SpacesAfter': {'\\n'}}

        # saves corrected file
        with open(f"{merge_directory}/corrected-files/{filename}", 'w', encoding='utf-8') as f:
            for sentence in corpus_conllu:
                f.write(sentence.conll())
                f.write("\n\n")


def merge_corrections():
    # walks at every file inside directory
    for filename in os.listdir(path=f"{merge_directory}/corrected-files"):
        # reads conllu w/ corrected annotation
        corrected_conllu = pyconll.load_from_file(
            f"{merge_directory}/corrected-files/{filename}")

        # reads conllu w/ old corpus
        old_conllu = pyconll.load_from_file(
            f"{merge_directory}/old-corpus/{filename}")

        # for each sentence in the corrected conllu...
        for corrected_sentence in corrected_conllu:

            # looks for the right one in the original corpus, and replaces it
            # after that, the original corpus must hold the sentence
            # with corrected annotation data
            for old_sentence in old_conllu:
                if old_sentence.meta_value("sent_id") == corrected_sentence.meta_value("sent_id"):
                    old_sentence.__init__(corrected_sentence.conll())
                    break

        # saves corrected file
        with open(f"{processed_directory}/{filename}", 'w', encoding='utf-8') as f:
            for sentence in old_conllu:
                f.write(sentence.conll())
                f.write("\n\n")


print(">> Fixing underscore problem...")
generate_conllu_to_merge()

print(">> Fixing 'id' and 'misc' problems...")
fix_conllu_to_merge()

print(">> merging the corrections...")
merge_corrections()
