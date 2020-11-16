#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Edward Higgins <ed.higgins@york.ac.uk>
#
# Distributed under terms of the MIT license.

"""
Single Molecule Tools
"""
import sys
from tracking import track
from parameters import Parameters

def main():
    params = Parameters()

    mode = sys.argv[1]
    if mode == "track":
        filename = sys.argv[2]
        track(filename, params)
    else:
        print("//////////////////////////////")
        print("     Single Molecule Tools")
        print("   Construction in progress")
        print("//////////////////////////////")


if __name__ == "__main__":
    main()
