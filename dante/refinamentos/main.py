import pyconll
import os
import pandas as pd
import json

# ----- CONSTANTS --------
INPUT_DIRECTORY = "./to-process"
OUTPUT_CONLLU_DIRECTORY = "./processed"

# ----- MAIN JOBS --------

# monta dicionário


def save_conllu(corpus_conllu, filename):
    # saves as conllu
    with open(f"{OUTPUT_CONLLU_DIRECTORY}/{filename}", 'w', encoding='utf-8') as f:
        for sentence in corpus_conllu:
            f.write(sentence.conll())
            f.write("\n\n")


def mount_dict():
    ref_dict = {}

    # lê como data frame
    ref_df = pd.read_csv("./ref.csv", header=None)

    # itera nas linhas p/ montar dict
    for i in range(len(ref_df)):
        # obtém os dados do df
        form = ref_df.iloc[i, 0]
        old_upos = ref_df.iloc[i, 1]
        new_upos = ref_df.iloc[i, 2]
        pack_number = ref_df.iloc[i, 3]

        # cria dicionário aninhado, se ele ainda não existir
        if not ref_dict.get(pack_number, False):
            ref_dict[pack_number] = {}

        # preenche dicionário aninhado
        ref_dict[pack_number][(form, old_upos)] = new_upos

    return ref_dict


# montar dicionario
ref_dict = mount_dict()
stats = []  # deve guardar estatísticas
# gets the pack number from the file name
pack_name_translator = {
    "1a147.conllu": 0,
    "dante_pack1.conllu": 1,
    "dante_pack2.conllu": 2,
    "dante_pack3.conllu": 3,
    "dante_pack4.conllu": 4,
    "dante_pack5.conllu": 5,
    "dante_pack6.conllu": 6,
    "dante_pack7.conllu": 7,
    "dante_pack8.conllu": 8,
    "dante_pack9.conllu": 9,
    "dante_pack10.conllu": 10,
    "dante_pack11.conllu": 11,
    "dante_pack12.conllu": 12
}

# walks at every file inside directory
for filename in os.listdir(path=INPUT_DIRECTORY):
    pack_number = pack_name_translator[filename]
    tokens_alterados = 0

    print(f"Convertendo {filename} para dict...")

    # reads one conllu file
    corpus_conllu = pyconll.load_from_file(
        f"{INPUT_DIRECTORY}/{filename}")

    print(f"{filename} convertido!")

    # iterates through every token of every sentence
    # adding the feature, if necessary
    print("Iterando em todos os tokens de todas as sentenças...")
    for sentence in corpus_conllu:
        # iterates through every token in current sentence
        for token in sentence:
            if (token.form, token.upos) in ref_dict[pack_number]:
                token.upos = ref_dict[pack_number][(token.form, token.upos)]
                tokens_alterados += 1

    print(
        f"Finalizado! Número de pos tags alteradas no pack {pack_number}: {tokens_alterados}\n\n\n")

    stats.append({
        "pack": filename,
        "pos_tags_alteradas": tokens_alterados
    })

    save_conllu(corpus_conllu, filename)

# serializes dict with stats
with open("./processed/stats.json", "w") as f:
    f.write(json.dumps(stats, sort_keys=True, indent=4))
