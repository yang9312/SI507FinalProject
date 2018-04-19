import requests
from bs4 import BeautifulSoup
import json
import csv
import time


# cache
def load_cache(CACHE_FNAME):
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except Exception:
        CACHE_DICTION = {}
    return CACHE_DICTION


def save_cache(CACHE_DICTION, CACHE_FNAME):
    fw = open(CACHE_FNAME, "w")
    fw.write(json.dumps(CACHE_DICTION, indent=4))
    fw.close()


# get product information
def get_product_data(suptype, suptype_dic):
    CACHE_DICTION = load_cache("{}_cache.json".format(suptype))
    baseurl = "https://www.esteelauder.com"
    suptype_product_lis = []
    for category in suptype_dic:
        for subtype in suptype_dic[category]:
            if subtype["SubtypeName"] in CACHE_DICTION:
                print("Get product basic information in " + subtype["SubtypeName"] + " from cache...")
            else:
                print("Request new product basic information in " + subtype["SubtypeName"] + "...")
                subtype_url = subtype["SubtypeUrl"]
                text = requests.get(baseurl + subtype_url).text
                soup = BeautifulSoup(text, "html.parser")
                content = soup.find("ul", attrs={"class": "mpp__product-grid"})
                product_lis = content.find_all("li", attrs={"class": "mpp__product"}) if content is not None else None

                subtype_product_lis = []
                if product_lis is not None:
                    for p in product_lis:
                        # product brief description
                        p_header = p.find("div", attrs={"class": "product_brief__description"}).find("a")
                        # product primary name
                        p_name = p_header.find("h3").text
                        # product subname
                        p_subname = p_header.find("h4").text if p_header.find("h4") is not None else "Unknown"
                        # product url
                        p_url = p_header["href"]
                        # star rating
                        star = p.find("div", attrs={"class": "product_brief__stars-rating"})
                        star_rating = star["style"][7:][:-1] if star is not None else "0%"
                        count = p.find("span", attrs={"class": "product_brief__reviews-count"})
                        review_count = count.text[1:-1] if count is not None else "0"

                        product = dict(PrimaryName=p_name, SubName=p_subname, StarRating=star_rating,
                                       ReviewCount=review_count, ProductUrl=p_url, SupType=suptype,
                                       SubType=subtype["SubtypeName"])

                        subtype_product_lis.append(product)

                else:
                    product = dict(PrimaryName="Unknown", SubName="Unknown", StarRating="Unknown",
                                   ReviewCount="Unknown", ProductUrl="Unknown", SupType=suptype,
                                   SubType=subtype["SubtypeName"])
                    subtype_product_lis.append(product)

                CACHE_DICTION[subtype["SubtypeName"]] = subtype_product_lis
                save_cache(CACHE_DICTION, "{}_cache.json".format(suptype))

            res = CACHE_DICTION[subtype["SubtypeName"]]
            for p in res:
                suptype_product_lis.append(p)
    return suptype_product_lis


# select product data and add product id
def select_unique_product():
    fil = open("category_info.json", "r").read()
    fil_dic = json.loads(fil)
    raw_pro_lis = []
    for i in fil_dic:
        ip_lis = get_product_data(i, fil_dic[i])
        for j in ip_lis:
            raw_pro_lis.append(j)

    # for product_dic in selected_product_lis:
    for product_dic in raw_pro_lis:        
        temp_url = product_dic["ProductUrl"]
        temp_url_lis = temp_url.split("/")
        try:
            product_id = temp_url_lis[3]
        except:
            product_id = "Unknown"
        product_dic.update({"ProductId": product_id})

    temp_dic = {}
    selected_product_lis = []
    for product in raw_pro_lis:
        if product["ProductId"] not in temp_dic and product["PrimaryName"] != "Unknown":
            selected_product_lis.append(product)
            temp_dic[product["ProductId"]] = 0

    return selected_product_lis


# get review information
def get_review_data():
    CACHE_DICTION = load_cache("review_cache.json")
    p_lis = select_unique_product()
    review_lis = []
    for p in p_lis:
        if p["ProductId"] in CACHE_DICTION:
            print("Get review for product (" + p["ProductId"] + ") from cache...")
        else:
            print("Request new review information for product (" + p["ProductId"] + ")...")
            url = "https://api.bazaarvoice.com/data/reviews.json?filter=ProductId:{}".format(p["ProductId"])
            param_dic = dict(filter="rating:gte:4&ReviewText:neq:%22%22", apiversion="5.4", Limit="100",
                             ContentLocale="en_US", passkey="36ny78oy0qlhkz86za07gl7ep", include="products")
            for pa in param_dic:
                url += "&" + pa + "=" + param_dic[pa]
            text = requests.get(url).text
            review_info = json.loads(text)["Results"]
            re_lis = []
            for re in review_info:
                age = re["ContextDataValues"].get("Age", "Unknown")
                age = age["Value"] if age != "Unknown" else age
                skintype = re["ContextDataValues"].get("Type", "Unknown")
                skintype = skintype["Value"] if skintype != "Unknown" else skintype
                using_year = re["ContextDataValues"].get("Using", "Unknown")
                using_year = using_year["Value"] if using_year != "Unknown" else using_year
                re_dic = dict(UserNickname=re["UserNickname"], ProductId=p["ProductId"],
                              Rating=re["Rating"], Skintype=skintype, Age=age, UsingYear=using_year)
                re_lis.append(re_dic)

            CACHE_DICTION[p["ProductId"]] = re_lis
            save_cache(CACHE_DICTION, "review_cache.json")
        
        res = CACHE_DICTION[p["ProductId"]]
        for r in res:
            review_lis.append(r)
        #time.sleep(5)
    return review_lis
                

if __name__ == "__main__":
    get_review_data()
    pro_lis = select_unique_product()
    product_fil = open("product.csv", "w")
    fil_header = ["PrimaryName", "SubName", "ProductId", "StarRating",
                  "ReviewCount", "ProductUrl", "SupType", "SubType"]
    fil_writer = csv.DictWriter(product_fil, fil_header)
    fil_writer.writeheader()
    fil_writer.writerows(pro_lis)
    product_fil.close()
