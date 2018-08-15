import json
import pdb

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
    #removing noisy data
    #...
    #...
    #...
    data_label = []
    #divide data into 2 types: text and tabular
    data_text = []
    data_tabular = []
    for item in data["products"]:
        tmp = dict()
        tmp_2 = dict()
        if item["store"] is not None:
            tmp_2["store"] = item["store"]
        else:
            tmp_2["store"] = "__"
        tmp["name"] = item["name"]
        tmp_2["brand"] = item["brand"]
        tmp["top_description"] = item["top_description"]
        tmp_2["base_category"] = item["base_category"]
        tmp_2["location"] = item["location"]
        if len(item["price"]) >= 1:
            tmp_2["current_price"] = item["price"][len(item["price"]) - 1]["current"]
            tmp_2["original_price"] = item["price"][len(item["price"]) - 1]["origin"]
        else:
            tmp_2["current_price"] = 0
            tmp_2["original_price"] = 0
        tmp["feature_description"] = item["feature_description"]
        data_text.append(tmp)
        data_tabular.append(tmp_2)
        data_label.append(item["label_category"])
    return data_text, data_tabular, data_label