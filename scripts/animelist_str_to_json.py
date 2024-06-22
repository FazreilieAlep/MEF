""" converting json string to json"""
import json
import ast

def convert_to_json(string_list):
    json_output = []
    for item in string_list:
        # item = item.replace("'", "\"").replace("\\n", "\n").replace("\\r", "\r").replace("\\", "\\\\").replace("\\s","\s")
        item = item.replace('\\"', "'")
        dictionary = ast.literal_eval(item)
        json_output.append(dictionary)
    return json_output

toJSONfile = 'data/MyAnimeListB2/MyAnimeList.json'

with open(toJSONfile, 'r') as f:
    data = json.load(f)

json_data = convert_to_json(data)
print(json_data)

# Define the path to the output JSON file
output_file_path = "data/MyAnimeListB2/MyAnimeList.json"

# Write json_data to the output file
with open(output_file_path, "w") as output_file:
    json.dump(json_data, output_file, indent=4)

print("JSON data has been saved to", output_file_path)