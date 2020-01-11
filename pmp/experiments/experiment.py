from random import seed

from .saving_files import save_to_file, FileType, filename_stamped
from ..preferences.ordinal import Ordinal
from ..preferences.profile import Profile
from ..rules.borda import Borda

from . import helpers
from .experiment_config import ExperimentConfig
from .generating_functions import impartial
from .helpers import Command, ExperimentElectionConfig
from .visualize import *

image_import_fail = False
try:
    from PIL import Image
except (ImportError, NameError):
    print("PIL module is not available. Pictures will not be generated.")
    image_import_fail = True


class Experiment:
    """Experiment to run"""

    def __init__(self, conf=None):
        self.__config = conf
        if conf is None:
            self.__config = ExperimentConfig()
        self.__generated_dir_path = "generated"  # default directory path for generated files
        self.k = 1
        self.rule = Borda
        self.inout_filename = "input-data"
        self.result_filename = "default"
        self.two_dimensional = True
        self.__generate_inout = False

    def set_generated_dir_path(self, dir_path):
        """Set a path to the directory where files are generated"""
        if not os.path.isabs(dir_path):
            dir_path = os.path.join(os.path.curdir, dir_path)
        self.__generated_dir_path = dir_path

    def get_generated_dir_path(self):
        """Get a path to the directory where files are generated"""
        return self.__generated_dir_path

    def set_election(self, rule, k):
        """Set election parameters: the rule and the size of the committee"""
        self.rule = rule
        self.k = int(k)

    def set_result_filename(self, name):
        """Set filename of result file."""
        self.result_filename = name

    def set_inout_filename(self, name):
        """Set filename of files containing generated candidates and voters"""
        self.__generate_inout = True
        self.inout_filename = name

    def run(self, visualization=False, n=1, save_win=False, save_in=False, save_out=False, log_on=True,
            elect_configs=None):
        """Run experiment"""
        dir_path = self.__generated_dir_path
        if self.__generate_inout:
            save_in = True
            save_out = True

        try:
            helpers.make_dirs(dir_path, exist_ok=True)
        except OSError as e:
            if not os.path.isdir(dir_path):
                raise e

        for i in range(n):
            candidates, voters, preferences = self.__execute_commands()

            if elect_configs is None:
                elect_configs = [ExperimentElectionConfig(self.rule, self.k, self.result_filename)]

            for elect_config in elect_configs:
                self.set_result_filename(elect_config.filename)
                self.set_election(elect_config.rule, elect_config.k)

                if log_on:
                    print('Candidates', candidates)
                    print('Voters', voters)

                if save_in:
                    save_to_file(self, FileType.IN_FILE, i, candidates, voters)
                if save_out:
                    save_to_file(self, FileType.OUT_FILE, i, candidates, voters, preferences)

                winners = self.__run_election(candidates, preferences)
                if log_on:
                    print('Winners', winners)

                if save_win:
                    save_to_file(self, FileType.WIN_FILE, i, candidates, voters, preferences, winners)

                if visualization:
                    self.__visualize(candidates, voters, winners, i)

    def __execute_commands(self):
        """Execute commands from config to compute candidates, voters and preferences"""
        candidates = self.__config.get_candidates()
        voters = self.__config.get_voters()
        preferences = []

        for experiment_command in self.__config.get_commands():
            command_type = experiment_command[0]
            args = experiment_command[1]
            if command_type == Command.GEN_CANDIDATES:
                candidates += experiment_command[1]()
            elif command_type == Command.GEN_VOTERS:
                voters += experiment_command[1]()
            elif command_type == Command.GEN_FROM_CANDIDATES:
                _, voters, preferences = experiment_command[1](candidates)
            elif command_type == Command.IMPARTIAL:
                candidates, voters, preferences = impartial(*args)
        if not preferences:
            preferences = preference_orders(candidates, voters)
        if any(isinstance(candidate, int) or len(candidate) != 3 for candidate in candidates):
            self.two_dimensional = False
        return candidates, voters, preferences

    # run election, compute winners
    def __run_election(self, candidates, preferences):
        """Run election"""
        seed()

        profile = Profile(candidates, preferences)
        if self.k > len(candidates):
            print("k is too big. Not enough candidates to find k winners.")
            return

        return self.rule().find_committee(self.k, profile)

    def __visualize(self, candidates, voters, winners, iteration):
        """Visualize winners from two-dimensional candidates and voters space"""
        if self.two_dimensional:
            if image_import_fail:
                print("Cannot visualize results because of PIL import fail.")
                return

            visualize(candidates, voters, winners, filename_stamped(self.result_filename, iteration),
                      self.__generated_dir_path)
        else:
            print("Cannot visualize non 2D.")


def compute_dist(v, candidates):
    """Compute the distances of voter v from the candidates in set C
    outputs a list of the format (i, d) where i is the candidate
    name and d is the distance"""
    m = len(candidates)
    d = [(j, dist(v, candidates[j])) for j in range(m)]
    return d


def preference_orders(candidates, voters):
    """Create Ordinal preferences list from candidates and voters"""
    preferences = []

    for v in voters:
        v_dist = compute_dist(v, candidates)
        v_sorted = sorted(v_dist, key=lambda x: x[1])
        v_order = [candidate_id for (candidate_id, _) in v_sorted]
        preferences += [Ordinal(v_order)]
    return preferences
