import os
import time
from enum import Enum
from collections import Iterable


class FileType(Enum):
    IN_FILE = 1,
    OUT_FILE = 2,
    WIN_FILE = 3


def __get_extension(file_type):
    if file_type == FileType.IN_FILE:
        return ".in"
    elif file_type == FileType.OUT_FILE:
        return ".out"
    elif file_type == FileType.WIN_FILE:
        return ".win"


def __file_path_stamped(path, filename, file_extension, number):
    time_str = time.strftime("%Y%m%d-%H%M%S")
    temp_filename = '{}_{}_{}'.format(filename, number, time_str)
    return os.path.join(path, temp_filename + file_extension)


def save_to_file(experiment, file_type, number, candidates, voters, preferences=None, winners=None):
    filename = experiment.filename
    path = experiment.get_generated_dir_path()
    k = experiment.k
    file_extension = __get_extension(file_type)

    m = len(candidates)
    n = len(voters)

    file_path = __file_path_stamped(path, filename, file_extension, number)

    with open(file_path, 'w') as file:
        if file_type == FileType.IN_FILE:
            file.write('{} {}\n'.format(m, n))
            __save_content(file, candidates)
            __save_content(file, voters)
        else:
            file.write('{} {} {}\n'.format(m, n, k))
            __save_candidates(file, candidates)
            __save_preferences(file, voters, preferences)
            if file_type == FileType.WIN_FILE:
                __save_winners(file, winners, candidates)


def __save_content(file, content):
    for i in range(len(content)):
        result = __get_content_string(content[i])
        file.write(result + '\n')


def __save_candidates(file, candidates):
    for i in range(len(candidates)):
        candidates_string = __get_content_string(candidates[i])
        result = '{} {}\n'.format(i, candidates_string)
        file.write(result)


def __save_preferences(file, voters, preferences):
    for i in range(len(preferences)):
        preference = __get_content_string(preferences[i].order)
        voter = __get_content_string(voters[i][:-1])
        result = '{} {}\n'.format(preference, voter)
        file.write(result)


def __save_winners(file, winners, candidates):
    for i in range(len(winners)):
        candidate = __get_content_string(candidates[i])
        result = '{} {}\n'.format(i, candidate)
        file.write(result)


def __get_content_string(content):
    if isinstance(content, Iterable):
        return ' '.join(map(str, content))
    return str(content)
