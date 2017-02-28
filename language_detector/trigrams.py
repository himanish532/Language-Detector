#!/usr/bin/env python

import collections
import logging
import math
import os
import re
from optparse import OptionParser


def create_model(path):
    # defining a list "model" to append the counts of unigrams, bigrams and trigrams
    model = []
    unigrams = collections.defaultdict(int)
    # defining dictionary(dictionary)
    bigrams = collections.defaultdict(lambda: collections.defaultdict(int))
    # defining dictionary of bigrams dictionary
    trigrams = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))

    # reading each line in the file
    f = open(path, 'r')
    for l in f.readlines():
        # punctuation script
        l = l.lower()
        l = re.sub('[\W][0-9]*', "", l)

        # tokenize the text:
        tokens = l.split(" ")

        # loop over Unigrams
        for word in tokens:
            word = '$$' + word + '$$'
            for i in range(len(word)):
                unigrams[word[i]] += 1
                # bigram = [word[i]][word[i + 1]] + 1
                if i < (len(word) - 1):
                    bigrams[word[i]][word[i + 1]] += 1
                if i < (len(word) - 2):
                    trigrams[word[i]][word[i + 1]][word[i + 2]] += 1

                model.append(unigrams)
                model.append(bigrams)
                model.append(trigrams)

    return model


def predict(file, model_en, model_es):
    prediction = None

    # Declaring calc_prob function which returns the probability values
    prob_en = calc_prob(file, model_en)
    prob_es = calc_prob(file, model_es)

    if prob_en > prob_es:
        print "Probability difference" + " " + str(prob_en - prob_es)
        prediction = "Its in English"
    else:
        print "Probability difference" + " " + str(prob_es - prob_en)
        prediction = "Its in Spanish"

    return prediction


def calc_prob(file, model):
    # assigning the unigrams and bigrams count into the local variables
    a = model[0]
    b = model[1]
    c = model[2]
    prob = 0.0
    prob1 = 0.0
    f = open(file, 'r')
    for l in f.readlines():
        # language build
        l = l.lower()
        l = re.sub('[\W][0-9]*', "", l)

        # tokenizing the string
        tokens = l.split(" ")

        # loop over to calculate the probability value of the model
        for word in tokens:
            word = '$$' + word + '$$'
            for i in range(len(word) - 2):
                prob1 = float(c[word[i]][word[i + 1]][word[i + 2]] + 1) / (b[word[i]][word[i + 1]] + 27)
                prob += float(math.log1p(prob1 - 1))

    return prob


def main(en_tr, es_tr, folder_te):
    # STEP 1: create a model for English with file en_tr
    model_en = create_model(en_tr)

    # STEP 2: create a model for Spanish with file es_tr
    model_es = create_model(es_tr)

    # STEP 3: loop through all the files in folder_te and print prediction
    folder = os.path.join(folder_te, "en")
    print "Prediction for English documents in test:"
    for f in os.listdir(folder):
        f_path = os.path.join(folder, f)
        print "%s\t%s" % (f, predict(f_path, model_en, model_es))

    folder = os.path.join(folder_te, "es")
    print "\nPrediction for Spanish documents in test:"
    for f in os.listdir(folder):
        f_path = os.path.join(folder, f)
        print "%s\t%s" % (f, predict(f_path, model_en, model_es))


if __name__ == "__main__":
    usage = "usage: %prog [options] EN_TR ES_TR FOLDER_TE"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug", action="store_true",
                      help="turn on debug mode")

    (options, args) = parser.parse_args()
    if len(args) != 3:
        parser.error("Please provide required arguments")

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    main(args[0], args[1], args[2])
