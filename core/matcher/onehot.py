def make_onehot(id_list, source):
    """Make a onehot encoding of data, with vector length equal to classes"""
    arr = [0] * len(source)
    for id in id_list:
        arr[source[str(id)]["id"]] = 1
    return arr