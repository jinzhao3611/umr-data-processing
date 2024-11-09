import os
import re, json
import warnings
from collections import defaultdict
from typing import List, Dict, Union
import itertools
from scripts import sent_level_terms_convert_dict, doc_level_terms_convert_dict, FILES_PATH

NBSP = u"\u00A0"  # non-breaking spaces
SENT_PREFIX = "# :: snt"
DOC_ROOT_VAR_SUFFIX = "/ sentence"



def contain_annotation(text: str) -> bool:
    lines = text.split("\n")
    # print(lines)
    return len(lines) > 10


def split_multiple_annotations(text: str) -> List[str]:
    if not contain_annotation(text):
        return [text]
    lines = text.split("\n")
    all_sent_dict = defaultdict(list)
    curr_sent = []
    curr_sent_id = None
    for line in lines:
        if line.startswith(SENT_PREFIX):
            if curr_sent_id:
                all_sent_dict[curr_sent_id].append("\n".join(curr_sent))
            curr_sent_id = line.split()[2]
            curr_sent = [line]
        else:
            curr_sent.append(line)

    if curr_sent_id:
        all_sent_dict[curr_sent_id].append("\n".join(curr_sent))


    if len(set([len(s) for s in all_sent_dict.values()])) != 1:
        warnings.warn("Missing sentence annotation from at least one version of the annotation file!")

    all_text = []

    for sents in itertools.zip_longest(*list(all_sent_dict.values()), fillvalue="[MISSING SENTENCE]"):
        sents_text = "\n".join(sents)
        all_text.append(sents_text)

    return all_text


def fix_doc_root_variable(text: str) -> str:
    lines = []
    for line in text.split("\n"):
        if line.strip().endswith(DOC_ROOT_VAR_SUFFIX):
            comp, *res = line.strip().split()
            if not comp.endswith("s0"):
                comp += "s0"
            line = " ".join([comp, *res])
        lines.append(line)
    return "\n".join(lines)


def fix_in_json(d: Dict[str, List[List[str]]]) -> Dict[str, List[List[str]]]:
    for doc_name, umr_info in d.items():
        for i, s_a in enumerate(umr_info[1]): #sentence level annotation
            if s_a == "sentence level graph:": # sentence level annotation is empty
                umr_info[1][i] = f"sentence level graph:\n(s{i+1}u / umr-empty)"
            else:
                for old, new in sent_level_terms_convert_dict.items():
                    s_a = s_a.replace(old, new) # lowercase all the sent level umr terms (Austin's suggestion)
                s_a = re.sub(r"\((s\d+\w\d+) \/ (s\d+\w\d+)\)", r"\2", s_a)  # correct the wrong format in :quote
                umr_info[1][i] = re.sub(r"\n\n", '\n', s_a) # remove unnecessary \n
        for i, a in enumerate(umr_info[2]): #alignment
            a = re.sub(r"(\d)-(undefined)", r'\1-\1', a) # this is a historical UMR writer bug
            a = re.sub(r"alignment:s", "alignment:\ns", a) #add a \n if there is no line break after "alignments:", historically UMR writer export files without line break after "alignments"
            a = re.sub(r"\n[\s\d\w]*:undefined", '', a) # this is an unknown UMR writer bug
            a_lst = [a.split("\n")[0]]
            # remove something like 'Singular : -1--1' in Kukama, this is due to manual change and UMR writer bug
            for line in a.split("\n")[1:]:
                if re.match("s\d+\w\d* ?: ?-?\d+--?\d+", line):
                    a_lst.append(line)
            umr_info[2][i] = "\n".join(a_lst)
        for i, d_a in enumerate(umr_info[3]): #document level annotation
            if d_a == "document level annotation:": #document level annotation is empty
                umr_info[3][i] = f"document level annotation:\n(s{i+1}s0 / sentence)"
            else:
                for old, new in doc_level_terms_convert_dict.items():
                    d_a = d_a.replace(old, new) # lowercase all the doc level umr terms
                # change null
                umr_info[3][i] = re.sub(r"\n\n+", '\n', d_a) #fix the extra \n in doc level annotation(historical UMR writer bug)
                if len(d_a) > len("document level graph: \n(s165s0 / sentence)") + 1 and ":modal" in d_a:
                    umr_info[1][i] = remove_sent_level_modal(umr_info[1][i])
    return d

def remove_sent_level_modal(text: str) -> str:
    # remove the lines of modal annotation
    text = re.sub(r"\n *:modal-strength [^)\n]+", "", text)
    text = re.sub(r"\n *:modal-predicate [^)\n]+", "", text)
    # text = re.sub(r"\n *:quote [^)\n]+", "", text) # there is :quote(s1e /event) or :quote(s1i/implicit-predicate), therefore we do not remove this anymore
    return text

def rename_files_in_folder(folder_path):
    mapping = {}
    # Get a list of all files in the folder
    file_list = [ele for ele in os.listdir(folder_path) if (ele!= "README.md" and ele!=".DS_Store")]

    # Iterate through the files and rename them one by one
    for index, old_name in enumerate(file_list, start=1):
        # Create the new name for the file
        new_name = f"{os.path.split(folder_path)[-1]}_umr-{str(index).zfill(4)}.txt"  # Adjust the extension as needed
        mapping[new_name] = old_name

        # Build the full file paths for old and new names
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)

        # Rename the file
        os.rename(old_path, new_path)

    with open(os.path.join(FILES_PATH, f"{os.path.split(folder_path)[-1]}_mapping.json"), "w") as jsonfile:
        json.dump(mapping, jsonfile, indent=4)

def clear_folder(folder_path: Union[str, os.PathLike]) -> None:
    """
    removes all files in a directory(except directories and README file), this is to avoid multiple versions of postprocessed files are save in data/output
    :param folder_path: e.g. data/output/english
    :return: None
    """
    files = os.listdir(folder_path)

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path) and "README" not in file_name:  # Check if it's a file (not a directory)
                os.remove(file_path)
                print(f"File '{file_name}' removed successfully.")
        except Exception as e:
            print(f"Error removing file '{file_name}': {e}")

def remove_sections_specific_to_umr_writer(exported_file_content:str) -> str:
    """
    UMR Writer exported files contain a info section at the beginning and the original sentences section in the end. This function remove those two sections
    :param exported_file_content: content read from the exported file
    :return: content without the beginning and ending section
    """
    exported_file_content = re.sub(
        r"user name:.*\nuser id:.*\nfile language:.*\nfile format:.*\nDoc ID in database:.*\nexport time:.*\n\n", "",
        exported_file_content)  # remove the info section of each document
    exported_file_content = re.sub(r"(?s)# Source File:.+", "", exported_file_content)  # remove the ending section of each document
    return exported_file_content

def remove_sections_due_to_other_file_format_english(text: str) -> str:
    """
    Remove irrelavant sections coming from other file formatting
    :param text: content files from data/input
    :return: content without irrelavant sections
    """
    text = re.sub(
        r"user name:.*\nuser id:.*\nfile language:.*\nfile format:.*\ntotal sentences:.*\nDoc ID in database:.*\nexport time:.*\n\n",
        "", text)
    text = re.sub(r"\n*#\s*(tokens\s*:\s*)*[\s\d]*#*\s*Sentence\s*:", "",
                                   text)
    text = re.sub(r"#\*.*", "", text)  # remove all comments Julia made like #*Guinsaugon
    return text

def remove_sections_due_to_other_file_format_arapaho(text:str) -> str:
    """
       Remove irrelavant sections coming from other file formatting
       :param text: content files from data/input
       :return: content without irrelavant sections
   """
    text = re.sub(r"user name:.*\nuser id:.*\nfile language:.*\ndocument:.*\ntotal sentences:.*\n\n", "",
                  text)  # remove the title of each document
    text = re.sub(r"(?s)# Source File:.+", "", text)  # remove the end of each document
    text = re.sub(r"(# :: snt\d+\s?\n)(#tk\s+1.*\n)(#t?x?)(.*\n)(#m?b?)(.*\n)(#g?e?)(.*\n)(#p?s?)(.*\n)(#t?r?)(.*)",
                  r"\1tx\4mb\6ge\8ps\10tr\12", text)
    text = text.replace("#- seven -3PL", "_ - seven -3PL")  # this hashtag is causing problems when split
    text = text.replace("tx9", "tx")
    text = re.sub(r"#\*.*", "", text)  # remove all comments Julia made like #*Guinsaugon
    return text