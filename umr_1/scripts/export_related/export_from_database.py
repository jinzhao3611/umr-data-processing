# export Jens’ Sanapana, Kukama and Navajo from database, get the files in step0 folder
from collections import defaultdict
from bs4 import BeautifulSoup
import psycopg2, os
from typing import Tuple
from parse_input_xml import parse_flex12, parse_toolbox4, parse_toolbox3
db = "umr_230523"
langs = ["sanapana", "kukama", "navajo"]

def get_doc_ids_given_lang(lang):
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        database=db,
        user="postgres",
        password="5791628bb0b13ce0c676dfde280ba245"
    )

    # Create a cursor object to interact with the database
    cur = conn.cursor()

    # Execute the query to fetch all rows with the specified column value
    cur.execute("SELECT * FROM doc WHERE lang = %s", (lang,))

    # Fetch all rows from the query result
    rows = cur.fetchall()

    doc_ids = []
    # Process the rows
    for row in rows:
        doc_ids.append(row[0])

    # Close the cursor and the database connection
    cur.close()
    conn.close()
    return doc_ids

def get_annotations_given_doc_id(doc_id):
    annotations = []
    conn = psycopg2.connect(
        host="localhost",
        database=db,
        user="postgres",
        password="5791628bb0b13ce0c676dfde280ba245"
    )
    # Create the cursor object
    cursor = conn.cursor()

    # Execute the SELECT query with the condition
    query = f"SELECT * FROM annotation WHERE doc_id = %s;"
    cursor.execute(query, (doc_id,))
    # Fetch the rows that match the condition
    rows = cursor.fetchall()

    # Process the retrieved data
    for row in rows:
        annotations.append(row)
    cursor.close()
    conn.close()
    return annotations

def get_doc_name_given_doc_id(doc_id):
    conn = psycopg2.connect(
        host="localhost",
        database=db,
        user="postgres",
        password="5791628bb0b13ce0c676dfde280ba245"
    )
    # Create the cursor object
    cursor = conn.cursor()

    # Execute the SELECT query with the condition
    query = f"SELECT * FROM doc WHERE id = %s;"
    cursor.execute(query, (doc_id,))
    # Fetch the rows that match the condition
    row = cursor.fetchall()[0]
    cursor.close()
    conn.close()
    return row[1]

def get_user_given_user_id(user_id):
    conn = psycopg2.connect(
        host="localhost",
        database=db,
        user="postgres",
        password="5791628bb0b13ce0c676dfde280ba245"
    )
    # Create the cursor object
    cursor = conn.cursor()

    # Execute the SELECT query with the condition
    query = f"SELECT * FROM \"user\" WHERE id = %s;"
    cursor.execute(query, (user_id,))
    # Fetch the rows that match the condition
    row = cursor.fetchall()[0]
    cursor.close()
    conn.close()
    return row[1]

def get_sent_content_given_doc_id_sent_id(doc_id, sent_id):
    conn = psycopg2.connect(
        host="localhost",
        database=db,
        user="postgres",
        password="5791628bb0b13ce0c676dfde280ba245"
    )
    # Create the cursor object
    cursor = conn.cursor()

    # Execute the SELECT query with the condition
    query = f"SELECT * FROM sent WHERE doc_id = %s;"
    cursor.execute(query, (doc_id,))
    # Fetch the rows that match the condition
    rows = cursor.fetchall()
    sorted_rows = sorted(rows, key=lambda x:x[0])
    cursor.close()
    conn.close()
    return sorted_rows[sent_id-1][1]

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

def get_sent_morph_given_doc_id_sent_id(doc_id, sent_id):
    file_content, file_format = get_content_file_format_given_doc_id(doc_id)
    if file_format == "toolbox4":
        txt, dfs, sents_gls, _, _ = parse_toolbox4(file_content)
        # print("txt: ", txt[0])
        # print("dfs: ", dfs[0])
        # print("sent_gls: ", sents_gls)
        snt_morph = "# :: snt" + str(sent_id) + "\n" + dfs[sent_id-1].to_string(index=True, header=False) + "\n" + \
                    "English Sent Gloss: " + sents_gls[sent_id-1][0] + "\n" + "Spanish Sent Gloss" + \
                    sents_gls[sent_id-1][1] + "\n"
        return snt_morph
    elif file_format == "toolbox3":
        sents_of_words, dfs, sents_gls, notes, _ = parse_toolbox3(file_content)
        snt_morph = "# :: snt" + str(sent_id) + "\n" + dfs[sent_id - 1].to_string(index=True, header=False) + "\n" + \
                    "English Sent Gloss: " + sents_gls[sent_id - 1][0] + "\n" + "Spanish Sent Gloss" + \
                    sents_gls[sent_id - 1][1] + "\n"
        return snt_morph
    elif file_format == "flex2":
        txt, dfs, sent_gls, conversation_turns, paragraph_groups = parse_flex12(file_content, file_format)
        # print("txt: ", txt[0])
        # print("dfs: ", dfs[0])
        # print("sent_gls: ", sent_gls)
        # print("conversation_turns: ", conversation_turns)
        # print('paragraph_groups: ', paragraph_groups)
        snt_morph = "# :: snt" + str(sent_id) + "\n" + dfs[sent_id-1].to_string(index=True,
                                                                        header=False) + "\n" + \
                      "English Sent Gloss: " + sent_gls[sent_id-1][0] + "\n" + "Spanish Sent Gloss: " + \
                      sent_gls[sent_id-1][1] + "\n"
        return snt_morph

    elif file_format == "flex2" or file_format == "flex1":
        txt, dfs, sent_gls, conversation_turns, paragraph_groups = parse_flex12(file_content, file_format)
        # print("txt: ", txt[0])
        # print("dfs: ", dfs[0])
        # print("sent_gls: ", sent_gls)
        # print("conversation_turns: ", conversation_turns)
        # print('paragraph_groups: ', paragraph_groups)
        snt_morph = "# :: snt" + str(sent_id) + "\n" + dfs[sent_id-1].to_string(index=True, header=False) + "\n"+ \
                      "English Sent Gloss: " + sent_gls[sent_id-1][0]  + "\n" + "Spanish Sent Gloss: "+ sent_gls[sent_id-1][1] + "\n"
        return snt_morph

    else:
        print("unknown format: " + file_format)
        return ""

def split_annotations_given_user_id(annotations):
    result_dict = {}  # Dictionary to hold the split lists
    for item in annotations:
        value = item[2]  # user_id
        if value not in result_dict:
            result_dict[value] = []  # Create a new list for this value
        result_dict[value].append(item)  # Append the tuple to the appropriate list

    # Convert the dictionary values to lists
    result_lists = list(result_dict.values())
    return result_lists

def write_annotation_to_exported_file(lang, document_annotations):
    sorted_document_annotations = sorted(document_annotations, key=lambda x:x[3]) #sort based on sent_id
    sorted_document_annotations_multi_users = split_annotations_given_user_id(sorted_document_annotations)
    if lang == 'sanapana':
        folder_path = "step0_sanapana_data_path"
    elif lang == 'navajo':
        folder_path = "step0_navajo_data_path"
    elif lang == 'kukama':
        folder_path = "step0_kukama_data_path"
    else:
        raise FileNotFoundError

    for sorted_document_annotations_per_user in sorted_document_annotations_multi_users:
        user_id = sorted_document_annotations_per_user[0][2]
        doc_id = sorted_document_annotations_per_user[0][1]
        doc_name = get_doc_name_given_doc_id(doc_id)
        user_name = get_user_given_user_id(user_id)
        os.makedirs(folder_path, exist_ok=True)
        first_sent_annotation = BeautifulSoup(sorted_document_annotations_per_user[0][6], "html.parser").get_text()
        if first_sent_annotation and first_sent_annotation != "empty umr":  # if first sentence has sent level annotation
            with open(os.path.join(folder_path, doc_name[:-4]) + f'_user_{user_id}.txt', "w") as write_file:
                write_content = f"""user name: {user_name}
user id: {user_id}
file language: {lang}
file format: 
Doc ID in database: {doc_id}
export time: 7/28/2023, 5:35:38 PM\n\n"""
                for sent_annotation in sorted_document_annotations_per_user:
                    if BeautifulSoup(sent_annotation[6], "html.parser").get_text(): #if sent level annotation exist
                        sent_annot = "# sentence level graph:\n" + BeautifulSoup(sent_annotation[6], "html.parser").get_text()
                        doc_annot = "# document level annotation:\n" + BeautifulSoup(sent_annotation[7], "html.parser").get_text()
                        align = "# alignment:\n" + "\n".join([f"{key} :{value}"for key, value in sent_annotation[8].items()])
                        # content = get_sent_content_given_doc_id_sent_id(doc_id=sent_annotation[1], sent_id=sent_annotation[3])
                        # snt_content = "# :: snt" + str(sent_annotation[3]) + "\t" + content + "\n"
                        snt_content = get_sent_morph_given_doc_id_sent_id(doc_id=doc_id, sent_id=sent_annotation[3])

                        write_content += snt_content + "\n"
                        write_content += sent_annot + "\n"
                        write_content += align + "\n"
                        write_content += doc_annot + "\n\n\n\n"
                    else:
                        break
                write_file.write(write_content)

def run():
    docs_wz_all_info = defaultdict(list)
    langs = ['kukama', 'navajo', 'sanapana']
    for lang in langs:
        doc_ids = get_doc_ids_given_lang(lang)
        print(doc_ids)
        for doc_id in doc_ids:
            annotations = get_annotations_given_doc_id(doc_id)
            docs_wz_all_info[lang].append(annotations)

    for lang, many_documents_of_annotation_rows in docs_wz_all_info.items():
        for one_document_of_annotation_rows in many_documents_of_annotation_rows:
            if len(one_document_of_annotation_rows) > 0: #throw out documents has less than 1 annotation
                write_annotation_to_exported_file(lang=lang, document_annotations=one_document_of_annotation_rows)


