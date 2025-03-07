import http.client
import json
import pandas as pd
import ast
import os


""" FUNCTIONS """
# Convert Fetched String to JSON
def convert_to_json(string_list):
    json_output = []
    for item in string_list:
        # item = item.replace("'", "\"").replace("\\n", "\n").replace("\\r", "\r").replace("\\", "\\\\").replace("\\s","\s")
        item = item.replace('\\"', "'")
        dictionary = ast.literal_eval(item)
        json_output.append(dictionary)
    return json_output


# Transforming the data to fit the AnimeCreate ReqBody model
def transform_data(data):
    transformed_data = {
        "myanimelist_id": data.get("myanimelist_id"),
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


""" 
    fetch new anime data here
    Ensure to update headers, toJSONfile

"""
folder = 'data/MyAnimeListB3'
toReJSONfile = folder + '/ReMyAnimeList2.json'
toJSONfile = folder + '/MyAnimeList2.json'

# Create the directory if it doesn't exist
os.makedirs(folder, exist_ok=True)

# fromCSVfile = 'data/MyAnimeList_V2.csv'
# df = pd.read_csv(fromCSVfile)  # Replace with your file path
# id_array = df['ID'].to_numpy()

# id_array = [52481, 33206, 35363, 39247, 36793, 37956, 46569, 53126, 50593, 35851, 41361, 38816, 52034, 55791, 57334, 56843, 55830, 53127, 34321, 38084, 38085, 38086, 41497, 40787, 37171, 9989, 15039, 53393, 57524, 37430, 39551, 41487, 53580, 28851, 18671, 14741,35608, 38101, 39783, 48548, 58755, 55887, 58939, 53802, 6045, 20847, 10119, 26123, 30240, 58426, 54968, 6547, 38329, 53129, 54870, 57433, 5081, 110031, 54857]
id_array = [47194, 55830]

# Define the connection and headers
conn = http.client.HTTPSConnection("myanimelist.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "d4be8a60abmshfc3a509129d1717p182a83jsne433b9d98635",
    'x-rapidapi-host': "myanimelist.p.rapidapi.com"
}

# Function to fetch data for a single anime ID
def fetch_anime_data(anime_id):
    conn.request("GET", f"/anime/{anime_id}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

# Loop through the anime IDs and fetch data
anime_data_list = []
for anime_id in id_array:
    try:
        anime_data = fetch_anime_data(str(anime_id))
        anime_data['myanimelist_id'] = anime_id
        anime_data_list.append(str(anime_data))
        print('ok ' + str(anime_id))
    except Exception as e:
        print(f"Error fetching data for anime ID {str(anime_id)}: {e}")

conn.close()


""" converting json string to json"""
json_data = convert_to_json(anime_data_list)
print(json_data)

# Write json_data to the output file
with open(toJSONfile, "w") as output_file:
    json.dump(json_data, output_file, indent=4)

print("JSON data has been saved to", toJSONfile)


""" Resturcture JSON for Req Body """
transformed_data_list = [transform_data(data) for data in json_data]

# Write json_data to the output file
with open(toReJSONfile, "w") as output_file:
    json.dump(transformed_data_list, output_file, indent=4)

print("Restructured JSON data has been saved to", toReJSONfile)



