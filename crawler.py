from bs4 import BeautifulSoup
import requests
import json
import bs4

#method from scraper.py 
def get_recipes_from_url(url):
    """Returns a list of recipe objects following Google's schema"""
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, "html.parser")
    json_tag_list = soup.find_all(lambda tag: tag.name == "script" and tag.get("type", "") == "application/ld+json")
    json_obj_list = [json.loads(" ".join(json_tag.text.split())) for json_tag in json_tag_list]
    return [json_obj for json_obj in json_obj_list if json_obj.get("@type", "") == "Recipe"]

def get_category_urls(source_link):
    """Returns a list of links to the recipes"""
    source_response = requests.get(source_link, timeout=5)
    # source_soup = BeautifulSoup(source_response.text, "lxml")
    source_soup = BeautifulSoup(source_response.text, "html.parser")
    source_cells = source_soup.find("div", {"class": "subnav"}).find_all('a')

    link_list = []
    for link in source_cells:
        link_list.append(link['href'])

    new_list = []
    for i in range(1, 9):
        new_list.append(link_list[i])

    recipe_list = []
    recipe_url = []
    for i in range(0, len(new_list)):
        recipe_link = new_list[i]
        recipe_response = requests.get(recipe_link, timeout=5)
        # recipe_soup = BeautifulSoup(recipe_response.text, "lxml")
        recipe_soup = BeautifulSoup(recipe_response.text, "html.parser")
        recipe_cells = recipe_soup.find_all('a', {'class': 'module__link'})

        for links in recipe_cells:
            recipe_list.append(links['href'])

        for j in range(0, len(recipe_list)):
            if recipe_list[j] not in recipe_url:
                recipe_url.append(recipe_list[j])
    return recipe_url

def get_recipes(recipe_url):
    """Returns a list of a list of recipe objects follosing Google's schema"""
    recipe_array = []
    for i in range(0, len(recipe_url)):
        try:            
            url = recipe_url[i]
            print("Scraping recipe from %s" % (url))
            res = get_recipes_from_url(url)
            recipe_array.append(res[0])
        except:
            pass
    return recipe_array

if __name__ == '__main__':
    source_link = "https://www.seriouseats.com/"
    recipes = get_recipes(get_category_urls(source_link))
    with open('recipes.txt', 'w') as fout:
        json.dump(recipes, fout)


