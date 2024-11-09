# this is used when I need to merge the sentence(+morpho) display in one file and the annotations in another file
import os
from scripts.utils.io import read_txt_file
import re

SNT_PREFIX = "# :: snt"
SNT_LEVEL_PREFIX = "# sentence level graph"
ALIGNMENT_PREFIX = "# alignments"
DOC_LEVEL_PREFIX = "# document level graph"

PATTERN = fr"{SNT_PREFIX}|{SNT_LEVEL_PREFIX}|{ALIGNMENT_PREFIX}|{DOC_LEVEL_PREFIX}"


def split_file_to_comps(text: str):
    text = text.strip()
    lines = text.split("\n")
    curr_comp_lines = []
    comps = []

    for line in lines:
        if re.match(PATTERN, line):
            if curr_comp_lines:
                comps.append("\n".join(curr_comp_lines))
            curr_comp_lines = [line]
        else:
            curr_comp_lines.append(line)
    if curr_comp_lines:
        comps.append("\n".join(curr_comp_lines))
    return comps


def merge_to_single_file(file_name: str, this_dir, other_dir) -> str:
    snt_text = read_txt_file(this_dir.joinpath(file_name))
    snt_text = re.sub(
        r"user name:.*\nuser id:.*\nfile language:.*\nfile format:.*\nDoc ID in database:.*\nexport time:.*\n\n",
        "",
        snt_text)  # remove the title of each document
    snt_text = re.sub(r"user name:.*\nuser id:.*\nfile language:.*\ndocument:.*\ntotal sentences:.*\n\n", "",
                  snt_text)  # remove the title of each document
    snt_text = re.sub(r"(?s)# Source File:.+", "", snt_text)  # remove the end of each document
    other_text = read_txt_file(other_dir.joinpath(file_name))
    snt_comps = split_file_to_comps(snt_text)
    other_comps = split_file_to_comps(other_text)
    assert len(snt_comps) == len(other_comps)
    final_comps = []
    for c1, c2 in zip(snt_comps, other_comps):
        if c1.startswith(SNT_PREFIX):
            final_comps.append(c1)
        else:
            final_comps.append(c2)
    text = "\n".join(final_comps)
    return text



