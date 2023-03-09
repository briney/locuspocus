#!/usr/bin/env python
# filename: map.py


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
import platform
import sys
import subprocess as sp
from typing import Optional, Union


def minimap(
    query: str,
    reference: str,
    output: str,
    as_sam: bool = False,
    include_cigar: bool = True,
    preset: str = "map-ont",
    additional_options: Optional[str] = None,
    debug: bool = False,
) -> str:
    """
    Maps sequences to a reference using `minimap2`_

    Parameters
    ----------
    query : str
        Path to a FASTA- or FASTQ-formatted input file. Gzip-compressed is also accepted.

    reference : str
        Path to a minimap reference, either as a FASTA file or a minimap index.

    output : str
        Path to the output file. By default, output is PAF-formatted although SAM-formatted output
        will be produced if `as_sam` is ``True``.

    as_sam : bool, optional
        If ``True``, produce SAM-formatted output. Default is ``False``, which produces PAF-formatted
        output.

    include_cigar : bool, optional
        Whether the output should include an alignment CIGAR. Default is ``True``.

    preset : str, optional
        Alignment preset to use. Default is ``"map-ont"``.

    additional_options : Optional[str], optional
        String containing additional minimap options. Will be appended directly to tthe minimap command.

    debug : bool, optional
        If ``True``, more verbose output (including the standard output and error from minimap) will
        be printed. Default is ``False``.

    Returns
    -------
    str
        Path to the output file.


    .. _minimap2
        https://github.com/lh3/minimap2

    """
    # parse input/output files
    query = os.path.abspath(query)
    reference = os.path.abspath(reference)
    output = os.path.abspath(output)
    # locate minimap2 binary
    mod_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    minimap_bin = os.path.join(
        mod_dir, "bin/minimap2_{}".format(platform.system().lower())
    )
    minimap_cmd = f"{minimap_bin} -x {preset.lower()}"
    if include_cigar:
        minimap_cmd += " -c"
    if as_sam:
        minimap_cmd += " -a"
    if additional_options is not None:
        minimap_cmd += f" {additional_options}"
    minimap_cmd += f" {reference} {query} > {output}"
    p = sp.Popen(minimap_cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    stdout, stderr = p.communicate()
    if debug:
        print(stdout)
        print(stderr)
    return output
