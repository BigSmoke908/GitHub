test_list = [[42, 23, 12], [69, 17, 13], [18, 21, 9]]
needed = [[42, 23], [18, 21]]


def check(element):
    if [element[0], element[1]] in needed:
        return True
    return False


gefiltert = list(filter(check, test_list))
print(gefiltert)
