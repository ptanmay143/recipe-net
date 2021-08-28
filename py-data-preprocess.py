import json
from nltk.tokenize import RegexpTokenizer


def read_raw_data(filename):
    with open(filename, "r", encoding="utf8") as data_file:
        data_file_lines = data_file.readlines()
    recipe_list = []
    for line in data_file_lines:
        recipe_list.append(json.loads(line))
    return recipe_list


def write_json_data(json_data, filename):
    with open(filename, "w", encoding="utf8") as data_outfile:
        json.dump(json_data, data_outfile, indent=4)


def feature_selection(recipe_list):
    recipes_list_feature_selected = []
    for i in range(len(recipe_list)):
        ingredients_detailed = recipe_list[i]["ingredient"]
        ingredients = []
        for ingredient_detailed in ingredients_detailed:
            try:
                ingredient = ingredient_detailed["ingredients"][0]
                ingredients.append(ingredient)
            except:
                ingredient = ""
                ingredients.append(ingredient)
        ingredients = list(filter(None, ingredients))
        recipes_list_feature_selected.append(
            {
                "id": i,
                "title": recipe_list[i]["title"],
                "ingredients": ingredients,
                "instructions": recipe_list[i]["instructions"],
                "url": recipe_list[i]["url"],
                "photo": recipe_list[i]["photo_url"],
            }
        )
    return recipes_list_feature_selected


def tokenization(recipe_list):
    tokenizer = RegexpTokenizer(r"\\w+")
    recipe_list_tokenized = recipe_list
    for recipe, recipe_tokenized in zip(recipe_list, recipe_list_tokenized):
        ingredient_list = list(set(recipe["ingredients"]))
        ingredient_list_tokenized = []
        for ingredient in ingredient_list:
            ingredient_tokenized = "-".join(
                tokenizer.tokenize(ingredient.lower()))
            ingredient_list_tokenized.append(ingredient_tokenized)
        ingredient_list_tokenized = list(set(ingredient_list_tokenized))
        recipe_tokenized["ingredients"] = ingredient_list_tokenized
    return recipe_list_tokenized


def load_into_corpus_list(recipe_list):
    corpus_set = set()
    for recipe in recipe_list:
        corpus_set.update(set(recipe["ingredients"]))
    corpus_list_sorted = sorted(corpus_set, reverse=True)
    corpus_list = []
    for id, item in zip(range(len(corpus_list_sorted)), corpus_list_sorted):
        corpus_list.append({"id": id, "text": item})
    return corpus_list


def main():
    recipe_list = read_raw_data("data/raw.json")
    recipe_list = feature_selection(recipe_list)
    recipe_list = tokenization(recipe_list)
    write_json_data(recipe_list, "data/data.json")
    corpus_list = load_into_corpus_list(recipe_list)
    write_json_data(corpus_list, "data/corpus.json")


if __name__ == "__main__":
    main()
