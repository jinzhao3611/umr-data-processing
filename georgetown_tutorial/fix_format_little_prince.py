import re
from scripts.utils import read_txt_file, write_txt_file, read_json_file, write_json_file, json2txt, txt2json

def fix_and_write(in_file_path, out_file_path) -> None:
    text = read_txt_file(in_file_path)

    pattern = r'# AMR \(Abstract Meaning Representation\) release v3\.0\n# Le Petit Prince \("The Little Prince"\), a 1943 novel by Antoine de Saint-Exupery \(1562 sentences\)\n# generated on .*'
    text = re.sub(pattern, '', text).strip()

    new_text = """user name: jin2
user id: 2
file language: english
file format: plain_text
Doc ID in database: N/A
export time: 1/10/2024, 11:38:07 PM\n\n"""
    blocks = text.split("\n\n")
    sentences = []
    for i, block in enumerate(blocks):
        for line in block.split("\n"):
            if line.startswith("# ::id ") or line.startswith("# ::save-date"):
                new_text += ""
            elif line.startswith("# ::snt"):
                modified_line = re.sub(r'(::snt )', f':: snt{i+1} ', line)
                sentence_text = re.sub(r'# ::snt ', '', line)
                sentences.append(sentence_text)
                new_text += modified_line + "\n" + "# sentence level graph:" + "\n"
            else:
                new_text += line + "\n"
        new_text += "# alignment:" + "\n"
        new_text += "# document level annotation:" + "\n" + f"(s{i+1}s0 / sentence)" + "\n"
        # new_text += "# document level annotation:" + "\n"
        new_text += "\n"

    new_text += "# Source File: " + "\n"
    for sentence_text in sentences:
        new_text += sentence_text + "\n"

    write_txt_file(new_text, out_file_path)


if __name__ == '__main__':
    in_file_path = "input/Little-Prince_1st-20-sent_UMR.txt"
    out_file_path = "output/Little-Prince_1st-20-sent_UMR.txt"
    fix_and_write(in_file_path, out_file_path)
