import os
import time
from enum import Enum
from collections import Iterable


class FileType(Enum):
    IN_FILE = 1,
    OUT_FILE = 2,
    WIN_FILE = 3


def __get_extension(file_type):
    """Get extension of file based on its type."""
    if file_type == FileType.IN_FILE:
        return ".in"
    elif file_type == FileType.OUT_FILE:
        return ".out"
    elif file_type == FileType.WIN_FILE:
        return ".win"


def filename_stamped(filename, number):
    """Create a time-stamped filename"""
    time_str = time.strftime("%Y%m%d-%H%M%S")
    return '{}_{}_{}'.format(filename, number, time_str)


def __file_path_stamped(path, filename, file_extension, number):
    """Create filepath with filename time-stamped."""
    return os.path.join(path, filename_stamped(filename, number) + file_extension)


def save_to_file(experiment, file_type, number, candidates, voters, preferences=None, winners=None, subdir=False):
    """Save relevant structures to file depending on file type."""
    filename = experiment.inout_filename
    if file_type == FileType.WIN_FILE:
        filename = experiment.result_filename
    path = experiment.get_generated_dir_path()
    if subdir:
        path = os.path.join(path, experiment.result_filename)
    k = experiment.k
    file_extension = __get_extension(file_type)

    m = len(candidates)
    n = len(voters)

    file_path = __file_path_stamped(path, filename, file_extension, number)

    with open(file_path, 'w') as file:
        if file_type == FileType.WIN_FILE:
            file.write('{} {} {}\n'.format(m, n, k))
        else:
            file.write('{} {}\n'.format(m, n))

        if file_type == FileType.IN_FILE:
            __save_content(file, candidates)
            __save_content(file, voters)
        else:
            __save_candidates(file, candidates)
            __save_preferences(file, voters, preferences)
            if file_type == FileType.WIN_FILE:
                __save_winners(file, winners, candidates)


def __save_content(file, content):
    """Save structure content to file."""
    for i in range(len(content)):
        result = __get_content_string(content[i])
        file.write(result + '\n')


def __save_candidates(file, candidates):
    """Save candidates to file."""
    for i in range(len(candidates)):
        candidates_string = __get_content_string(candidates[i])
        result = '{} {}\n'.format(i, candidates_string)
        file.write(result)


def __save_preferences(file, voters, preferences):
    """Save preferences to file."""
    for i in range(len(preferences)):
        preference = __get_content_string(preferences[i].order)
        voter = __get_content_string(voters[i])
        result = '{} {}\n'.format(preference, voter)
        file.write(result)


def __save_winners(file, winners, candidates):
    """Save winners to file."""
    for i in winners:
        candidate = __get_content_string(candidates[i])
        result = '{} {}\n'.format(i, candidate)
        file.write(result)


def __get_content_string(content):
    """Create a string from content of a structure."""
    if isinstance(content, Iterable):
        return ' '.join(map(str, content))
    return str(content)
