import os, random
import nltk
from bs4 import BeautifulSoup
from feature_extraction import *
from nltk import accuracy


def split_data(lang_folders, langs, test_percent=0.2):
    """
    Split the data set into training and test sets, each language has the same ratio of train : test files
    The default percentage of a test set is 20%

    :param lang_folders: A list of folder names
    :param langs: A list of languages
    :param test_percent: A float number of the percentage of the test set, default to 0.2
    :return: a tuple of a train set and a test set
    """
    train_set = []
    test_set = []
    for l in lang_folders:
        if l in langs:
            docs_path = os.path.join(TEST_FOLDER, l)
            docs = os.listdir(docs_path)
            num_test_files = int(test_percent*len(docs))
            train = [(os.path.join(docs_path, f), l) for f in docs[:len(docs) - max(1, num_test_files) + 1]]
            test = [(os.path.join(docs_path, f), l) for f in docs[len(docs) - max(1, num_test_files) + 1:]]
            train_set.extend(train)
            test_set.extend(test)
    return train_set, test_set


def read_file(filename):
    """
    Loads an xml file and checks if it is successfully read, raises an error otherwise.
    :param filename: A string of the name of a file.
    :return: A BeautifulSoup object of parsed xml file.
    """
    annotation_xml = BeautifulSoup(open(filename), "xml")
    if annotation_xml.is_empty_element:
        raise ValueError("Cannot read from file: "+filename)
    return annotation_xml


def find_text(xml_soup, text_tagname="TEXT"):
    """
    Finds the TEXT tag
    :param xml_soup: A BeautifulSoup object
    :param text_tagname: The name of a TEXT tag, default to TEXT
    :return: A string
    train_set = []
    test_set = [] of the text content of the current xml file.
    """
    return xml_soup.find(text_tagname).string


def find_tags(xml_soup, tags_tagname="TAGS"):
    """
    Finds all the annotation tags
    :param xml_soup:
    :param tags_tagname:
    :return: a BeautifulSoup object of the TAGS node.
    """
    return xml_soup.find(tags_tagname).findChildren()


def train_classifier(train_set, classifier=nltk.classify.NaiveBayesClassifier,
                     feature_extract_fun=bag_of_words, limit=100):
    """
    Train the specified classifier using the feature extracted from the training set with feature extraction
    functions

    :param train_set:  A list of file names
    :param classifier: A classifier to be trained
    :param feature_extract_fun: The feature extraction function to be used
    :param limit: A number to be passed to the feature extraction function, specifies the max number of features to use.
    :return: The trained classifier.
    """
    extracted = []
    for t in train_set:
        xml_file = read_file(t[0])
        text = find_text(xml_file)
        tags = find_tags(xml_file)
        extracted.append((feature_extract_fun(text, tags, n=limit), t[1]))
    cf = classifier.train(extracted)

    return cf


def test_classifier(test_set, trained_classifier, feature_extract_fun=bag_of_words, limit = 100):
    """
    Test the trained classifier on the test set, using the specified feature extraction function
    :param test_set: a list of filenames
    :param trained_classifier: the classifier trained in train_classifier.
    :param feature_extract_fun: the funtion used to extract features
    :param limit: the
    :return: a list of tuples of correct and prediction classes.
    """
    results = []
    for t in test_set:
        xml_file = read_file(t[0])
        text = find_text(xml_file)
        tags = find_tags(xml_file)
        predict = trained_classifier.classify(feature_extract_fun(text, tags, n=limit))
        gold = t[1]
        results.append((gold, predict))

    return results


def precision(c, results):
    """
    Calculate the precision for a given class
    :param c: A class in the task
    :param results: A list of 2-tuples of Correct tag/Predicted tag pairs.
    :return: A float number, or -1 if it happens to be division by zero.
    """
    tp = 0
    fp = 0
    fn = 0
    for gold, pred in results:
        if gold == c and gold == pred:
            tp += 1
        elif gold == c and gold != pred:
            fn += 1
        elif gold != c and pred == c:
            fp += 1

    if tp + fp == 0:
        return -1
    else:
        return (1.0*tp)/(tp+fp)


def recall(c, results):
    """
    Calculate the recall for a give class.
    :param c: A class in the task
    :param results: A list of 2-tuples of Correct tag/Predicted tag pairs.
    :return: A float number, or -1 if it happens to be division by zero.
    """
    tp = 0
    fp = 0
    fn = 0
    for gold, pred in results:
        if gold == c and gold == pred:
            tp += 1
        elif gold == c and gold != pred:
            fn += 1
        elif gold != c and pred == c:
            fp += 1
    if tp + fn == 0:
        return -1
    else:
        return (1.0 * tp) / (tp + fn)


def macro_average_f1(langs, results):
    """
    Calculate the macro-averaged F1 score for the current experiment
    :param langs: A list of languages.
    :param results: A list of tuples of correct vs predicted label pairs.
    :return: A float number
    """
    ps = 0
    rs = 0
    count = 0
    for l in langs:
        ps += max(precision(l, results), 0)
        rs += max(recall(l, results), 0)
        count += 1
    average_ps = ps/count
    average_rs = rs/count
    if average_rs + average_ps == 0:
        return -1
    else:
        return (2*average_ps*average_rs)/(average_ps+average_rs)


if __name__ == "__main__":
    TEST_FOLDER = "./data"
    DIRS = os.listdir(TEST_FOLDER)
    LANGS = ["ara", "fra", "hin", "jpn", "spa", "tel", "zho"]
    # change this variable to specify the feature extraction function to be used.
    FEATURE_FUN = with_link_tags
    CLASSIFIER = nltk.classify.NaiveBayesClassifier

    train, test = split_data(DIRS, LANGS, test_percent=0.3)

    random.shuffle(train)
    random.shuffle(test)
    cf = train_classifier(train,classifier=CLASSIFIER, feature_extract_fun=FEATURE_FUN)
    results = test_classifier(test, cf, feature_extract_fun=FEATURE_FUN)
    gold, predictions = zip(*results)
    cm = nltk.ConfusionMatrix(predictions, gold)

    print(cf.most_informative_features(10))
    print(results)
    print("The confusion matrix of the test results:")
    print(cm)
    for l in LANGS:
        p = precision(l, results)
        r = recall(l, results)
        print(l+": ", end="")
        if p == -1:
            print("Precision: N\A", end=" ")
        else:
            print("Precision: {:.3f}".format(p), end=" ")

        if r == -1:
            print("Recall: N\A")
        else:
            print("Recall: {:.3f}".format(r))

    print("Accuracy: {:.3f}". format(accuracy(gold,predictions)))

    f1 = macro_average_f1(LANGS, results)
    if f1 == -1:
        print("Macro-averaged F1: N\A")
    else:
        print("Macro-averaged F1: {:.3}".format(f1))