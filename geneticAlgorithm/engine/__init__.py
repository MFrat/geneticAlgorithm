def splitter(array, partsize=1):
    return [array[i:i+partsize] for i in range(0, len(array), partsize)]
