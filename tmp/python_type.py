#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 16/04/24 15:15
# @Author  : tina.huanght@shopee.com
# @File    : python_type.py
from typing import List, Tuple, Set, Dict


def process_list(items: List[str]):
    for item in items:
        print(item)
        print(item.capitalize())


def process_tuple_set(items_t: Tuple[int, int, str], items_s: Set[bytes]):
    for item in items_t:
        print(item)
    print(items_t)
    print(items_s)
    return items_s, items_t


def process_dict(prices: Dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)


if __name__ == '__main__':
    process_list(['a', 'b', 'c'])
    process_tuple_set((1, 2, "test"), [123415, 135125])
    process_dict({"prodcut1": 12.3, "product2": 32, "product3": 43.12})

# Pydantic  学习
# class Person:
#     def __init__(self, name: str):
#         self.name = name
#
#     def get_person_name(one_person: Person):
#         return one_person.name
#
