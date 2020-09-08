import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


def read_json_data(filename):
    with open(filename, "r", encoding="utf8") as data_file:
        json_list = json.load(data_file)
    return json_list


def load_into_ingredients_list(recipe_list):
    ingredients_list = []
    for recipe in recipe_list:
        ingredients_list.append(recipe["ingredients"])
    return ingredients_list


def temp_function(doc):
    return doc


def calculate_tf_idf(ingredients_list):
    tf_idf = TfidfVectorizer(
        analyzer="word",
        tokenizer=temp_function,
        preprocessor=temp_function,
        token_pattern=None,
    )
    tf_idf.fit(ingredients_list)
    tf_idf_matrix = tf_idf.transform(ingredients_list)
    pickle.dump(
        tf_idf, open("data/tf_idf.pickle", "wb"),
    )
    pickle.dump(
        tf_idf_matrix, open("data/tf_idf_matrix.pickle", "wb"),
    )


def main():
    recipe_list = read_json_data("data/cookstr-data.json")
    ingredients_list = load_into_ingredients_list(recipe_list)
    calculate_tf_idf(ingredients_list)


if __name__ == "__main__":
    main()
