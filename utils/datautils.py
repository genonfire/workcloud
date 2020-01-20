

def search_dict(key, value, list_of_dict):
    for item in list_of_dict:
        if item[key] == value:
            return item
