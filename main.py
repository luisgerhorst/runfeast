#!/usr/bin/env python3

import sys
import os
from pathlib import Path
import logging
import argparse
from io import StringIO

import random
import itertools

nr_groups = 5
size = 3

def main():
    main = range(0, nr_groups)
    main_struct = structure(main)
    main_cookers = set(cookers(main))
    for start in itertools.permutations(range(0, nr_groups)):

        start_cookers = set(cookers(start))
        start_struct = structure(start)
        if len(main_cookers.intersection(start_cookers)) >= 1:
            continue;

        start_i_sum, start_i_max = check_intersect(main_struct, start_struct)
        if start_i_max == size:
            continue

        for end in itertools.permutations(range(0, nr_groups)):
            end_cookers = set(cookers(end))
            if len(main_cookers.intersection(end_cookers)) >= 1:
                continue
            if len(start_cookers.intersection(end_cookers)) >= 2:
                continue

            eis, eim = check_intersect(main_struct, start_struct)
            if eim == size:
                continue

            end_struct = structure(end)
            meet_min, meet_max, m_sum = meet(start_struct, main_struct, end_struct)
            if meet_min < nr_groups or m_sum <= 23:
                continue

            print("start:", structure(start))
            print("main:", main_struct)
            print("end:", structure(end))
            print(start_i_sum, start_i_max, eis, eim, meet_min, meet_max, m_sum)

def meet(a, b, c):
    m_min = nr_groups
    m_max = 0
    m_sum = 0
    for g in range(0, nr_groups):
        mg = set()
        for m in a:
            if g in m:
                mg.update(m)
        for m in b:
            if g in m:
                mg.update(m)
        for m in c:
            if g in m:
                mg.update(m)
        m_min = min(len(mg), m_min)
        m_max = max(len(mg), m_max)
        m_sum += len(mg)
    return (m_min, m_max, m_sum)


def check_intersect(main_struct, start_struct):
    start_i_sum = 0
    start_i_max = 0
    for m in main_struct:
        main_set = set(m)
        for s in start_struct:
            start_set = set(s)
            i = len(main_set.intersection(start_set))
            start_i_sum += i
            start_i_max = max(start_i_max, i)
    return (start_i_sum, start_i_max)

def structure(l):
    s = []
    if len(l) % size == 0:
        for g in range(0, len(l), size):
            s += [[l[g], l[g+1], l[g+2]]]
    if len(l) % size == 1:
        for g in range(0, len(l)-size*2, size):
            s += [[l[g], l[g+1], l[g+2]]]
        s += [[l[-4], l[-3]]]
        s += [[l[-2], l[-1]]]
    if len(l) % size == 2:
        for g in range(0, len(l)-size, size):
            s += [[l[g], l[g+1], l[g+2]]]
        s += [[l[-2], l[-1]]]
    return s

def cookers(l):
    s = []
    for g in range(0, len(l), 3):
        s += [l[g]]
    return s



if __name__ == "__main__":
    main()
