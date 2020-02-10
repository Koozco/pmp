from random import seed

from .saving_files import save_to_file, FileType, filename_stamped
from ..preferences import Preference
from ..preferences.ordinal import Ordinal
from ..preferences.profile import Profile
from ..rules.borda import Borda

from . import helpers
from .experiment_config import ExperimentConfig
from .election_config import ElectionConfig
from .generating_functions import impartial
from .helpers import Command
from .visualize import *

image_import_fail = False
try:
    from PIL import Image
except (ImportError, NameError):
    print('PIL module is not available. Pictures will not be generated.')
    image_import_fail = True


class Experiment:
    """Experiment to run"""

    def __init__(self, config=None):
        """
        :param config: Experiment's configuration
        :type config: ExperimentConfig
        """
        self.__config = config
        if config is None:
            self.__config = ExperimentConfig()
        self.__generated_dir_path = 'generated'  # default directory path for generated files
        self.k = 1
        self.rule = Borda()
        self.election_configs = []
        self.inout_filename = 'input-data'
        self.result_filename = 'default'
        self.two_dimensional = True
        self.__generate_inout = False

    def run(self, visualization=False, n=1, save_win=False, save_in=False, save_out=False, log_on=True,
            elect_configs=None, split_dirs=True):
        """
        :param visualization:
        :type visualization: bool
        :param n:
        :type n: int
        :param save_win:
        :type save_win: bool
        :param save_in:
        :type save_in: bool
        :param save_out:
        :type save_out: bool
        :param log_on:
        :type log_on: bool
        :param elect_configs: Election configs. If given, experiment ignores it's one-rule configuration
        :type elect_configs: List[ElectionConfig]
        :param split_dirs: When True create separate directory for each election related files
        :type split_dirs: bool

        Run experiment. Experiment runs elections configured in following precedence:
        * from elect_configs parameter, if present
        * set up from election_configurations added by add_election, if added
        * set up from set_election
        """
        dir_path = self.__generated_dir_path
        if self.__generate_inout:
            save_in = True
            save_out = True

        try:
            helpers.make_dirs(dir_path, exist_ok=True)
        except OSError as e:
            if not os.path.isdir(dir_path):
                raise e

        election_configurations = []
        if elect_configs is not None:
            election_configurations = elect_configs
        elif len(self.election_configs) > 0:
            election_configurations = self.election_configs
        else:
            election_configurations = [ElectionConfig(self.rule, self.k, self.result_filename)]

        if split_dirs:
            for config in election_configurations:
                path = os.path.join(dir_path, config.id)
                try:
                    helpers.make_dirs(path, exist_ok=True)
                except OSError as e:
                    if not os.path.isdir(path):
                        raise e

        for i in range(n):
            print('{}/{}'.format(i+1, n))
            candidates, voters, preferences = self.__execute_commands()

            for elect_config in election_configurations:
                self.set_result_filename(elect_config.id)
                self.set_election(elect_config.rule, elect_config.k)

                if log_on:
                    print('Candidates', candidates)
                    print('Voters', voters)

                if save_in:
                    save_to_file(self, FileType.IN_FILE, i, candidates, voters, subdir=split_dirs)
                if save_out:
                    save_to_file(self, FileType.OUT_FILE, i, candidates, voters, preferences, subdir=split_dirs)

                winners = self.__run_election(candidates, preferences)
                if log_on:
                    print('Winners', winners)

                if save_win:
                    save_to_file(
                        self, FileType.WIN_FILE, i, candidates, voters, preferences, winners, subdir=split_dirs
                    )

                if visualization:
                    self.__visualize(candidates, voters, winners, i)

    def add_election(self, rule, k, id):
        """
        :param rule: Scoring rule for added election
        :type rule: Rule
        :param k: Size of the winning committee for added election
        :type k: int
        :param id: Text id for the election. Builds up first part of output filenames
        :type id: str

        For multi-rule experiments. It's preferred way of defining elections in experiments.
        """
        self.election_configs.append(ElectionConfig(rule, k, id))

    def set_generated_dir_path(self, dir_path):
        """
        :param dir_path: Path to the root directory where files are generated
        :type dir_path: str
        """
        if not os.path.isabs(dir_path):
            dir_path = os.path.join(os.path.curdir, dir_path)
        self.__generated_dir_path = dir_path

    def get_generated_dir_path(self):
        """
        :returns: Path to the root directory where files are generated
        :rtype: str
        """
        return self.__generated_dir_path

    def set_election(self, rule, k):
        """
        :param rule: Scoring rule being set
        :type rule: Rule
        :param k: Size of the committee being set
        :type k: int

        [Deprecated]
        Set election parameters the rule and the size of the committee.
        Overrides previous experiment setup. Only for setting up one-rule experiments.
        """
        self.rule = rule
        self.k = int(k)

    def set_result_filename(self, name):
        """
        :param name: Result filename
        :type name: str

        [Deprecated]
        Set result name. It builds up first part of names of all files being generated during experiment.
        Overrides previous value. Only for setting up one-rule experiments.
        """
        self.result_filename = name

    def set_inout_filename(self, name):
        """
        :param name: Inout filename
        :type name: str

        Set filename of files containing generated candidates and voters.
        Overrides previous value. Only for setting up one-rule experiments.
        """
        self.__generate_inout = True
        self.inout_filename = name

    def get_config_id(self):
        return self.__config.id

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
            if isinstance(voters[0], Preference):
                preferences = voters
            else:
                preferences = preference_orders(candidates, voters)
        if any(isinstance(candidate, int) or len(candidate) != 3 for candidate in candidates):
            self.two_dimensional = False
        return candidates, voters, preferences

    def __run_election(self, candidates, preferences):
        """
        :param candidates:
        :type candidates: List
        :param preferences:
        :type preferences: List[Preference]

        Run election, compute winners
        """
        seed()

        profile = Profile(candidates, preferences)
        if self.k > len(candidates):
            print("k is too big. Not enough candidates to find k winners.")
            return

        return self.rule.find_committee(self.k, profile)

    def __visualize(self, candidates, voters, winners, iteration):
        """
        :param candidates:
        :type candidates: List[Tuple[Number]]
        :param voters:
        :type voters: List[Tuple[Number]]
        :param winners: Winning candidates id's
        :type winners: List[int]
        :param iteration:
        :type iteration: int

        Visualize winners from two-dimensional candidates and voters space
        """
        if self.two_dimensional:
            if image_import_fail:
                print("Cannot visualize results because of PIL import fail.")
                return

            visualize(candidates, voters, winners, filename_stamped(self.result_filename, iteration),
                      self.__generated_dir_path)
        else:
            print("Cannot visualize non 2D.")


def compute_dist(v, candidates):
    """
    :param v: voter
    :type v: Tuple[Number]
    :param candidates:
    :type candidates: List[Tuple[Number]]

    Compute the distances of voter v from the candidates in set C
    outputs a list of the format (i, d) where i is the candidate
    name and d is the distance.
    """
    m = len(candidates)
    d = [(j, dist(v, candidates[j])) for j in range(m)]
    return d


def preference_orders(candidates, voters):
    """
    :param candidates:
    :type candidates: List[Tuple[Number]]
    :param voters:
    :type voters: List[Tuple[Number]]
    :rtype: List[Ordinal]

    Create Ordinal preferences list from n-dimensional candidates and voters.
    """
    preferences = []

    for v in voters:
        v_dist = compute_dist(v, candidates)
        v_sorted = sorted(v_dist, key=lambda x: x[1])
        v_order = [candidate_id for (candidate_id, _) in v_sorted]
        preferences += [Ordinal(v_order)]
    return preferences
