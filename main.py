
from sklearn.feature_extraction.text import CountVectorizer
import re
import pandas as pd
import os
import argparse


def convert_tuple_to_dict(data):
    added_keyword = set()
    dict_list= []
    for row in data:
        word_dict = {}
        if row[0] in added_keyword:
            for record in dict_list:
                if record["Word"] == row[0]:
                    record["Total Occurences"] += row[1]
                    if row[2] not in record["Document"]:
                        record["Document"] = record["Document"] + "," + row[2]
                    record["Sentences containing the word"] = record["Sentences containing the word"] + "\n" + row[3]
                    break
        else:
            word_dict = {
                "Word": row[0],
                "Total Occurences": row[1],
                "Document": row[2],
                "Sentences containing the word": row[3],
            }
            dict_list.append(word_dict)
            added_keyword.add(row[0])
    return dict_list


def get_table_of_interesting_words(directory, number=20):
    results = []
    if not os.path.isdir(directory) or not os.listdir(directory):
        print(f"Directory {directory} either does not exist or is empty. Make sure the supplied directory has files in it.")
        return
    for file in os.listdir(directory):
        file_name = os.path.join(directory, file)
        words = [line.replace("\n", "") for line in open(file_name)]
        result = get_word_frequency(words, file)
        results.extend(result)

    result_dict = convert_tuple_to_dict(results)
    common_words = sorted(result_dict, key = lambda x: x["Total Occurences"], reverse=True)
    table_of_words = pd.DataFrame(common_words[:number])
    table_of_words.to_html('result.html')


def get_word_frequency(corpus, file_name, max_word_len=7):
    vectorizer = CountVectorizer().fit(corpus)
    bag_of_words = vectorizer.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_frequency = []
    for word, idx in vectorizer.vocabulary_.items():
        if len(word) > max_word_len:
            corpus = str(corpus).lower()
            sentence = re.findall(r"([^.]*?"+word+"[^.]*\.)", corpus)
            words_frequency.append((word, sum_words[0, idx], file_name, "".join(sentence)))
    return words_frequency


if __name__ == "__main__":
    parse = argparse.ArgumentParser(
        description="Required args to perform the operation."
    )
    parse.add_argument("--directory", help="Folder where the text files are", type=str, required=True)
    parse.add_argument("--number", help="Number of records to return", type=int, required=False)
    args = parse.parse_args()
    get_table_of_interesting_words(args.directory, args.number)