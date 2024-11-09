import re
from scripts.utils import read_txt_file, write_txt_file

def fix_and_write(in_file_path, out_file_path) -> None:
    text = read_txt_file(in_file_path)

    pattern = r'# workset tutorial (generated on Wed Nov 8, 2023 at 10:00:27 for user consensus)'
    text = text.replace(pattern, '').strip()

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
            if line.startswith("# ::id ") or line.startswith("# ::save-date") or line.startswith("# ::note "):
                new_text += ""
            elif line.startswith("# ::snt"):
                modified_line = re.sub(r'(::snt )', f':: snt{i+1} ', line)
                sentence_text = re.sub(r'# ::snt ', '', line)
                sentences.append(sentence_text)
                new_text += modified_line + "\n" + "# sentence level graph:" + "\n"
            else:
                #add sentence number to the variables
                #match h, s, h1, s3, h11, but cannot match s1n,s1n1,s1n22, but cannot match above s\d+\w\d*
                new_line = re.sub(r'(\()(\w\d*\s)', rf'\1s{str(i+1)}\2', line)
                new_text += new_line + "\n"
        new_text += "# alignment:" + "\n"
        # new_text += "# document level annotation:" + "\n" + f"(s{i+1}s0 / sentence)" + "\n"
        new_text += "# document level annotation:" + "\n"
        new_text += "\n"

    new_text += "# Source File: " + "\n"
    for sentence_text in sentences:
        new_text += sentence_text + "\n"

    write_txt_file(new_text, out_file_path)


if __name__ == '__main__':
    in_file_path = "input/AMR-parallel-tutorial-UMR.txt"
    out_file_path = "output/AMR-parallel-tutorial-UMR.txt"
    fix_and_write(in_file_path, out_file_path)
