from typing import List, Union, TextIO


def generate(
    input_file: Union[str, TextIO],
    search_word_list: List[str],
    stop_word_list: List[str],
):
    search_word_list = {word.lower() for word in search_word_list}
    stop_word_list = {word.lower() for word in stop_word_list}

    if isinstance(input_file, str):
        with open(input_file, "r", encoding='UTF-8') as open_file:
            file = open_file.read()
    else:
        file = input_file

    for line in file:
        words_of_line = set(line.lower().split())

        if not words_of_line.isdisjoint(
            search_word_list
        ) and words_of_line.isdisjoint(
            stop_word_list
        ):
            yield line
