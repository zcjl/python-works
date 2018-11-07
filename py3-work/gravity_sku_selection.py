# coding=utf-8

from itertools import combinations
import numpy as np


class SKU:
    def __init__(self, name, gravity, deviation):
        self.name = name
        self.gravity = gravity
        self.deviation = deviation

    def __repr__(self):
        return "<SKU name:%s gravity:%d deviation:%d>" % (self.name, self.gravity, self.deviation)

    def __str__(self):
        return "SKU: name is %s, gravity is %d, deviation is %d" % (self.name, self.gravity, self.deviation)


def get_test_sku_list():
    test_sku_list = list()
    test_sku_list.append(SKU('a', 3000, 5))
    test_sku_list.append(SKU('bb', 1850, 5))
    test_sku_list.append(SKU('ccc', 2750, 5))
    test_sku_list.append(SKU('dddd', 1650, 5))
    test_sku_list.append(SKU('eeeee', 456, 5))
    test_sku_list.append(SKU('ffffff', 130, 5))
    test_sku_list.append(SKU('ggggggg', 433, 5))
    test_sku_list.append(SKU('hhhhhhhh', 500, 5))
    test_sku_list.append(SKU('iiiiiiiii', 567, 5))
    # test_sku_list.append(SKU('jjjjjjjjjj', 4567, 5))
    # test_sku_list.append(SKU('kkkkkkkkkkk', 3456, 5))
    # test_sku_list.append(SKU('llllllllllll', 2345, 5))
    # test_sku_list.append(SKU('mmmmmmmmmmmmm', 1234, 5))
    # test_sku_list.append(SKU('nnnnnnnnnnnnnn', 6543, 5))
    return test_sku_list


def check_gravity(sku_group):
    sku_a = all_sku_list[sku_group[0]]
    sku_b = all_sku_list[sku_group[1]]
    num_a = 20 * 1000 // sku_a.gravity
    num_b = 20 * 1000 // sku_b.gravity
    for a in range(num_a):
        min_a = (sku_a.gravity - sku_a.deviation) * (a + 1)
        max_a = (sku_a.gravity + sku_a.deviation) * (a + 1)
        for b in range(num_b):
            min_b = (sku_b.gravity - sku_b.deviation) * (b + 1)
            max_b = (sku_b.gravity + sku_b.deviation) * (b + 1)
            if (min_a <= min_b <= max_a) or (min_a <= max_b <= max_a):
                # print(sku_group)
                # print(num_a, num_b)
                # print(a, b, min_a, max_a, min_b, max_b)
                return False
    return True


def check_all_set(item):
    result_list = list()
    for sku_group in item:
        if check_gravity(sku_group):
            result_list.append(sku_group)
        if len(result_list) >= len(item):
            print(result_list, [[all_sku_list[x[0]].name, all_sku_list[x[1]].name] for x in result_list])
            return True
    return False


def get_combinations(index_range, sku_per_group, count_of_groups):
    list_a = list(range(index_range))
    list_b = list(combinations(list_a, sku_per_group))
    list_c = list(filter(lambda x: len(np.unique(x)) == count_of_groups * 2, combinations(list_b, count_of_groups)))
    return list_c


def main():
    list_result = list()
    for count in range(4, 0, -1):
        list_c = get_combinations(len(all_sku_list), 2, count)
        for item in list_c:
            if check_all_set(item):
                list_result.append(item)
        if len(list_result) > 0:
            print(count)
            break


if __name__ == "__main__":
    all_sku_list = get_test_sku_list()
    main()
