#!/usr/bin/env python
# filename: paf.py


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


import os
from typing import Iterable


PAF_HEADER = [
    "query_name",
    "query_length",
    "query_start",
    "query_end",
    "strand",
    "target_name",
    "target_length",
    "target_start",
    "target_end",
    "num_matches",
    "alignment_length",
    "mapping_quality",
]


def read_paf(paf_file: str) -> Iterable:
    """Reads the contents of a PAF-formatted file.

    Parameters
    ----------
    paf_file : str
        Path to a PAF-formatted file

    Returns
    -------
    Iterable
        List of ``PAFEntry`` objects, one for each line in the input
        PAF-formatted file.

    Raises
    ------
    FileNotFoundError
        Raised if the provided PAF file does not exist.
    """
    if not os.path.isfile(paf_file):
        err = f"The provided file path:\n  {paf_file}\ndoes not exist."
        raise FileNotFoundError(err)
    pafs = []
    with open(paf_file, "r") as f:
        for line in f:
            if l := line.strip().split():
                pafs.append(PAFEntry(l))
    return pafs


class PAFEntry:
    """ """

    header = PAF_HEADER

    def __init__(self, line_data):
        self.line_data = line_data
        self.data = {h: v for h, v in zip(self.header, self.line_data)}
        self._tags = None

    def __getattr__(self, attr):
        if attr in self.data:
            return self.data[attr]
        if attr in self.tags:
            return self.tags[attr]
        raise AttributeError(f"PAFEntry does not have the attribute: {attr}")

    @property
    def tags(self):
        if self._tags is None:
            tag_dict = {}
            tags = self.line_data[len(self.header) :]
            for t in tags:
                t = t.split(":")
                tag_dict[t[0]] = t[1:]
            self._tags = tag_dict
        return self._tags
