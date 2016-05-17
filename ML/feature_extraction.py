from collections import Counter
from bs4 import BeautifulSoup
from nltk import ne_chunk, pos_tag


IGNORE = set(("id", "spans", "text"))


def bag_of_words(text, tags, n=100):
    """
    Simple bag of words counting
    :param text: A string
    :param tags: The tags in the current xml file.
    :param n: A number used in feature functions to specify the limit of words to use as features.
    :return: A dictionary of word:count
    """
    counts = Counter()
    words = text.split()
    for w in words:
        counts[w] += 1
    return counts


def bag_of_words_no_gpe(text, tags, n=100):
    """
    Bag of words approach. except names of locations are ignored
    :param text:
    :param tags:
    :param n:
    :return:
    """
    words = text.split()
    pos_tagged = pos_tag(words)
    chunks = ne_chunk(pos_tagged)
    names = set()
    for s in chunks.subtrees(filter=lambda x: x.label() == "GPE"):
        names.add(s.leaves()[0][0])

    counts = Counter()
    for w in words:
        if w not in names:
            counts[w] += 1
    return counts

def most_frequent_words(text, tags, n=100):
    """
    Find the most frequent n words in the document
    :param text:
    :param tags:
    :param n:
    :return:
    """
    bow = bag_of_words(text, tags)
    return dict(bow.most_common(n))


def tag_name_counts(text, tags, n=100):
    """
    Counts of the tags in each document
    :param text:
    :param tags:
    :param n:
    :return:
    """
    counts = Counter()
    for t in tags:
        counts["$" + t.name] += 1
    return counts


def word_tag_counts(text, tags, n=100):
    """
    Counts of tags and counts of words
    :param text:
    :param tags:
    :param n:
    :return:
    """
    wc = list(most_frequent_words(text, tags, n=n).items())
    wc.extend(list(tag_name_counts(text,tags).items()))
    return dict(wc)


def tags_existence(text, tags, n=100):
    """
    Check the existence of each tag, in each document.
    :param text:
    :param tags:
    :param n:
    :return:
    """
    tag_set = {}
    for t in tags:
        tag_set[t.name] = True
    return tag_set


def tag_attr_name_counts(text, tags, n=100):
    """
    Counts of each tag, and the counts of each attribute name
    :param text:
    :param tags:
    :param n:
    :return:
    """
    counts = Counter()
    for t in tags:
        counts[t] += 1
        for a in t.attrs.keys():
            counts[a] += 1
    return counts


def attr_name_existence(text, tags, n=100):
    """
    Check the existence of each attribute name.
    :param text:
    :param tags:
    :param n:
    :return:
    """
    existence = {}
    for t in tags:
        for a in t.attrs.keys():
            if a not in IGNORE:
                existence[a] = True
    return existence


def attr_val_counts(text, tags, n=100):
    """
    Counts of attribute values in all tags for a given document.
    :param text:
    :param tags:
    :param n:
    :return:
    """
    counts = Counter()
    for t in tags:
        for a in t.attrs.keys():
            if a not in IGNORE:
                counts[t[a]] += 1
    return dict(counts.most_common(n))


def count_misspelling(text, tags, n=100):
    """
    Count the types of each misspelling error.
    :param text:
    :param tags:
    :param n:
    :return:
    """
    counts = Counter()
    misspelling_tag = "Misspelling : "
    for t in tags:
        if t.name == "Misspelling":
            if t.has_attr("Error"):
                counts[misspelling_tag+t["Error"]] += 1
    return counts


def count_verb_errors(text, tags, n=100):
    """
    Count each type of verb related error.
    :param text:
    :param tags:
    :param n:
    :return:
    """
    counts = Counter()
    verb_tag = "Verb : "
    for t in tags:
        if t.name == "Verb":
            if t.has_attr("PrepError"):
                counts[verb_tag+t["PrepError"]] += 1
            if t.has_attr("TenseOrFormError"):
                counts[verb_tag+t["TenseOrFormError"]] += 1
            if t.has_attr("MissingSubj") and t["MissingSubj"] == "Yes":
                counts[verb_tag+t["MissingSubj"]] += 1
    return counts

def count_det_errors(text, tags, n=100):
    """
    Count the types of determiner errors in the given document
    :param text:
    :param tags:
    :param n:
    :return:
    """
    counts = Counter()
    det_tag = "Determiner : "
    for t in tags:
        if t.name == "Determiner":
            if t.has_attr("text"):
                counts[det_tag+t["text"]] += 1
            if t.has_attr("CorrectForm"):
                counts[det_tag+t["CorrectForm"]] += 1
            if t.has_attr("OtherCorrectForm"):
                counts[det_tag+t["OtherCorrectForm"]] += 1
    return counts


def count_noun_errors(text, tags, n=100):
    """
    Count the types of noun errors in the given document
    :param text:
    :param tags:
    :param n:
    :return:
    """
    counts = Counter()
    noun_tag = "Noun : "
    for t in tags:
        if t.name == "Noun":
            if t.has_attr("PrepError"):
                counts[noun_tag+t["PrepError"]] += 1
            if t.has_attr("DetError"):
                counts[noun_tag+t["DetError"]] += 1
            if t.has_attr("PlError"):
                counts[noun_tag+t["PlError"]] += 1
            if t.has_attr("GenderError") and t["GenderError"] == "Yes":
                counts[noun_tag+t["GenderError"]] += 1
    return counts


def noun_verb_misspelling_features(text, tags, n=100):
    """
    Count the types of errors for one of Verb, Noun, Misspelling tags.
    :param text:
    :param tags:
    :param n:
    :return:
    """
    noun_features = count_noun_errors(text, tags)
    verb_features = count_verb_errors(text, tags)
    misspelling_features = count_misspelling(text, tags)
    all_features = {}
    all_features.update(noun_features)
    all_features.update(verb_features)
    all_features.update(misspelling_features)

    all_features["VerbErrors"] = sum(verb_features.values())
    all_features["NounErrors"] = sum(noun_features.values())
    all_features["Misspellings"] = sum(misspelling_features.values())

    return all_features


def noun_verb_features(text, tags, n=100):
    """
    Count the error types for each noun tag and verb tag.
    :param text:
    :param tags:
    :param n:
    :return:
    """
    noun_features = count_noun_errors(text, tags)
    verb_features = count_verb_errors(text, tags)

    all_features = {}
    all_features.update(noun_features)
    all_features.update(verb_features)

    all_features["VerbErrors"] = sum(verb_features.values())
    all_features["NounErrors"] = sum(noun_features.values())

    return all_features


def noun_misspelling_features(text, tags, n=100):
    noun_features = count_noun_errors(text, tags)
    misspelling_features = count_misspelling(text, tags)

    all_features = {}
    all_features.update(noun_features)
    all_features.update(misspelling_features)

    all_features["NounErrors"] = sum(noun_features.values())
    all_features["Misspellings"] = sum(misspelling_features.values())

    return all_features


def link_tag_counts(text, tags, n=100):
    """Count the numbers of different kinds of link tags for each document."""
    counts = Counter()
    link_prefix = "Link : "
    link_tags = set(("DetNounLink", "SVDisagreement", "PrepositionLink"))
    for t in tags:
        if t.name in link_tags:
            counts[link_prefix+t.name] += 1
    return counts


def with_link_tags(text, tags, n=100):
    """Similar to noun_misspelling_features, but includes link tag counts as
    well."""

    total = {}
    total.update(noun_verb_misspelling_features(text, tags))
    total.update(link_tag_counts(text, tags))

    return total


def nvdpm_svd(text, tags, n=100):
    """Count each kind of errors in Verb, Noun, Determiner, Misspelling, Preposition and SVDisagreement"""
    allfeatures = {}
    allfeatures.update(noun_verb_misspelling_features(text, tags, n))
    allfeatures.update(count_det_errors(text, tags, n))

    counts = Counter()
    for t in tags:
        if t.name == "SVDisagreement":
            counts[t.name] += 1
        if t.name == "Preposition":
            counts[t.name] += 1
    allfeatures.update(counts)

    return allfeatures



if __name__ == "__main__":
    test_annotation = "31117.xml"
    xml_annotation = BeautifulSoup(open(test_annotation), "xml")
    text = xml_annotation.find("TEXT").string
    tags = xml_annotation.find("TAGS").findChildren()
    print(with_link_tags(text, tags))