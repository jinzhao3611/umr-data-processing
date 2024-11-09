import os
from typing import Union
from pathlib import Path
from umr_1_postprocess.scripts import IN_DATA_PATH, INTERMEDIATE_DATA_PATH, OUT_DATA_PATH, JSON_PATH, all_relations, all_concepts, all_expressions
from .utils.io import read_txt_file, write_txt_file, read_json_file, write_json_file, json2txt, txt2json
from .utils.merge_files import merge_to_single_file
from .utils.toolkit import fix_in_json, rename_files_in_folder, clear_folder, remove_sections_specific_to_umr_writer, remove_sections_due_to_other_file_format_english, remove_sections_due_to_other_file_format_arapaho
from .utils.check_valid_graph import is_valid_sent_level_umr, is_valid_doc_level_umr
from manual_changes import manual_fix_english, manual_fix_arapaho, manual_fix_kukama, manual_fix_sanapana, manual_fix_navajo, manual_fix_chinese

def fix_and_write(lang) -> None:
    in_dir: Union[str, os.PathLike] = Path(os.path.join(IN_DATA_PATH, lang))
    intermediate_dir: Union[str, os.PathLike] = Path(os.path.join(INTERMEDIATE_DATA_PATH, lang))
    out_dir: Union[str, os.PathLike] = Path(os.path.join(OUT_DATA_PATH, lang))

    os.makedirs(intermediate_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    clear_folder(intermediate_dir)
    clear_folder(out_dir)

    # STEP1: data/input -> data/intermediate: remove all irrelavant information, apply manual changes
    for in_file_path in Path(in_dir).iterdir():
        if in_file_path.suffix.endswith("txt"):
            file_stem = Path(in_file_path).stem
            if lang == "sanapana": # Jens send me a final version (the input folder) without morph information, that's why i need to merge with the files I exported from database
                text = merge_to_single_file(f"{file_stem}.txt", Path(os.path.join(IN_DATA_PATH, "sanapana_from_database")), in_dir)
            else:
                text = read_txt_file(in_file_path)

            if lang == "english":
                text = remove_sections_specific_to_umr_writer(text)
                text = remove_sections_due_to_other_file_format_english(text)
                text = manual_fix_english(text)
            elif lang == "arapaho":
                text = remove_sections_due_to_other_file_format_arapaho(text)
                text = manual_fix_arapaho(text)
            elif lang == "chinese":
                text = remove_sections_specific_to_umr_writer(text)
                text = manual_fix_chinese(text)
            elif lang == "kukama":
                text = remove_sections_specific_to_umr_writer(text)
                text = manual_fix_kukama(text)
            elif lang == "navajo":
                text = remove_sections_specific_to_umr_writer(text)
                text = manual_fix_navajo(text)
            elif lang == "sanapana":
                text = remove_sections_specific_to_umr_writer(text)
                text = manual_fix_sanapana(text)
            write_txt_file(text, Path(intermediate_dir).joinpath(f"{file_stem}.txt"))
    print(f"finished modifications and wrote file(s) to {intermediate_dir}!")

    # STEP2: intermediate_folder -> jsons folder: change graphs info to json that's easier to check
    txt2json(intermediate_dir)

    #fix through json file
    d = read_json_file(os.path.join(JSON_PATH, f"{lang}.json"))
    d = fix_in_json(d)
    write_json_file(d, os.path.join(JSON_PATH, f"{lang}.json"))

    #check through json file, and generate the error files, and send those error files to the annotators
    is_valid_doc_level_umr(os.path.join(JSON_PATH, f"{lang}.json"))
    is_valid_sent_level_umr(os.path.join(JSON_PATH, f"{lang}.json"), all_relations, all_concepts, all_expressions)

    # STEP 3: jsons folder -> output folder
    json2txt(os.path.join(OUT_DATA_PATH, lang))
    print(f"finished fixing in json and wrote fixed file(s) to {out_dir}!")

    if lang == "kukama":
        # remove duplicated annotation:
        filenames = ["exported_KUK_Sent-JVG_user_1.txt", "exported_kuk1999oct01-umr1-6131_user_1.txt",
                     "kuk1999oct01-umr1_user_4.txt", "kuk1999oct01-umr1_user_8.txt", "KUK_Sent_user_1.txt",
                     "KUK_Sent_user_4.txt", "KUK_Sent_user_8.txt", "kuk20061103-vy_user_9.txt"]
        for filename in filenames:
            os.remove(Path(out_dir).joinpath(filename))

    rename_files_in_folder(out_dir)

if __name__ == '__main__':
    for lang in ["english", "arapaho", "chinese", "kukama", "navajo", "sanapana"]:
        fix_and_write(lang)
