from helpers import Command
import inspect
import copy


class ExperimentConfig:
    def __init__(self):
        self.__candidates = []
        self.__voters = []
        self.__commands = []
        self.__two_dimensional = True

    def set_two_dimensional(self, value):
        self.__two_dimensional = value

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

    def is_two_dimensional(self):
        return self.__two_dimensional

    def add_command(self, value):
        self.__commands.append(value)

    def get_commands(self):
        return self.__commands

    def impartial(self, m, n):
        self.__commands.append((Command.IMPARTIAL, (m, n)))
