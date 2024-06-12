""" Resturcture JSON for Req Body """
# MyAnimeList.json -> ReMyAnimeList.json
# 1. determine what the req body stucture based on ChatGPT intepretation
# 2. modify the current json to match the structure given by chatgpt
# 3. try to add req body to api

import json

# Transforming the data to fit the AnimeCreate model
def transform_data(data):
    transformed_data = {
        "title_ov": data.get("title_ov"),
        "title_en": data.get("title_en"),
        "synopsis": data.get("synopsis"),
        "picture_url": data.get("picture_url"),
        "alternative_titles": {
            "synonym": data["alternative_titles"].get("synonyms"),
            "japanese": data["alternative_titles"].get("japanese")
        } if data.get("alternative_titles") else None,
        "information": {
            "aired": data["information"].get("aired"),
            "episode": int(data["information"]["episodes"]) if data["information"].get("episodes", "").isdigit() else None,
            "broadcast": data["information"].get("broadcast"),
            "status": {
                "name": data["information"]["status"]
            } if data["information"].get("status") else None,
        } if data.get("information") else None,
        "type": {
            "name": data["information"]["type"][0]["name"],
            "url": data["information"]["type"][0]["url"]
        } if data.get("information") and isinstance(data["information"].get("type"), list) and len(data["information"]["type"]) > 0 else None,
        "premiered": {
            "name": data["information"]["premiered"][0]["name"],
            "url": data["information"]["premiered"][0]["url"]
        } if data.get("information") and isinstance(data["information"].get("premiered"), list) and len(data["information"]["premiered"]) > 0 else None,
        "producers": [
            {"name": producer["name"], "url": producer.get("url")}
            for producer in data["information"].get("producers", []) if isinstance(producer, dict)
        ] if data.get("information") else [],
        "studios": [
            {"name": studio["name"], "url": studio.get("url")}
            for studio in data["information"].get("studios", []) if isinstance(studio, dict)
        ] if data.get("information") else [],
        "genres": [
            {"name": genre["name"], "url": genre.get("url")}
            for genre in data["information"].get("genres", []) if isinstance(genre, dict)
        ] if data.get("information") else [],
        "demographics": [
            {"name": demographic["name"], "url": demographic.get("url")}
            for demographic in data["information"].get("demographic", []) if isinstance(demographic, dict)
        ] if data.get("information") else [],
    }
    return transformed_data

# Reading data from JSON file
with open('scripts/data/MyAnimeList/MyAnimeList.json', 'r') as file:
    data = json.load(file)

# Transform the data
# transformed_data = transform_data(data)
transformed_data_list = [transform_data(data) for data in data]

# Define the path to the output JSON file
output_file_path = 'scripts/data/MyAnimeList/ReMyAnimeList.json'

# Write json_data to the output file
with open(output_file_path, "w") as output_file:
    json.dump(transformed_data_list, output_file, indent=4)

print("JSON data has been saved to", output_file_path)