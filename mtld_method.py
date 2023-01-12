# coding=utf8
# Rewritten and simplified based on John Frens's code 2017
# https://github.com/jennafrens/lexical_diversity
import string


def remove_punc(text):
    return text.translate(str.maketrans('', '', string.punctuation)).lower()


def convert_to_list(text):
    return text.split()


def mtld_formula(all_tokens, gold_ratio=0.72):
    types = set()
    tokens = []
    factors = 0
    ttr_score = 1  # initial ttr

    for item in all_tokens:
        if item not in types:
            types.add(item)
        tokens.append(item)
        ttr_score = len(types) / len(tokens)
        # print(item, ":", ttr_score)
        if ttr_score <= gold_ratio:
            # print(types)
            factors += 1
            tokens = []
            types = set()
            ttr_score = 1

    # calculating the distance between the ttr score of the last item of the remainder
    # and the gold ratio
    excess = 1.0 - ttr_score
    excess_val = 1.0 - gold_ratio # always 0.28 if gold_ratio =0.72
    # final factor is :
    # print("factors:", factors, " + (remainder of the last ttr_score", ttr_score, "distnce from 1.0 which is", excess, "/", "0.28 =", excess / excess_val, ")")
    factors = factors + (excess / excess_val)
    if factors != 0:
        # final mtld score
        score = len(all_tokens) / factors
        return score
    return -1


def mtld_score(text, gold_ratio=0.72):
    all_tokens = convert_to_list(remove_punc(text))
    # forward calculation
    forward = mtld_formula(all_tokens, gold_ratio)
    # backward calculation
    backward = mtld_formula(all_tokens[::-1], gold_ratio)
    # final score
    return (forward + backward) / 2


if __name__ == '__main__':
    pass
    # sample = 'In sum, all textual analyses are fraught with difficulty and disagreement, and LD is no exception. There is no agreement in the field as to the form of processing (sequential or nonsequential) or the composition of lexical terms (e.g., words, lemmas, bigrams, etc.); and even a common position with regard to the distinction between the terms lexical diversity, vocabulary diversity, and lexical richness remains unclear (Malvern et al., 2004). In this study, we do not attempt to remedy these issues. Instead, we argue that the field is sufficiently young to be still in need of exploring its potential to inform substantially. Thus, we include in our analyses the most sophisticated indices of LD that are currently available.'
    # sample = 'this mountain is very big and the scene is very good and there is a Lake lake is very beautiful and beside there is a Tree and over there I see the big mountain there is a very beautiful and this Taro’s room before is Taro’s name on textbook but'
    # sample = 'this mountain is very big and the scene is very'
    # sample = 'of the people, by the people, for the people '
    # sample= "Baby Shark doo doo doo doo doo doo Baby Shark doo doo doo doo doo doo Baby Shark doo doo doo doo doo doo Baby Shark! Mommy Shark doo doo doo doo doo doo Mommy Shark doo doo doo doo doo doo Mommy Shark doo doo doo doo doo doo Mommy Shark! Daddy Shark doo doo doo doo doo doo Daddy Shark doo doo doo doo doo doo Daddy Shark doo doo doo doo doo doo Daddy Shark! GrandMa Shark doo doo doo doo doo doo GrandMa Shark doo doo doo doo doo doo GrandMa Shark doo doo doo doo doo doo GrandMa Shark doo doo doo doo doo doo GrandMa Shark! GrandPa Shark doo doo doo doo doo doo GrandPa Shark doo doo doo doo doo doo GrandPa Shark doo doo doo doo doo doo GrandPa Shark doo doo doo doo doo doo GrandPa Shark! Let's go hunt doo doo doo doo doo doo Let's go hunt doo doo doo doo doo doo Let's go hunt doo doo doo doo doo doo Let's go hunt doo doo doo doo doo doo Let's go hunt doo doo doo doo doo doo Let's go hunt! Run away doo doo doo doo doo doo Run away doo doo doo doo doo doo Run away doo doo doo doo doo doo Run away! Safe at last doo doo doo doo doo doo Safe at last doo doo doo doo doo doo Safe at last doo doo doo doo doo doo Safe at last! It's the end doo doo doo doo doo doo It's the end doo doo doo doo doo doo It's the end doo doo doo doo doo doo It's the end doo doo doo doo doo doo It's the end! Baby Shark doo doo doo doo doo doo Baby Shark doo doo doo doo doo doo Baby Shark doo doo doo doo doo doo Baby Shark! Mommy Shark doo doo doo doo doo doo Mommy Shark doo doo doo doo doo doo Mommy Shark doo doo doo doo doo doo Mommy Shark! Daddy Shark doo doo doo doo doo doo Daddy Shark doo doo doo doo doo doo Daddy Shark! GrandMa Shark doo doo doo doo doo doo GrandMa Shark doo doo doo doo doo doo GrandMa Shark doo doo doo doo doo doo GrandMa Shark doo doo doo doo doo doo GrandMa Shark! GrandPa Shark doo doo doo doo doo doo GrandPa Shark doo doo doo doo doo doo GrandPa Shark doo doo doo doo doo doo GrandPa Shark! Let's go hunt doo doo doo doo doo doo Let's go hunt doo doo doo doo doo doo Let's go hunt doo doo doo doo doo doo Let's go hunt doo doo doo doo doo doo Let's go hunt! Run away doo doo doo doo doo doo Run away doo doo doo doo doo doo Run away doo doo doo doo doo doo Run away! Safe at last doo doo doo doo doo doo Safe at last doo doo doo doo doo doo Safe at last doo doo doo doo doo doo Safe at last doo doo doo doo doo doo Safe at last! It's the end doo doo doo doo doo doo It's the end doo doo doo doo doo doo It's the end doo doo doo doo doo doo It's the end! Baby Shark doo doo doo doo doo doo Baby Shark doo doo doo doo doo doo Baby Shark doo doo doo doo doo doo Baby Shark doo doo doo doo doo doo Baby Shark doo doo doo doo doo doo Baby Shark! Mommy Shark doo doo doo doo doo doo Mommy Shark doo doo doo doo doo doo Mommy Shark doo doo doo doo doo doo Mommy Shark doo doo doo doo doo doo Mommy Shark! Daddy Shark doo doo doo doo doo doo Daddy Shark doo doo doo doo doo doo Daddy Shark doo doo doo doo doo doo Daddy Shark doo doo doo doo doo doo Daddy Shark! GrandMa Shark doo doo doo doo doo doo GrandMa Shark doo doo doo doo doo doo GrandMa Shark doo doo doo doo doo doo GrandMa Shark doo doo doo doo doo doo GrandMa Shark! GrandPa Shark doo doo doo doo doo doo GrandPa Shark doo doo doo doo doo doo GrandPa Shark doo doo doo doo doo doo GrandPa Shark doo doo doo doo doo doo GrandPa Shark! Let's go hunt doo doo doo doo doo doo Let's go hunt doo doo doo doo doo doo Let's go hunt doo doo doo doo doo doo Let's go hunt doo doo doo doo doo doo Let's go hunt! Run away doo doo doo doo doo doo Run away doo doo doo doo doo doo Run away doo doo doo doo doo doo Run away doo doo doo doo doo doo Run away doo doo doo doo doo doo Run away! Safe at last doo doo doo doo doo doo Safe at last doo doo doo doo doo doo Safe at last doo doo doo doo doo doo Safe at last doo doo doo doo doo doo Safe at last! It's the end doo doo doo doo doo doo It's the end doo doo doo doo doo doo It's the end doo doo doo doo doo doo It's the end doo doo doo doo doo doo It's the end! Baby Shark doo doo doo doo doo doo doo Baby Shark doo doo doo doo doo doo doo Baby Shark doo doo doo doo doo doo doo Baby Shark! Mommy Shark doo doo doo doo doo doo Mommy Shark doo doo doo doo doo doo Mommy Shark doo doo doo doo doo doo Mommy Shark doo doo doo doo doo doo Mommy Shark! Daddy Shark doo doo doo doo doo doo Daddy Shark doo doo doo doo doo doo Daddy Shark doo doo doo doo doo doo Daddy Shark doo doo doo doo doo doo Daddy Shark! GrandMa Shark doo doo doo doo doo doo GrandMa Shark doo doo doo doo doo doo GrandMa Shark doo doo doo doo doo doo GrandMa Shark! GrandPa Shark doo doo doo doo doo doo GrandPa Shark doo doo doo doo doo doo GrandPa Shark doo doo doo doo doo doo GrandPa Shark doo doo doo doo doo doo GrandPa Shark doo doo doo doo doo doo GrandPa Shark! Let's go hunt doo doo doo doo doo doo Let's go hunt doo doo doo doo doo doo Let's go hunt doo doo doo doo doo doo Let's go hunt doo doo doo doo doo doo Let's go hunt Run away doo doo doo doo doo doo Run away doo doo doo doo doo doo Run away doo doo doo doo doo doo Run away doo doo doo doo doo doo Run away! Safe at last doo doo doo doo doo doo Safe at last doo doo doo doo doo doo Safe at last doo doo doo doo doo doo Safe at last doo doo doo doo doo doo Safe at last! It's the end doo doo doo doo doo doo It's the end doo doo doo doo doo doo It's the end doo doo doo doo doo doo It's the end doo doo doo doo doo doo It's the end!"
    # print(mtld_score(sample))

