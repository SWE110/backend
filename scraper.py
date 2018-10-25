import sys
import json

import requests
import bs4

def get_recipes_from_url(url):
    """Returns a list of recipe objects following Google's schema"""
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, "html.parser")
    json_tag_list = soup.find_all(lambda tag: tag.name == "script" and tag.get("type", "") == "application/ld+json")
    json_obj_list = [json.loads(" ".join(json_tag.text.split())) for json_tag in json_tag_list]
    return [json_obj for json_obj in json_obj_list if json_obj.get("@type", "") == "Recipe"]

if __name__ == "__main__":
    url = sys.argv[1]
    res = get_recipes_from_url(url)
    json_string = json.dumps(res[0])
    print(json_string)
