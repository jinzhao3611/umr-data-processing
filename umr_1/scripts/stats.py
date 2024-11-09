import os
import json
import penman
from pathlib import Path
from umr_1_postprocess.scripts.utils.io import txt2json
from umr_1_postprocess.scripts import OUT_DATA_PATH, FINAL_JSON_PATH


def convert_txt_to_json(out_data_path: Path, final_json_path: Path, languages: list) -> None:
    """
    Converts text files to JSON format for the specified languages.

    Args:
        out_data_path (Path): The base directory containing language-specific text files.
        final_json_path (Path): The directory where JSON files will be saved.
        languages (list): List of language subdirectories to process.
    """
    for language in languages:
        txt2json(out_data_path / language, final_json_path)


def gather_statistics(json_path: Path) -> dict:
    """
    Collects statistics on documents, sentences, tokens, and concepts from JSON files in the specified path.

    Args:
        json_path (Path): The directory containing JSON files to analyze.

    Returns:
        dict: A dictionary containing counts for documents, sentences, tokens, and concepts.
    """
    stats = {
        "doc_count": [],
        "sent_count": [],
        "token_count": [],
        "concepts_count": []
    }

    for json_file in json_path.glob("*.json"):
        with json_file.open('r', encoding='utf-8') as f:
            data = json.load(f)

        # Document count
        stats["doc_count"].append(len(data))

        # Process each document
        for umr_info in data.values():
            # Sentence count
            stats["sent_count"].append(len(umr_info[0]))

            # Token count per sentence
            for sent_display in umr_info[0]:
                tokens = extract_tokens(sent_display)
                stats["token_count"].append(len(tokens))

            # Concepts count per sentence-level UMR
            for sent_umr in umr_info[1]:
                concepts = extract_concepts(sent_umr)
                stats["concepts_count"].append(concepts)

    return stats


def extract_tokens(sentence: str) -> list:
    """
    Extracts tokens from a sentence display.

    Args:
        sentence (str): The sentence display string.

    Returns:
        list: A list of tokens.
    """
    lines = sentence.split("\n")
    sents_of_tokens = lines[1] if len(lines) > 1 else lines[0]
    return sents_of_tokens.split()


def extract_concepts(sent_umr: str) -> int:
    """
    Extracts and counts concepts in a sentence-level UMR.

    Args:
        sent_umr (str): The UMR representation of a sentence.

    Returns:
        int: The count of concepts in the UMR.
    """
    g = penman.decode(sent_umr[21:])
    return len(g.variables())


def print_statistics(stats: dict) -> None:
    """
    Prints the collected statistics.

    Args:
        stats (dict): A dictionary containing document, sentence, token, and concept counts.
    """
    print("Document Count per File:", stats["doc_count"])
    print("Total Document Count:", sum(stats["doc_count"]))
    print("Sentence Count per Document:", stats["sent_count"])
    print("Total Sentence Count:", sum(stats["sent_count"]))
    print("Token Count per Sentence:", stats["token_count"])
    print("Total Token Count:", sum(stats["token_count"]))
    print("Concepts Count per UMR:", stats["concepts_count"])
    print("Total Concepts Count:", sum(stats["concepts_count"]))


if __name__ == "__main__":
    # List of languages to process
    languages = ["arapaho", "chinese", "english", "kukama", "navajo", "sanapana"]

    # Convert text files to JSON
    convert_txt_to_json(Path(OUT_DATA_PATH), Path(FINAL_JSON_PATH), languages)

    # Gather statistics
    stats = gather_statistics(Path(FINAL_JSON_PATH))

    # Print statistics
    print_statistics(stats)
