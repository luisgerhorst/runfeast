#!/usr/bin/env python3

import sys
import os
from pathlib import Path
import logging
import argparse
from io import StringIO

import itertools


def main():
    nr_groups = 21
    main = range(0, nr_groups)
    main_struct = structure(main)
    main_cookers = set(cookers(main))
    for start in itertools.permutations(range(0, nr_groups)):
        start_cookers = set(cookers(start))
        start_struct = structure(main)
        if len(main_cookers.intersection(start_cookers)) != 0:
            continue;

        valid = True
        for m in main_struct:
            main_set = set(m)
            for s in start_struct:
                start_set = set(s)
                if len(main_set.intersection(start_set)) > 2:
                    valid = False
                if not valid:
                    break
            if not valid:
                break
        if not valid:
            continue

        for end in itertools.permutations(range(0, nr_groups)):
            end_cookers = set(cookers(end))
            if len(main_cookers.intersection(end_cookers)) != 0:
                continue;
            if len(start_cookers.intersection(end_cookers)) != 0:
                continue;
            print("start:", structure(start))
            print("main:", main_struct)
            print("end:", structure(end))
            return



def structure(l):
    s = []
    for g in range(0, len(l), 3):
        s += [[l[g], l[g+1], l[g+2]]]
    return s

def cookers(l):
    s = []
    for g in range(0, len(l), 3):
        s += [l[g]]
    return s



if __name__ == "__main__":
    main()
