import json
import pdb
from sklearn.feature_extraction.text import TfidfVectorizer

def tabular_type_statistic(data_tabular, data_tabular_feature_name):
    tabular_type = dict()
    for feature in data_tabular_feature_name:
        tabular_type[feature] = dict()
        for item in data_tabular:
            if item[feature] not in tabular_type[feature]:
                tabular_type[feature][item[feature]] = 1
            else:
                tabular_type[feature][item[feature]] += 1
    return tabular_type

def load_and_preprocess_data(dir="./config/products.json"):
    #open and load json file
    data = None
    with open("./config/products.json",'r') as f:
        data = json.load(f)
    
    #count category
    cat = dict()
    for item in data["products"]:
        if str(item["label_category"]) not in cat:
            cat[str(item["label_category"])] = 1
        else:
            cat[str(item["label_category"])] += 1

    #remove label_category whose quantity is low
    removed_cat = []
    for mem in cat:
        if cat[mem] <= 2: #based on observation
            removed_cat.append(mem)
    for item in data["products"]:
        if str(item["label_category"]) in removed_cat:
            del item

    #divide data into 2 types: text and tabular
    data_label = []
    data_text = []
    data_tabular = []
    data_text_feature_name = ["name","top_description","feature_description"]
    data_tabular_feature_name = ["store","brand","base_category","location","current_price","original_price"]
    for item in data["products"]:
        text_type = dict()
        tabular_type = dict()
        if item["store"] is not None:
            tabular_type["store"] = item["store"]
        else:
            tabular_type["store"] = "__"
        text_type["name"] = item["name"]
        tabular_type["brand"] = item["brand"]
        text_type["top_description"] = item["top_description"]
        tabular_type["base_category"] = item["base_category"]
        tabular_type["location"] = item["location"]
        if len(item["price"]) >= 1:
            tabular_type["current_price"] = item["price"][len(item["price"]) - 1]["current"]
            tabular_type["original_price"] = item["price"][len(item["price"]) - 1]["origin"]
        else:
            tabular_type["current_price"] = 0
            tabular_type["original_price"] = 0
        text_type["feature_description"] = item["feature_description"]
        data_text.append(text_type)
        data_tabular.append(tabular_type)
        data_label.append(item["label_category"])
    
    #preprocessing tabular data##################################################################################
    tabular_statistic = tabular_type_statistic(data_tabular,data_tabular_feature_name)
    #converting brand to number
    brand_name = []
    for brand in tabular_statistic["brand"]:
        brand_name.append(brand)
    #converting base category to number
    base_category = []
    for b_c in tabular_statistic["base_category"]:
        base_category.append(b_c)
    #converting store to number
    store_name = []
    for store in tabular_statistic["store"]:
        store_name.append(store)
    #converting location to number
    location_name = []
    for location in tabular_statistic["location"]:
        location_name.append(location)
    for item in data_tabular:
        item["brand"] = brand_name.index(item["brand"])
        item["base_category"] = base_category.index(item["base_category"])
        item["store"] = store_name.index(item["store"])
        item["location"] = location_name.index(item["location"])
    ####################################################################################################################

    #preprocessing text data############################################################################################
    #grouping name, top_description and feature_description
    name = []
    top_description = []
    feature_description = []
    for item in data_text:
        name.append(item["name"])
        top_description.append(item["top_description"])
        feature_description.append(item["feature_description"])
    name = TfidfVectorizer(input=name, encoding='utf-8')
    top_description = TfidfVectorizer(input=top_description, encoding='utf-8')
    feature_description = TfidfVectorizer(input=feature_description, encoding='utf-8')
    pdb.set_trace()
    return data_text,data_text_feature_name, data_tabular, data_tabular_feature_name, data_label

