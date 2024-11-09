import os, re

import penman

def fill_in_alignments(input_text):
    output = []
    sentences = []
    parts = [item for item in input_text.split("#") if item != ""]
    # for p in parts:
    #     print(p)
    for i in range(0, len(parts), 2):
        print("here: ", i)
        sentence = re.sub(r":: snt\d+", "", parts[i]).strip()
        graph = parts[i + 1].strip()
        # Formatting output
        # print(graph)
        g = penman.decode(graph.replace("sentence level graph", ""))
        alignment = ": 0-0\n".join(sorted(g.variables())) + ": 0-0\n"
        output.append(
            f"# :: snt{int((i + 2) / 2)}\tSentence: {sentence}\n\n# {graph}\n\n# alignment:\n{alignment}\n# document level annotation:\n")
        sentences.append(sentence)
        # print(f"Here: # :: snt{int((i + 1) / 2)}\tSentence: {sentence}\n\n# {graph}\n\n# alignment:\n{alignment}\n# document level annotation:\n")


    prefix = """user name:
user id:
file language: chinese
file format: plain_text
Doc ID in database:
export time:\n\n"""

    suffix = """\n# Source File: \n""" + "\n".join(sentences)
    output = prefix + "\n".join(output) + suffix
    output = output.replace(":aspect", ":Aspect")
    output = output.replace(":modstr", ":MODSTR")
    return output


if __name__ == '__main__':
    input_folder_path = "/Users/jinzhao/schoolwork/lab-work/umr-postprocess/data/LLM_parsed/batch3/"
    output_folder_path = "/Users/jinzhao/schoolwork/lab-work/umr-postprocess/data/LLM_parsed/batch3_processed/"

    for filename in os.listdir(input_folder_path):
        print(filename)
        input_file_path = os.path.join(input_folder_path, filename)
        output_file_path = os.path.join(output_folder_path, filename)
        with open(input_file_path, "r") as f:
            input_text = f.read()
        output_text = fill_in_alignments(input_text)
        with open(output_file_path, "w") as f:
            f.write(output_text)
        fill_in_alignments(input_text)


