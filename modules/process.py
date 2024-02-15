from typing import List


def process_usernames(input_file: str) -> None:
    with open(input_file, 'r') as file:
        lines = [line.strip() for line in file]

    unique_lines = list(dict.fromkeys(lines))

    with open(input_file, 'w') as out_file:
        out_file.write('\n'.join(unique_lines))
