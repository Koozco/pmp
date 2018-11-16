import copy
import inspect

from .helpers import Command


class ExperimentConfig:
    def __init__(self):
        self.__candidates = []
        self.__voters = []
        self.__commands = []
        self.two_dimensional = True

    def get_candidates(self):
        return copy.copy(self.__candidates)

    def set_candidates(self, list_of_candidates):
        self.__candidates = list_of_candidates

    def add_candidates(self, list_of_candidates):
        if inspect.isfunction(list_of_candidates):
            self.__commands.append((Command.GEN_CANDIDATES, list_of_candidates))
        else:
            self.__candidates += list_of_candidates

    def add_one_candidate(self, position, party='None'):
        self.__candidates += [position + (party,)]

    def set_voters(self, list_of_voters):
        self.__voters = list_of_voters

    def add_voters(self, list_of_voters):
        if inspect.isfunction(list_of_voters):
            args = len(inspect.getargspec(list_of_voters)[0])
            if args == 1:
                self.__commands.append((Command.GEN_FROM_CANDIDATES, list_of_voters))
            else:
                self.__commands.append((Command.GEN_VOTERS, list_of_voters))
        else:
            self.__voters += list_of_voters

    def add_one_voter(self, position, party='None'):
        self.__voters += [position + (party,)]

    def get_voters(self):
        return copy.copy(self.__voters)

    def add_command(self, value):
        self.__commands.append(value)

    def get_commands(self):
        return self.__commands

    # candidates in impartial only as a list of consecutive integers starting from 0
    def impartial(self, m, n):
        self.__commands.append((Command.IMPARTIAL, (m, n)))
