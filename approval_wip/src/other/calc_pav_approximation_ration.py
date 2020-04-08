import numpy
import pathlib

# python/voting-rules/mw2d-experiments/experiment_synthetic_pav/
# elections_unidisc_CC_Greedy_nearest-uniform10.0-10.0_k10/CC_Greedy_k10_0.txt
from aaa_pb.rules.approval.single_committee_value import CommitteeScore


class CalculateApproximationRatio:

    @classmethod
    def readElectionResult(self, electionResultPath):
        # type: (pathlib.Path) -> dict

        # TODO read from file

        with open(str(electionResultPath), 'r') as f:
            lines = f.readlines()

        candidatesNo, votersNo, k = [int(x.strip()) for x in lines[0].split(" ")]
        assert len(lines) == votersNo + candidatesNo + k + 1

        candidatesRaw = [x.strip() for x in lines[1: 1 + candidatesNo ]]
        assert len(candidatesRaw) == candidatesNo


        def parseVoterLine(line):
            items = [x.strip() for x in line.split(" ")]
            _coordinates = items[0] + " " + items[1]
            ballot = [int(x) for x in items[2:]]
            return ballot

        votersRaw = lines[1 + candidatesNo: 1 + candidatesNo + votersNo]
        assert len(votersRaw) == votersNo
        V = [parseVoterLine(x) for x in votersRaw]

        committeeRaw = lines[1 + candidatesNo + votersNo: 1 + candidatesNo + votersNo + k]
        assert len(committeeRaw) == k

        committee = [candidatesRaw.index(x.strip()) for x in committeeRaw]

        return {
            'V': V,
            'k': k,
            'number_of_candidates': candidatesNo,
            'committee': committee
        }

    @classmethod
    def calculatePavScore(self, electionResult):
        # type: (dict) -> float

        return CommitteeScore.PAV(
            V=electionResult['V'],
            committee=electionResult['committee']
        )

    @classmethod
    def readElectionResults(self, electionsDir, getElectionResultFileName, electionNumbers):
        # type: (pathlib.Path, callable, list) -> list[dict]

        results = []
        for electionNumber in electionNumbers:
            resultFilePath = electionsDir / getElectionResultFileName(electionNumber)
            results.append(self.readElectionResult(resultFilePath))

        return results

    @classmethod
    def calculate(self, optimalElectionResults, approximateElectionResults):
        # type: (list[dict], list[dict]) -> list[float]

        optScores = [self.calculatePavScore(x) for x in optimalElectionResults]
        appScores = [self.calculatePavScore(x) for x in approximateElectionResults]

        assert len(optScores) == len(appScores)

        ratios = [a / o for o, a in zip(optScores, appScores)]

        return ratios


def getElectionResultFileNameFun(ruleName):
    return lambda fileNumber: "{0}_k10_{1}.txt".format(ruleName, fileNumber)


def calcMean(l):
    return sum(l)/float(len(l))


def calcStd(l):
    mean = calcMean(l)
    sumOfSquaresOfDiffs = sum([(x - mean)**2 for x in l])
    return sumOfSquaresOfDiffs**0.5


if __name__ == '__main__':
    experimentBaseDirStr = '~/src/code-misc/python/voting-rules/mw2d-experiments/experiment_synthetic_pav/'
    experimentBaseDir = pathlib.Path(experimentBaseDirStr).expanduser()

    PAV_Greedy_nearest_elections = experimentBaseDir / 'elections_unidisc_PAV_Greedy_nearest-uniform10.0-10.0_k10'
    PAV_Greedy_radius_elections = experimentBaseDir / 'elections_unidisc_PAV_Greedy_radius-uniform1.05-1.05_k10'

    PAV_ILP_nearest_elections = experimentBaseDir / 'elections_unidisc_PAV_ILP_nearest-uniform10.0-10.0_k10'
    PAV_ILP_radius_elections = experimentBaseDir / 'elections_unidisc_PAV_ILP_radius-uniform1.05-1.05_k10'

    electionNumbers = range(2000)

    PAV_Greedy_nearest_electionResults = CalculateApproximationRatio.readElectionResults(
        electionsDir=PAV_Greedy_nearest_elections,
        getElectionResultFileName=getElectionResultFileNameFun('PAV_Greedy'),
        electionNumbers=electionNumbers
    )

    PAV_Greedy_radius_electionResults = CalculateApproximationRatio.readElectionResults(
        electionsDir=PAV_Greedy_radius_elections,
        getElectionResultFileName=getElectionResultFileNameFun('PAV_Greedy'),
        electionNumbers=electionNumbers
    )

    PAV_ILP_nearest_electionResults = CalculateApproximationRatio.readElectionResults(
        electionsDir=PAV_ILP_nearest_elections,
        getElectionResultFileName=getElectionResultFileNameFun('PAV_ILP'),
        electionNumbers=electionNumbers
    )

    PAV_ILP_radius_electionResults = CalculateApproximationRatio.readElectionResults(
        electionsDir=PAV_ILP_radius_elections,
        getElectionResultFileName=getElectionResultFileNameFun('PAV_ILP'),
        electionNumbers=electionNumbers
    )

    ratios_PAV_nearest = CalculateApproximationRatio.calculate(
        optimalElectionResults=PAV_ILP_nearest_electionResults,
        approximateElectionResults=PAV_Greedy_nearest_electionResults
    )

    ratios_PAV_radius = CalculateApproximationRatio.calculate(
        optimalElectionResults=PAV_ILP_radius_electionResults,
        approximateElectionResults=PAV_Greedy_radius_electionResults
    )

    arr = numpy.array([ratios_PAV_nearest, ratios_PAV_radius])

    def meanAndStd(l, msg):
        m = calcMean(l)
        s = calcStd(l)
        print("{0}: mean: {1}, std: {2}".format(msg, m, s))

    meanAndStd(ratios_PAV_radius, 'ratios_PAV_radius (Greedy/ILP)')
    meanAndStd(ratios_PAV_nearest, 'ratios_PAV_nearest (Greedy/ILP)')

    # ratios_PAV_radius (Greedy/ILP): mean: 0.995750353897, std: 0.192095846852
    # ratios_PAV_nearest (Greedy/ILP): mean: 0.996407786827, std: 0.179251542003
