def get_data(obj, key):
    try:
        val = obj[key]
        return val
    except:
        return None