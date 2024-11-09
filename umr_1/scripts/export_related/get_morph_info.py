# when I export sanapana, kukama and navajo files, I didn't export the morphology information

import psycopg2, os
from typing import Tuple
from umr_1_postprocess.scripts.parse_input_xml import parse_flex12, parse_toolbox4
db = "umr_230523"

def get_content_file_format_given_doc_id(doc_id: int) -> Tuple[str, str]:
    conn = psycopg2.connect(
        host="localhost",
        database=db,
        user="postgres",
        password="5791628bb0b13ce0c676dfde280ba245"
    )
    cur = conn.cursor()
    # Execute the query to fetch all rows with the specified column value
    cur.execute("SELECT * FROM doc WHERE id = %s", (doc_id,))
    rows = cur.fetchall()
    # Close the cursor and the database connection
    cur.close()
    conn.close()

    return rows[0][3], rows[0][5] # uploaded document content, document format

def run_sanapana():
    sanapana_docs = {"EG_08312021.txt": 180, "EG_2_Raw.txt": 551, "exported_RL_Raw-78_v2.txt": 499,
                     "Marino_Doto_raw.txt": 538, "MO_2_raw.txt": 539, "RA_Gold_v2.txt": 465}

    for filename, doc_id in sanapana_docs.items():
        file_content, file_format = get_content_file_format_given_doc_id(doc_id)
        if file_format == "flex2":
            txt, dfs, sent_gls, conversation_turns, paragraph_groups = parse_flex12(file_content, file_format)
            print("txt: ", txt[0])
            print("dfs: ", dfs[0])
            print("sent_gls: ", sent_gls)
            print("conversation_turns: ", conversation_turns)
            print('paragraph_groups: ', paragraph_groups)
            os.makedirs(step3_sanapana_data_path, exist_ok=True)
            with open(os.path.join(step3_sanapana_data_path, filename), "w") as write_file:
                write_content = f"""user name: 
user id: 
file language: 
file format: 
Doc ID in database: {doc_id}
export time: 7/28/2023, 5:35:38 PM\n\n"""
                for index, df in enumerate(dfs):
                    snt_content = "# :: snt" + str(index + 1) + "\n" + df.to_string(index=True, header=False) + "\n"+ \
                                  "English Sent Gloss: " + sent_gls[index][0]  + "\n" + "Spanish Sent Gloss: "+ sent_gls[index][1] + "\n"
                    sent_annot = "# sentence level graph:\n"
                    doc_annot = "# document level annotation:\n"
                    align = "# alignment:\n"

                    write_content += snt_content + "\n"
                    write_content += sent_annot + "\n"
                    write_content += align + "\n"
                    write_content += doc_annot + "\n\n\n\n"
                write_file.write(write_content + "# Source File:\n")

def run_kukama():
    kukama_docs = {"exported_KUK_Sent-JVG_v2.txt": 450, "kuk1999oct01-02_1.txt": 700}
    for filename, doc_id in kukama_docs.items():
        file_content, file_format = get_content_file_format_given_doc_id(doc_id)
        if file_format == "toolbox4":
            txt, dfs, sents_gls, _, _ = parse_toolbox4(file_content)
            print("txt: ", txt[0])
            print("dfs: ", dfs[0])
            print("sent_gls: ", sents_gls)
            os.makedirs(step3_kukama_data_path, exist_ok=True)
            with open(os.path.join(step3_kukama_data_path, filename), "w") as write_file:
                write_content = f"""user name:
user id:
file language:
file format:
Doc ID in database: {doc_id}
export time: 7/28/2023, 5:35:38 PM\n\n"""
                for index, df in enumerate(dfs):
                    snt_content = "# :: snt" + str(index + 1) + "\n" + df.to_string(index=True, header=False) + "\n" + \
                                  "English Sent Gloss: " + sents_gls[index][0] + "\n" + "Spanish Sent Gloss"+ sents_gls[index][1] + "\n"
                    sent_annot = "# sentence level graph:\n"
                    doc_annot = "# document level annotation:\n"
                    align = "# alignment:\n"

                    write_content += snt_content + "\n"
                    write_content += sent_annot + "\n"
                    write_content += align + "\n"
                    write_content += doc_annot + "\n\n\n\n"
                write_file.write(write_content + "# Source File:\n")

def run_navajo():
    navajo_docs = {"A_Childhood_Tale.txt": 1185, "I_flew_over_Navajo_Land.txt": 554, "The_first_Mother-in-law.txt": 302,
                   "the_trouble_at_round_rock1.txt": 48, "the_trouble_at_round_rock2.txt": 153}
    for filename, doc_id in navajo_docs.items():
        file_content, file_format = get_content_file_format_given_doc_id(doc_id)
        if file_format == "flex2" or "flex1":
            txt, dfs, sent_gls, conversation_turns, paragraph_groups = parse_flex12(file_content, file_format)
            print("txt: ", txt[0])
            print("dfs: ", dfs[0])
            print("sent_gls: ", sent_gls)
            print("conversation_turns: ", conversation_turns)
            print('paragraph_groups: ', paragraph_groups)
            os.makedirs(step3_navajo_data_path, exist_ok=True)
            with open(os.path.join(step3_navajo_data_path, filename), "w") as write_file:
                write_content = f"""user name: 
user id: 
file language: 
file format: 
Doc ID in database: {doc_id}
export time: 7/28/2023, 5:35:38 PM\n\n"""
                for index, df in enumerate(dfs):
                    snt_content = "# :: snt" + str(index + 1) + "\n" + df.to_string(index=True, header=False) + "\n"+ \
                                  "English Sent Gloss: " + sent_gls[index][0]  + "\n" + "Spanish Sent Gloss: "+ sent_gls[index][1] + "\n"
                    sent_annot = "# sentence level graph:\n"
                    doc_annot = "# document level annotation:\n"
                    align = "# alignment:\n"

                    write_content += snt_content + "\n"
                    write_content += sent_annot + "\n"
                    write_content += align + "\n"
                    write_content += doc_annot + "\n\n\n\n"
                write_file.write(write_content + "# Source File:\n")
if __name__ == '__main__':
    # run_kukama()
    run_sanapana()
    # run_navajo()