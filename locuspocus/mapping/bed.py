#!/usr/bin/env python
# filename: bed.py


#
# Copyright (c) 2023 Bryan Briney
# License: The MIT license (http://opensource.org/licenses/MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


def read_bed(bed_file: str):
    return BedSet(bed_file)


class BedSet:
    def __init__(self, bed_file):
        """ """
        self.bed_file = bed_file
        self.beds = self.process_bed_file()

    def __iter__(self):
        for bed in self.beds:
            yield bed

    def __len__(self):
        return len(self.beds)

    def __contains__(self, item):
        return item in self.bed_dict.keys()

    def __getitem__(self, key):
        if type(key) == slice:
            return self.beds[key]
        elif key in self.bed_dict.keys():
            return self.bed_dict.get(key, None)
        elif type(key) == int:
            return self.beds[key]
        return None

    def __setitem__(self, key, val):
        self.bed_dict[key] = val

    @property
    def bed_dict(self):
        return {bed.name: bed for bed in self.beds}

    def find_matches(self, paf):
        matches = []
        for bed in self.beds:
            if bed.matches(paf):
                matches.append(bed)
        return matches

    def process_bed_file(self):
        beds = []
        with open(self.bed_file, "r") as f:
            for line in f:
                if len(l := line.strip().split()) == 4:
                    beds.append(Bed(*l))
        return beds


class Bed:
    def __init__(self, gene, start, end, name):
        self.gene = gene
        self.start = int(start)
        self.end = int(end)
        self.name = name
        self._matches = None

    @property
    def matches(self):
        if self._matches is None:
            self._matches = []
        return self._matches

    # def matches(self, paf):
    #     if paf.target_name != self.gene:
    #         return False
    #     if any(
    #         [
    #             self.start <= paf.target_start <= self.end,
    #             self.start <= paf.target_end <= self.end
    #         ]
    #     ):
    #         return True
    #     return False

    def append(self, paf):
        """
        Appends a PAF object that matches the BED region.

        Parameters
        ----------
        paf : PAF
            a single PAF object that matches the BED region
        """
        self._matches.append(paf)

    def extend(self, pafs):
        self.matches.extend(pafs)
