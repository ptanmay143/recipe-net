import json
import sys
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy


def read_json_data(filename):
    with open(filename, "r", encoding="utf8") as data_file:
        json_list = json.load(data_file)
    return json_list


def data_pre_processing():
    user_choice_list = [int(s) for s in sys.argv[1].split(",")]
    corpus_list = read_json_data("data/cookstr-corpus.json")
    ingredient_list = []
    for item in corpus_list:
        if item["id"] in user_choice_list:
            ingredient_list.append(item["text"])
    ingredients_list = [ingredient_list]
    return ingredients_list


def temp_function(doc):
    return doc


def calculate_cos_sim(ingredients_list):
    tf_idf = pickle.load(open("data/tf_idf.pickle", "rb"))
    tf_idf_matrix_corpus = pickle.load(open("data/tf_idf_matrix.pickle", "rb"))
    tf_idf_matrix_choice = tf_idf.transform(ingredients_list)
    cos_sim = cosine_similarity(tf_idf_matrix_corpus, tf_idf_matrix_choice)
    max_sim = numpy.argmax(cos_sim)
    return max_sim


def main():
    sys.stdout.flush()
    ingredients_list = data_pre_processing()
    max_sim = calculate_cos_sim(ingredients_list)
    print(str(max_sim).zfill(4))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
