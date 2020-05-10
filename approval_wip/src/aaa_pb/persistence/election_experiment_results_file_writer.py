from aaa_pb.output_file_paths_getter import OutputFilePathsGetter
from aaa_pb.model.elections_experiment import ElectionsExperiment
from aaa_pb.legacy_adapters.histogram import Histogram
from aaa_pb.persistence.new_experiment_file_writer import NewExperimentFileWriter


class ElectionExperimentResultsFileWriter:

    def __init__(self, elections_experiment: ElectionsExperiment,
                 output_file_path_getter: OutputFilePathsGetter) -> None:
        self.elections_experiment = elections_experiment
        self.output_file_path_getter = output_file_path_getter
        self.histogram = Histogram.fromElectionResults(
            election_results=elections_experiment.election_results
        )

    def writeResults_Text(self) -> 'ElectionExperimentResultsFileWriter':
        election_results = self.elections_experiment.getElectionResults()

        for i, election_result in enumerate(election_results):
            output_path = self.output_file_path_getter.pathForSingleElection_Text(election_index=i)

            NewExperimentFileWriter.writeToTextFile(
                election_result=election_result,
                path=output_path
            )

        return self

    def writeResults_Images(self) -> 'ElectionExperimentResultsFileWriter':
        election_results = self.elections_experiment.getElectionResults()

        for i, election_result in enumerate(election_results):
            output_path = self.output_file_path_getter.pathForSingleElection_Image(election_index=i)

            NewExperimentFileWriter.writeToImageFile(
                election_result=election_result,
                path=output_path
            )

        return self

    def writeHistogram_Text(self) -> 'ElectionExperimentResultsFileWriter':
        output_path = self.output_file_path_getter.pathForHistogram_Text()
        self.histogram.writeToTextFile(path=output_path)

        return self

    def writeHistogram_Image(self) -> 'ElectionExperimentResultsFileWriter':
        output_path = self.output_file_path_getter.pathForHistogram_Image()
        self.histogram.writeToImageFile(path=output_path)

        return self

    pass
