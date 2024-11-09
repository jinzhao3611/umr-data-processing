from pathlib import Path
import os, json

IN_DATA_PATH = Path(__file__).parent.parent.joinpath("data/input")
INTERMEDIATE_DATA_PATH = Path(__file__).parent.parent.joinpath("data/intermediate")
OUT_DATA_PATH = Path(__file__).parent.parent.joinpath("data/output")


JSON_PATH = Path(__file__).parent.parent.joinpath("jsons")
FINAL_JSON_PATH = Path(__file__).parent.parent.joinpath("final_jsons") # used to count the statistics of the released dataset
ERRORS_PATH = Path(__file__).parent.parent.joinpath("errors")
FILES_PATH = Path(__file__).parent.parent.joinpath("files")

document_level_constants = ['author', 'author2', 'author3', 'document-creation-time', 'root', 'past-reference', 'present-reference', 'future-reference', 'null-conceiver', "purpose", "have-condition-91", "have-purpose-91", "have-concession-91", "have-concessive-condition-91"]
#kukama doc level annotation has purpose
concept_rel_attr_dict = {}
for filename in os.listdir(os.path.join(FILES_PATH, "umr_terms")):
    file_path = os.path.join(FILES_PATH, "umr_terms", filename)
    if os.path.isfile(file_path) and not filename.startswith("README"):
        with open(file_path, "r") as file:
            concept_rel_attr_dict[filename[:-7]] = [item.strip() for item in file.readlines()]

with open(os.path.join(FILES_PATH, "sent_level_terms.json"), "r") as jsonfile:
    sent_level_terms_convert_dict = json.load(jsonfile)
with open(os.path.join(FILES_PATH, "doc_level_terms.json"), "r") as jsonfile:
    doc_level_terms_convert_dict = json.load(jsonfile)

all_relations = [ele.lower().replace(" ", "-").replace("_", "-") if "ARG" not in ele else ele for ele in concept_rel_attr_dict["modal"] + concept_rel_attr_dict["roles"] + concept_rel_attr_dict["attr_types"]] \
    + [":modal-strength", ":quote", ":modal-predicate"] \
    + [":vocative", "stimulus", ":accompanier", ":possession", ":destination", ":end-state", ":result"] \
    + [":op" + str(num) for num in range(1,100)]

all_concepts = [ele.lower().replace(" ", "-").replace("_", "-") for ele in concept_rel_attr_dict["abstract_concept"] + concept_rel_attr_dict["ne"]]
all_expressions_before_process =  concept_rel_attr_dict["attr_ref_person"] + concept_rel_attr_dict["attr_polarity"] \
                  + concept_rel_attr_dict["modstr"] + concept_rel_attr_dict["attr_degree"] \
                  + concept_rel_attr_dict["attr_mode"] + concept_rel_attr_dict["attr_aspect"] \
                  + concept_rel_attr_dict["attr_ref_number"]
all_expressions = ['4th', 'interrogative', 'umr-unknown']
for ele in all_expressions_before_process:
    if ele in sent_level_terms_convert_dict:
        all_expressions.append(sent_level_terms_convert_dict[ele])
    else:
        all_expressions.append(ele)

print(all_expressions)