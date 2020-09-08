import json


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
        ingredients_detailed = recipe_list[i]["ingredients_detailed"]
        ingredients = set()
        for ingredient_detailed in ingredients_detailed:
            try:
                ingredient = ingredient_detailed["ingredients"][0]
                ingredients.add(ingredient.lower().replace(" ", "-"))
            except:
                pass
        recipes_list_feature_selected.append(
            {
                "id": i,
                "title": recipe_list[i]["title"],
                "ingredients": list(ingredients),
                "instructions": recipe_list[i]["instructions"],
                "url": recipe_list[i]["url"],
                "photo": recipe_list[i]["photo_url"],
            }
        )
    return recipes_list_feature_selected


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
    recipe_list = read_raw_data("data/cookstr-recipes.json")
    recipe_list = feature_selection(recipe_list)
    write_json_data(recipe_list, "data/cookstr-data.json")
    corpus_list = load_into_corpus_list(recipe_list)
    write_json_data(corpus_list, "data/cookstr-corpus.json")


if __name__ == "__main__":
    main()
