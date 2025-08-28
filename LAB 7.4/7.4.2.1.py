def sort_list(data, key=None):
    return sorted(data, key=key)
items = [3, "apple", 1, "banana", 2]
print(sort_list(items, key=str))
