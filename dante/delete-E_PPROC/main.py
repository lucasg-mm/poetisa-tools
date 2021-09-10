import pyconll
import os
import json

# stores statistics of processing
stats = []
directory = "./to-process"

# walks at every file inside directory
for filename in os.listdir(path=directory):
    # loads corpus
    corpus_conll_gold = pyconll.load_from_file(f"{directory}/{filename}")

    # should have the clean conll-u files
    clean_conll = []

    # should have the dirty conll-u files
    dirty_conll = []

    # removes extension from filename
    filename_without_extension = filename[0:-7]

    # iterates through every token of every sentence in the golden corpus
    for sentence in corpus_conll_gold:
        sentence_has_e_pproc = False

        for token in sentence:
            # if the token has E_PPROC as value, put the
            # sentence in the dirty_conll list
            if token.upos == "E_DIGIT":
                sentence_has_e_pproc = True
                dirty_conll.append(sentence)
                break

        # if the sentence does not has E_PPROC as a value, it's clean
        if not sentence_has_e_pproc:
            clean_conll.append(sentence)

    # writes clean conllu
    with open(f"./processed/arquivos-limpos/{filename}", 'w', encoding='utf-8') as f:
        for clean_sentence in clean_conll:
            f.write(clean_sentence.conll())
            f.write("\n\n")

    # writes dirty conllu
    with open(f"./processed/arquivos-sujos/{filename}", 'w', encoding='utf-8') as f:
        for dirty_sentence in dirty_conll:
            f.write(dirty_sentence.conll())
            f.write("\n\n")

    # annotates stats
    stats.append({
        "pack": filename_without_extension,
        "qtd_inicial_de_tweets": len(corpus_conll_gold),
        "qtd_de_E_DIGIT": len(dirty_conll),
        "qtd_final_de_tweets": len(clean_conll)
    })


# serializes dict with stats
with open("./processed/stats.json", "w") as f:
    f.write(json.dumps(stats, sort_keys=True, indent=4))
