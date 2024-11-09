import json
import os
import re
from collections import defaultdict

import penman
from penman.exceptions import DecodeError

from umr_1_postprocess.scripts import all_concepts, all_expressions, all_relations, JSON_PATH, ERRORS_PATH, document_level_constants

def is_integer(s):
    try:
        int(s)  # Attempt to convert the string to an integer
        return True  # Return True if the conversion succeeds
    except ValueError:
        return False  # Return False if the conversion fails

def is_float(s): #attribute value of :quant could be 2.6 like seismic quantity
    try:
        float(s)  # Attempt to convert the string to an integer
        return True  # Return True if the conversion succeeds
    except ValueError:
        return False  # Return False if the conversion fails

def find_unmatched_parentheses(s):
    stack = []
    unmatched_positions = []
    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if not stack:
                unmatched_positions.append(i)
            else:
                stack.pop()
    # Append unmatched opening parenthesis positions to the result
    unmatched_positions.extend(stack)
    return unmatched_positions

def find_all_bracketed_information(input_string):
    stack = []
    result = []

    for i, char in enumerate(input_string):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                start = stack.pop()
                result.append(input_string[start:i + 1])

    return result

def find_duplicates(lst):
    seen = {}
    duplicates = []

    for item in lst:
        if item in seen:
            duplicates.append(item)
        else:
            seen[item] = 1

    return duplicates

def doc_umr_decode(doc_umr_graph):
    all_bracketed_information = find_all_bracketed_information(doc_umr_graph)
    triples = defaultdict(list)
    all_rels = []
    for b in all_bracketed_information:
        graph_root_match = re.match(r"\(s\d+s0\s+/\s+sentence", b)
        if graph_root_match:
            all_rels = re.findall(r":temporal|:modal|:coref", b)
    current_relation_index = 0
    for b in all_bracketed_information:
        graph_root_match = re.match(r"\(s\d+s0\s+/\s+sentence", b)
        if not graph_root_match:
            if b.startswith("(("):
                current_relation_index += 1
            else:
                tuple_of_triple = tuple(re.search(r"\((.*?)\)", b).group(1).split())
                triples[all_rels[current_relation_index]].append(tuple_of_triple)
    return triples

def get_all_variables(filename):
    variables_of_docs = {}
    file_path = os.path.join(JSON_PATH, filename)
    with open(file_path, "r") as jsonfile:
        umrs = json.load(jsonfile)
        for doc_name, umr_info in umrs.items():
            variables = []
            for i in range(len(umr_info[0])):
                # load sentence_level umr graph
                try:
                    g = penman.decode(umr_info[1][i][21:])
                    # print("#" + umr_info[0][i] + umr_info[1][i][21:])
                except DecodeError as e:
                    print(e)
                variables = variables + list(g.variables())
            variables_of_docs[doc_name] = variables
    return variables_of_docs

def is_valid_sent_level_umr(json_file_path, all_relations, all_concepts, all_expressions):
    error_msgs = defaultdict(list)
    filename = os.path.basename(json_file_path)
    with open(json_file_path, "r") as jsonfile:
        umrs = json.load(jsonfile)
        for doc_name, umr_info in umrs.items():
            for i in range(len(umr_info[0])):
                # check if parentheses are balanced:
                umr_graph = umr_info[1][i][21:]
                unmatched_positions = find_unmatched_parentheses(umr_graph)
                if unmatched_positions:
                    for unmatched_position in unmatched_positions:
                        error_msgs[filename[:-5]].append(
                            f"""In document '{doc_name}', in {umr_info[0][i][:9]}, in sent_level_umr, Parentheses are not balanced. Unmatched {umr_graph[unmatched_position]} in: ***{umr_graph[unmatched_position - 20: unmatched_position + 20]}***""")
                # load sentence_level umr graph
                try:
                    if umr_info[1][i][21:]:
                        g = penman.decode(umr_info[1][i][21:])
                        # check duplicated variable: Julia said there could be mistakes when two different nodes in a sentence have a 'sn2' variable, when neither is a reentrancy. One should really be 'sn3'
                        parent_nodes = []
                        for instance in g.instances():
                            parent_nodes.append(instance.source)
                        duplicated_variables = find_duplicates(parent_nodes)
                        if duplicated_variables:
                            for var in duplicated_variables:
                                error_msgs[filename[:-5]].append(
                                    f"In document '{doc_name}', in {umr_info[0][i][:9]}, there is duplicated variable {var}")
                        # check roles, concepts
                        triples_include_instances = list(g.epidata.keys())
                        for triple in triples_include_instances:
                            if triple[1] == ":instance":
                                concept = triple[2]
                                if concept:
                                    # navajo has ’ character
                                    if not re.match(r"'\w+-\d\d", concept) and not re.match(r"[’'\w-]+",
                                                                                            concept) and concept not in all_concepts:  # if concept is not valid
                                        error_msgs[filename[:-5]].append(
                                            f"In document '{doc_name}', in {umr_info[0][i][:9]}, concept {concept} is not valid")
                                else:  # concept is None
                                    error_msgs[filename[:-5]].append(
                                        f"In document '{doc_name}', in {umr_info[0][i][:9]}, concept {concept} is None")
                            else:
                                rel = triple[1]
                                child = triple[2]
                                if child:
                                    if rel not in all_relations:  # check if the relation name is valid
                                        error_msgs[filename[:-5]].append(
                                            f"In document '{doc_name}', in {umr_info[0][i][:9]}, relation {rel} is not valid")
                                    if re.match(r"\"s\d+\w\d*\"",
                                                child):  # check if reentrancy variable is quoted mistakenly
                                        error_msgs[filename[:-5]].append(
                                            f"In document '{doc_name}', in {umr_info[0][i][:9]}, reentrancy variable {child} is quoted mistakenly")
                                    if not (re.match(r"s\d+\w\d*",
                                                     child) or '"' in child or child in all_expressions or is_integer(
                                            child) or is_float(child)):
                                        print("here:")
                                        print(child)
                                        error_msgs[filename[:-5]].append(
                                            f"In document '{doc_name}', in {umr_info[0][i][:9]}, attribute value {child} is not valid")
                                else:
                                    error_msgs[filename[:-5]].append(
                                        f"In document '{doc_name}', in {umr_info[0][i][:9]}, child {child} is None, relation is {rel}")
                    else: # umr graph is empty
                        error_msgs[filename[:-5]].append(
                            f"In document '{doc_name}', in {umr_info[0][i][:9]}, the sentence level umr is empty ")
                except DecodeError as e:
                    error_msgs[filename[:-5]].append(
                        f"In document '{doc_name}', in {umr_info[0][i][:9]}, there is unknown problem: {e} ")

    with open(os.path.join(ERRORS_PATH, "sent_level_" + filename), "w") as jsonfile:
        json.dump(error_msgs, jsonfile, indent=4)

def is_valid_doc_level_umr(file_path):
    filename = os.path.basename(file_path)
    error_msgs = defaultdict(list)
    with open(file_path, "r") as jsonfile:
        umrs = json.load(jsonfile)
        variables_of_doc = get_all_variables(filename)
        for doc_name, umr_info in umrs.items():
            for i in range(len(umr_info[0])):
                # check if parentheses are balanced:
                umr_graph = umr_info[3][i][22:].strip()
                unmatched_positions = find_unmatched_parentheses(umr_graph)
                if unmatched_positions:
                    for unmatched_position in unmatched_positions:
                        error_msgs[filename[:-5]].append(
                            f"""In document '{doc_name}', in {umr_info[0][i][:9]}, in doc_level_umr, Parentheses are not balanced. Unmatched {umr_graph[unmatched_position]} in: ***{umr_graph[unmatched_position - 20: unmatched_position + 20]}***""")
                # parse doc level umr
                try:
                    doc_triples = doc_umr_decode(umr_info[3][i])
                    if not doc_triples:
                        error_msgs[filename[:-5]].append(
                            f"""In document '{doc_name}', in {umr_info[0][i][:9]}, doc_level_umr does not exist""")
                    # check doc variables against sent level variables
                    for doc_rel, triple in doc_triples.items():
                        for t in triple:
                            if len(t) < 3:
                                error_msgs[filename[:-5]].append(
                                    f"""In document '{doc_name}', in {umr_info[0][i][:9]}, in doc_level_umr,  {t} lacks information""")
                            else:
                                if t[0] not in variables_of_doc[doc_name] + document_level_constants:
                                    error_msgs[filename[:-5]].append(
                                        f"""In document '{doc_name}', in {umr_info[0][i][:9]}, in doc_level_umr,  {t[0]} does not exist in sent_level_umr""")
                                if t[2] not in variables_of_doc[doc_name] + document_level_constants:
                                    error_msgs[filename[:-5]].append(
                                        f"""In document '{doc_name}', in {umr_info[0][i][:9]}, in doc_level_umr,  {t[2]} does not exist in sent_level_umr""")
                except IndexError:
                    error_msgs[filename[:-5]].append(
                        f"""In document '{doc_name}', in {umr_info[0][i][:9]}, doc_level_umr root format is incorrect""")
                except AttributeError:
                    error_msgs[filename[:-5]].append(
                        f"""In document '{doc_name}', in {umr_info[0][i][:9]}, there is unknown problem with one of the triples""")

    with open(os.path.join(ERRORS_PATH, "doc_level_" + filename), "w") as jsonfile:
        json.dump(error_msgs, jsonfile, indent=4)

def is_chinese_aligned(file_path): #alignments counts start from 1
    filename = os.path.basename(file_path)
    error_msgs = defaultdict(list)
    no_align_concept = []
    with open(file_path, "r") as jsonfile:
        umrs = json.load(jsonfile)
        for doc_name, umr_info in umrs.items():
            for i in range(len(umr_info[0])):
                aligns = [e.split(":") for e in umr_info[2][i][10:].strip().split("\n")]
                try:
                    aligns_dict = {e[0]:e[1].strip() for e in aligns if e[0]}
                except IndexError:
                    error_msgs[filename[:-5]].append(f"In document '{doc_name}', the alignment of sent {umr_info[0][i][:9]} is empty. ")
                sentence = umr_info[0][i].strip()
                tokens = re.sub(r":: snt\d+(	Sentence:)?","",sentence).strip().split()
                token_indices = defaultdict(list)
                for index, element in enumerate(tokens):
                    token_indices[element].append(index+1)
                try:
                    g = penman.decode(umr_info[1][i][21:])
                except DecodeError as e:
                    error_msgs[filename[:-5]].append(
                        f"In document '{doc_name}', in {umr_info[0][i][:9]}, there is unknown problem: {e} ")
                for instance in g.instances():
                    if instance.target.split("-")[0] in tokens:
                        try:
                            annotated_align = int(aligns_dict[instance.source].split("-")[0])
                        except ValueError:
                            annotated_align = -1
                        except KeyError:
                            annotated_align = -2 # there is no alignment for this one
                            error_msgs[filename[:-5]].append(f"In document '{doc_name}', missing alignment for variable '{instance.source}'")
                        true_align = [token_index for token_index in token_indices[instance.target.split("-")[0]]]
                        if not annotated_align in true_align:
                            # correct in align_dict
                            for t_a in true_align:
                                if not any(t_a in item for item in list(aligns_dict.items())):
                                    if instance.source in aligns_dict:
                                        aligns_dict[instance.source] = f"{true_align[0]}-{true_align[0]}"
                                    else: # if the variable is not annotated variable
                                        aligns_dict.update({instance.source: f"{true_align[0]}-{true_align[0]}"})
                                    error_msgs[filename[:-5]].append(
                                        f"In document '{doc_name}', the alignment of variable '{instance.source}', concept '{instance.target}' is annotated as '{annotated_align}', but should be '{true_align}'")
                        # else:
                        #     print(f"correct! concept '{instance.target}' is annotated as '{annotated_align}', and is '{true_align}'")
                    else: # should be abstract concept, no nothing for now
                        no_align_concept.append(instance.target)
                    umr_info[2][i] = "alignment:\n" + "\n".join([f"{k}: {v}" for k, v in aligns_dict.items()])

    with open(JSON_PATH.joinpath(filename), "w") as json_file:
        json.dump(umrs, json_file, indent=4)
    error_msgs[filename[:-5]].append(
        f"In document '{doc_name}', no align concepts are : {no_align_concept}")
    with open(os.path.join(ERRORS_PATH, "align_" + filename), "w") as jsonfile:
        json.dump(error_msgs, jsonfile, indent=4)

def fix_navajo_align(file_path): #alignments counts start from 1, however, navajo align starts from 0
    filename = os.path.basename(file_path)
    error_msgs = defaultdict(list)
    with open(file_path, "r") as jsonfile:
        umrs = json.load(jsonfile)
        for doc_name, umr_info in umrs.items():
            for i in range(len(umr_info[0])):
                aligns = [e.split(":") for e in umr_info[2][i][10:].strip().split("\n")]
                try:
                    aligns_dict = {e[0].strip():e[1].strip() for e in aligns if e[0]}
                except IndexError:
                    error_msgs[filename[:-5]].append(f"In document '{doc_name}', the alignment of sent {umr_info[0][i][:9]} is empty. ")
                try:
                    g = penman.decode(umr_info[1][i][21:])
                except DecodeError as e:
                    error_msgs[filename[:-5]].append(
                        f"In document '{doc_name}', in {umr_info[0][i][:9]}, there is unknown problem: {e} ")
                for instance in g.instances():
                    if instance.target not in all_expressions:
                        try:
                            start, end = aligns_dict[instance.source].split("-")
                        except ValueError:
                            # ignore the alignment that's -1--1
                            continue
                        except KeyError:
                            error_msgs[filename[:-5]].append(f"In document '{doc_name}', missing alignment for variable '{instance.source}'")
                        try:
                            aligns_dict[instance.source] = str(int(start)+1) + "-" + str(int(end)+1)
                        except ValueError:
                            error_msgs[filename[:-5]].append(
                                f"In document '{doc_name}', the alignment of sent {umr_info[0][i][:9]} has undefined. ")
                umr_info[2][i] = "alignment:\n" + "\n".join([f"{k}: {v}" for k, v in aligns_dict.items()])

    with open(JSON_PATH.joinpath(filename), "w") as json_file:
        json.dump(umrs, json_file, indent=4)

    with open(os.path.join(ERRORS_PATH, "align_" + filename), "w") as jsonfile:
        json.dump(error_msgs, jsonfile, indent=4)


import re


def check_align_format(string: str) -> str:
    """
    Checks if a given string matches one of the defined formats:
    - `s1x1: 1-2` (MWE)
    - `s12x2: 3-4,6-6` (non-contiguous MWE)
    - `s1x33: 1.1-1.12` (subword)

    Args:
        string (str): The input string to check.

    Returns:
        str: The matching format type ('MWE', 'non-contiguous MWE', 'subword') or 'Invalid format' if no match.
    """
    # Pattern for `s1x1: 1-2` (MWE)
    pattern_mwe = r"^s\d+x\d+: \d+-\d+$"

    # Pattern for `s12x2: 3-4,6-6` (non-contiguous MWE)
    pattern_non_contiguous_mwe = r"^s\d+x\d+: (\d+-\d+,)*\d+-\d+$"

    # Pattern for `s1x33: 1.1-1.12` (subword)
    pattern_subword = r"^s\d+x\d+: \d+\.\d+-\d+\.\d+$"

    if re.match(pattern_mwe, string):
        return "MWE"
    elif re.match(pattern_non_contiguous_mwe, string):
        return "non-contiguous MWE"
    elif re.match(pattern_subword, string):
        return "subword"
    else:
        return "Invalid format"




if __name__ == '__main__':
    # is_valid_doc_level_umr(os.path.join(JSON_PATH, "arapaho.json"))
    # is_valid_sent_level_umr(os.path.join(JSON_PATH, "arapaho.json"), all_relations, all_concepts, all_expressions)
    is_chinese_aligned(os.path.join(JSON_PATH, "corr_chinese.json"))
    # fix_navajo_align(os.path.join(JSON_PATH, "navajo.json"))


