from typing import List


def generate(
    input_file_path: str,
    search_word_list: List[str],
    stop_word_list: List[str],
):

    with open(input_file_path, "r") as file1:
        for line in file1:
            words_of_line = line.lower().split()
            if not set(words_of_line).isdisjoint(
                set([s.lower() for s in search_word_list])
            ) and set(words_of_line).isdisjoint(
                set([s.lower() for s in stop_word_list])
            ):
                yield line
