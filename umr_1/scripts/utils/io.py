from typing import Union, Dict, List, Any
import os, json
from scripts import JSON_PATH
from pathlib import Path


def read_txt_file(file_path: Union[str, os.PathLike]) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_txt_file(text: str, out_file_path: Union[str, os.PathLike]) -> None:
    with open(out_file_path, "w", encoding="utf-8") as f:
        f.write(text)


def read_json_file(file_path: Union[str, os.PathLike]) -> Dict[str, List[Any]]:
    with open(file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def write_json_file(d:Dict[str, List[Any]], out_file_path: Union[str, os.PathLike]) -> None:
    with open(out_file_path, "w", encoding="utf-8") as json_file:
        json.dump(d, json_file, indent=4)


def json2txt(txt_folder: Union[str, os.PathLike]) -> None:
    os.makedirs(txt_folder, exist_ok=True)
    file_path = os.path.join(JSON_PATH, f"{os.path.split(txt_folder)[-1]}.json")
    if os.path.isfile(file_path) and file_path.endswith(".json"):
        with open(file_path, "r") as jsonfile:
            umrs = json.load(jsonfile)
            for doc_name, umr_info in umrs.items():
                with open(os.path.join(txt_folder, doc_name + ".txt"), "w") as writefile:
                    for i in range(len(umr_info[0])):
                        s = "# " + umr_info[0][i] + "\n\n" + "# " + umr_info[1][i] + "\n\n" + "# " + umr_info[2][i] + "\n\n" + "# " + umr_info[3][i] + "\n\n\n"
                        writefile.write(s)


def txt2json(txt_folder: Union[str, os.PathLike], output_folder: Union[str, os.PathLike] = JSON_PATH) -> None:
    txt_folder = Path(txt_folder)
    output_folder = Path(output_folder)
    data_dict = {}

    for txt_file in txt_folder.glob("*.txt"):
        with txt_file.open("r") as file:
            content = file.read().split("#")

            # Define indices for each section type
            num_sections = (len(content) - 1) // 4
            indices = {
                "sentences": [4 * i + 1 for i in range(num_sections)],
                "sent_level_umrs": [4 * i + 2 for i in range(num_sections)],
                "aligns": [4 * i + 3 for i in range(num_sections)],
                "doc_level_umrs": [4 * i + 4 for i in range(num_sections)]
            }

            # Verify all lists have the same length
            if len({len(lst) for lst in indices.values()}) == 1:
                # Retrieve and clean each section
                data_dict[txt_file.stem] = [
                    [content[i].strip() for i in indices[key]]
                    for key in ["sentences", "sent_level_umrs", "aligns", "doc_level_umrs"]
                ]
            else:
                # If section counts don't match, print debugging info
                print(f"Issue with file: {txt_file.name}")
                for key, idx_list in indices.items():
                    print(f"{key}: {idx_list}")
                print("Length mismatch in indices.")

    # Write the data to JSON file
    output_path = output_folder / f"{txt_folder.stem}.json"
    with output_path.open("w") as json_file:
        json.dump(data_dict, json_file, indent=4)
