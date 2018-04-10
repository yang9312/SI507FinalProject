import requests
from bs4 import BeautifulSoup
import json


# get and store category information(name and detail url)


def get_category_info():
    baseurl = "https://www.esteelauder.com"
    text = requests.get(baseurl).text
    soup = BeautifulSoup(text, "html.parser")
    ctype = soup.find("nav", attrs={"class": "page-navigation"}).find("div",
                      attrs={"class": "content"}).find_all("div", attrs={"class": "menu-reference"})
    suptype_dic = {}

    for suptype in ctype[0:3]:
        name = suptype.find("li").find("a").text  # Skincare, Makeup, Fragrance
        category_lis = suptype.find("div", attrs={"class": "menu-container"}).find_all("li", attrs={"class": "expanded"})
        category_dic = {}

        for category in category_lis:
            category_name = category.find("h3").text  # By Categary, By Concern, Collection
            subtype_lis = category.find_all("li")
            category_info_lis = []

            for subtype in subtype_lis:
                subtype_name = subtype.find("a").text.strip()  # Repair Serum
                subtype_url = subtype.find("a")["href"]  # url for subtype

                subtype_dic = {"SubtypeName": subtype_name, "SubtypeUrl": subtype_url}
                category_info_lis.append(subtype_dic)

            category_dic.update({category_name: category_info_lis})

        suptype_dic.update({name: category_dic})

    return suptype_dic


if __name__ == "__main__":
    fw = open("category_info.json", "w")
    content = get_category_info()
    fw.write(json.dumps(content, indent=4))
    fw.close()
