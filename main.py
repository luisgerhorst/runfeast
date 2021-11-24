#!/usr/bin/env python3

import sys
import os
from pathlib import Path
import logging
import argparse
from io import StringIO

import random
import itertools

nr_groups = 8
size = 3

def main():
    main = range(0, nr_groups)
    main_struct = structure(main)
    main_cookers = set(cookers(main))

    opt_sim = nr_groups
    opt_eim = nr_groups
    opt_seci = nr_groups
    opt_meci = nr_groups
    opt_smci = nr_groups
    opt_meetsum = 0
    opt_meetmin = 0
    opt_meetmax = 0
    opt_sis = nr_groups*nr_groups
    opt_eis = nr_groups*nr_groups

    ep = list(itertools.permutations(range(0, nr_groups)))
    random.shuffle(ep)
    sp = list(itertools.permutations(range(0, nr_groups)))
    random.shuffle(sp)

    for start in sp:

        start_cookers = set(cookers(start))
        start_struct = structure(start)

        smci = len(main_cookers.intersection(start_cookers))
        if smci > opt_smci:
            continue;

        sis, sim = check_intersect(main_struct, start_struct)
        if not (sim <= opt_sim):
            continue
        if sis > opt_sis:
            continue

        for end in ep:
            end_cookers = set(cookers(end))

            meci = len(main_cookers.intersection(end_cookers))
            if meci > opt_meci:
                continue

            end_struct = structure(end)
            eis, eim = check_intersect(main_struct, end_struct)
            meetmin, meetmax, meetsum = meet(start_struct, main_struct, end_struct)
            seci = len(start_cookers.intersection(end_cookers))
            if not (((meetmin > opt_meetmin or meetmin == opt_meetmin and meetsum >= opt_meetsum) or eis < opt_eis or eim < opt_eim) and seci <= max(opt_seci, opt_meci, opt_smci)):
                continue

            opt_smci = smci
            opt_meci = meci
            opt_seci = seci
            opt_sim = sim
            opt_sis = sis
            opt_eim = eim
            opt_eis = eis
            opt_meetmin = meetmin
            opt_meetsum = meetsum
            opt_meetmax = meetmax

            print("start:", structure(start))
            print("main:", main_struct)
            print("end:", structure(end))
            print(smci, meci, sim, eim, sis, eis, meetmin, meetmax, meetsum, seci, sis, eis)

def meet(a, b, c):
    m_min = nr_groups
    m_max = 0
    meetsum = 0
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
        meetsum += len(mg)
    return (m_min, m_max, meetsum)


def check_intersect(main_struct, start_struct):
    "How many different are the groups between the two rounds. sum/max are better if lower."
    sis = 0
    sim = 0
    for m in main_struct:
        main_set = set(m)
        for s in start_struct:
            start_set = set(s)
            i = len(main_set.intersection(start_set))
            sis += i
            sim = max(sim, i)
    return (sis, sim)

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
    for g in structure(l):
        s += [g[0]]
    return s



if __name__ == "__main__":
    main()
