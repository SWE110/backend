import json

import requests
from bs4 import BeautifulSoup

def get_recipes_from_url(url):
    """Returns a list of recipe objects following Google's schema"""
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    json_tag_list = soup.find_all(lambda tag: tag.name == "script" and tag.get("type", "") == "application/ld+json")
    json_obj_list = [json.loads(" ".join(json_tag.text.split())) for json_tag in json_tag_list]
    return [json_obj for json_obj in json_obj_list if json_obj.get("@type", "") == "Recipe"]