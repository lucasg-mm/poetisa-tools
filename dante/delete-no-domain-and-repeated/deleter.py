import pyconll
import pandas as pd
import os
import json

# >> gather sentences' ids that should be deleted
print(">> Gathering ids from the sentences that should be deleted...")

# list of ids of the sentences to be deleted
to_delete = {}

# ids from repetidos
repetidos = pd.read_csv("./to-process/Repetidos.txt",
                        sep="\t", names=["tweet_id", "retweet_id"])

# saves the ids in the 'to_delete' dict
to_delete["repeated"] = set(repetidos["retweet_id"].tolist())

# creates nested dict for later
to_delete["invalid"] = {}

# ids from DANTEStocks_DomainNo
# iterates through every file in the directory
directory = "./to-process/DANTEStocks_DomainNo"

for filename in os.listdir(path=directory):
    # reads from excel file
    corpus_xls = pd.concat(pd.read_excel(
        f"{directory}/{filename}", header=None, sheet_name=None), ignore_index=True)

    # gets the name of column
    last_column_name = corpus_xls.iloc[:, -1].name

    # removes extension from filename
    filename_without_extension = filename[0:-5]

    # saves list of sentences to be deleted in a dict
    to_delete["invalid"][filename_without_extension] = set(corpus_xls[corpus_xls[last_column_name]
                                                                      == "DomainNo"][0].tolist())

    print(f"{filename}: {to_delete['invalid'][filename_without_extension]}")


# >> gather invalid tweets and deletes them from the corpus
print(">> Deleting sentences from the corpus and saving filtered sentences...")

# iterates through every corpus file
# dict to gather some statistics
stats = []
directory = "./to-process/DANTEStocks"
for filename in os.listdir(path=directory):
    print(f"\n\n>> FOR {filename}")
    # loading corpus
    corpus_conll_gold = pyconll.load_from_file(f"{directory}/{filename}")

    # should have conll with valid and non-repeated tweets
    clean_conll = []

    # filters the invalid sentences
    invalid_in_this_file_conll = []

    # filters the repeated sentences
    repeated_in_this_file_conll = []

    print(f">> number of sentences: {len(corpus_conll_gold)}")

    # removes extension from filename
    filename_without_extension = filename[0:-7]

    # gets the ids from the sentences that should be deleted in this file
    invalid_in_this_file_ids = to_delete["invalid"][filename_without_extension]
    print(
        f">> number of invalid tweets detected: {len(invalid_in_this_file_ids)}")

    # we're going to count how many repeated tweets there are in the file
    number_of_invalid = 0
    number_of_repeated = 0
    number_of_repeated_and_invalid = 0
    for index, sentence in enumerate(corpus_conll_gold):

        # if this sentence is invalid
        if sentence.meta_value("sent_id") in invalid_in_this_file_ids or sentence.meta_value("sent_id") in to_delete["repeated"]:

            if sentence.meta_value("sent_id") in invalid_in_this_file_ids:
                print(f">> invalid {sentence.meta_value('sent_id')}")
                number_of_invalid += 1
                # saves it in a list
                invalid_in_this_file_conll.append(sentence)

            if sentence.meta_value("sent_id") in to_delete["repeated"]:
                print(f">> repeated {sentence.meta_value('sent_id')}")
                number_of_repeated += 1
                # saves it in a list
                repeated_in_this_file_conll.append(sentence)

            if sentence.meta_value("sent_id") in invalid_in_this_file_ids and sentence.meta_value("sent_id") in to_delete["repeated"]:
                print(
                    f">> repeated and invalid {sentence.meta_value('sent_id')}")
                number_of_repeated_and_invalid += 1
        else:
            print(f">> keep {sentence.meta_value('sent_id')}")
            # saves it in a list
            clean_conll.append(sentence)

    # pushes some stats to the stats list
    stats.append({
        "pack": filename_without_extension,
        "qtd_inicial_de_tweets": len(corpus_conll_gold),
        "qtd_de_NoDomain": number_of_invalid,
        "qtd_de_repetidos": number_of_repeated,
        "qtd_de_repetidos_e_NoDomain": number_of_repeated_and_invalid,
        "qtd_final_de_tweets": len(clean_conll)
    })

    # writes clean conllu
    with open(f"./processed/arquivos-limpos/{filename}", 'w', encoding='utf-8') as f:
        for sentence in clean_conll:
            f.write(sentence.conll())
            f.write("\n\n")

    # writes invalid conllu in other directory
    with open(f"./processed/excluidos/DomainNo/{filename}", 'w', encoding='utf-8') as f:
        for invalid_sentence in invalid_in_this_file_conll:
            f.write(invalid_sentence.conll())
            f.write("\n\n")

    # writes repeated conllu in other directory
    with open(f"./processed/excluidos/repetidos/{filename}", 'w', encoding='utf-8') as f:
        for repeated_sentence in repeated_in_this_file_conll:
            f.write(repeated_sentence.conll())
            f.write("\n\n")

# serializes dict with stats
with open("./processed/stats.json", "w") as f:
    f.write(json.dumps(stats, sort_keys=True, indent=4))
