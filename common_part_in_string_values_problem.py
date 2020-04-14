def compareLength(str_list):
    str_0 = str_list[0].strip()
    str_1 = str_list[1].strip()
    if len(str_0) > len(str_1):
        return (str_1, str_0)
    else:
        return (str_0, str_1)


def findStartIndex(_str, char):
    index_list=[]
    for i in range(len(_str)):
        if _str[i] == char:
            index_list.append(i)
    return index_list


def findCommonLength(short_str, long_str, i, j):
    cl = 1
    try:
        if short_str[i+1] == long_str[j+1]:
            cl += findCommonLength(short_str, long_str, i+1, j+1)
    finally:
        return cl


def findLongestCommonLength(str_list):
    short_str, long_str = compareLength(str_list)
    longest_common_length = 0
    for i in range(len(short_str)):
        char = short_str[i]
        start_index = findStartIndex(long_str, char)
        for j in start_index:
            cl = findCommonLength(short_str, long_str, i, j)
            longest_common_length = cl if cl > longest_common_length else longest_common_length
    return longest_common_length


def main():
    inp_str_list = input("").strip().split()
    print(findLongestCommonLength(inp_str_list))


main()