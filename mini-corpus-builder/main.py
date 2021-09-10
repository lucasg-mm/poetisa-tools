import pyconll
from os import walk, path

def get_number_of_sentences(fname):
    """
    """
    
    with open(fname) as f:
        i = -1
        for i, l in enumerate(f):
            pass
    return i / 3


def write_patterns(sentence, match_results, upper_number_of_sentences):
    """
    """

    for result in match_results:
        file_directory = f"results/{result[0]}.txt"
        with open(file_directory, "a") as results_file:
            if get_number_of_sentences(file_directory) < upper_number_of_sentences:
                results_file.write(f"Sentence: {sentence.text}\n")
                results_file.write(f"Match: {result[1]}\n")
                results_file.write("\n")
                print(f">> Added sentence to file '{file_directory}'!")
            else:
                print(f">> The file '{file_directory}' already has {upper_number_of_sentences} sentences!")


def is_verb_or_aux(sentence, index):
    """
    """

    return (sentence[index].upos == "VERB" or sentence[index].upos == "AUX")


def is_sconj_or_adp(sentence, index):
    """
    """

    return (sentence[index].upos == "SCONJ" or sentence[index].upos == "ADP")


def analyse_sentence(sentence):
    """
    """

    match_results = []

    # with SCONJ/ADP and without ADV
    patterns = (("chegar", "a", "Inf"),
                ("passar", "a", "Inf"),
                ("vir", "a", "Inf"),
                ("voltar", "a", "Inf"),
                ("acabar", "de", "Inf"),
                ("deixar", "de", "Inf"),
                ("ter", "de", "Inf"),
                ("ter", "que", "Inf"))

    for pattern in patterns:
        index = 0

        while index < len(sentence) - 3:
            if (sentence[index].lemma == pattern[0] and is_verb_or_aux(sentence, index) and
                sentence[index+1].lemma == pattern[1] and is_sconj_or_adp(sentence, index+1) and
                    sentence[index+2].feats.get("VerbForm") and pattern[2] in sentence[index+2].feats.get("VerbForm") and is_verb_or_aux(sentence, index+2)):

                match_results.append(("|".join(
                    pattern), f"{sentence[index].form} {sentence[index+1].form} {sentence[index+2].form}"))

            index += 1

    # with SCONJ/ADP and with ADV in position 1
    patterns = (("chegar", "ADV", "a", "Inf"),
                ("passar", "ADV", "a", "Inf"),
                ("vir", "ADV", "a", "Inf"),
                ("voltar", "ADV", "a", "Inf"),
                ("acabar", "ADV", "de", "Inf"),
                ("deixar", "ADV", "de", "Inf"),
                ("ter", "ADV", "de", "Inf"),
                ("ter", "ADV", "que", "Inf"))

    for pattern in patterns:
        index = 0

        while index < len(sentence) - 4:
            if (sentence[index].lemma == pattern[0] and is_verb_or_aux(sentence, index) and
                sentence[index+1].upos == pattern[1] and
                sentence[index+2].lemma == pattern[2] and is_sconj_or_adp(sentence, index+2) and
                    sentence[index+3].feats.get("VerbForm") and pattern[3] in sentence[index+3].feats.get("VerbForm") and is_verb_or_aux(sentence, index+3)):

                match_results.append(("|".join(
                    pattern), f"{sentence[index].form} {sentence[index+1].form} {sentence[index+2].form} {sentence[index+3].form}"))

            index += 1

    # with SCONJ/ADP and with ADV in position 3
    patterns = (("chegar", "a", "ADV", "Inf"),
                ("passar", "a", "ADV", "Inf"),
                ("vir", "a", "ADV", "Inf"),
                ("voltar", "a", "ADV", "Inf"),
                ("acabar", "de", "ADV", "Inf"),
                ("deixar", "de", "ADV", "Inf"),
                ("ter", "de", "ADV", "Inf"),
                ("ter", "que", "ADV", "Inf"))

    for pattern in patterns:
        index = 0

        while index < len(sentence) - 4:
            if (sentence[index].lemma == pattern[0] and is_verb_or_aux(sentence, index) and
                sentence[index+1].lemma == pattern[1] and is_sconj_or_adp(sentence, index+1) and
                sentence[index+2].upos == pattern[2] and
                    sentence[index+3].feats.get("VerbForm") and pattern[3] in sentence[index+3].feats.get("VerbForm") and is_verb_or_aux(sentence, index+3)):

                match_results.append(("|".join(
                    pattern), f"{sentence[index].form} {sentence[index+1].form} {sentence[index+2].form} {sentence[index+3].form}"))

            index += 1

    # without SCONJ/ADP and without ADV
    patterns = (("vir", "Ger"),
                ("dever", "Inf"),
                ("estar", "Ger"),
                ("haver", "Part"),
                ("ir", "Inf"),
                ("poder", "Inf"),
                ("ser", "Part"),
                ("ter", "Part"))

    for pattern in patterns:
        index = 0

        while index < len(sentence) - 2:
            if (sentence[index].lemma == pattern[0] and is_verb_or_aux(sentence, index) and
                    sentence[index+1].feats.get("VerbForm") and pattern[1] in sentence[index+1].feats.get("VerbForm") and is_verb_or_aux(sentence, index+1)):

                match_results.append(("|".join(
                    pattern), f"{sentence[index].form} {sentence[index+1].form}"))

            index += 1

    # without SCONJ/ADP and with ADV in position 1
    patterns = (("vir", "ADV", "Ger"),
                ("dever", "ADV", "Inf"),
                ("estar", "ADV", "Ger"),
                ("haver", "ADV", "Part"),
                ("ir", "ADV", "Inf"),
                ("poder", "ADV", "Inf"),
                ("ser", "ADV", "Part"),
                ("ter", "ADV", "Part"))

    for pattern in patterns:
        index = 0

        while index < len(sentence) - 3:
            if (sentence[index].lemma == pattern[0] and is_verb_or_aux(sentence, index) and
                sentence[index+1].upos == pattern[1] and
                    sentence[index+2].feats.get("VerbForm") and pattern[2] in sentence[index+2].feats.get("VerbForm") and is_verb_or_aux(sentence, index+2)):

                match_results.append(("|".join(
                    pattern), f"{sentence[index].form} {sentence[index+1].form} {sentence[index+2].form}"))

            index += 1

    return match_results


def find_and_write_patterns(conllu, upper_number_of_sentences):
    """
    """

    # for each sentence defined in the conllu object...
    for sentence in conllu:
        # analyses the sentence and get the matching patterns, and what
        # n-gram was matched
        match_results = analyse_sentence(sentence)

        # writes the sentence and match result in the appropriate file
        write_patterns(sentence, match_results, upper_number_of_sentences)


def main():
    """
    Main function.
    """

    for root, _, files in walk("/home/lucas/repos/poetisa-tools/mini-corpus-builder/corpus"):
        for filename in files:
            # location of the CoNLL-U file
            conllu_location = path.join(root, filename)

            print(conllu_location)

            # uses pyconll to load the CoNLL-U file into an object
            conllu = pyconll.load_from_file(conllu_location)

            # finds every pattern defined in the file
            find_and_write_patterns(conllu, 200)


if __name__ == "__main__":
    main()
