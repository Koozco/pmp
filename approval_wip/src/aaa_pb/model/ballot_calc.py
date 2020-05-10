class BallotCalc(object):
    """Generates election instances from 2d input data points"""

    def calculateFrom2dPoints(self, V, C):
        raise NotImplementedError("Should have implemented this")

    def calculateFrom2PointsFile(self, input_file_path, output_file_path):
        raise NotImplementedError("Should have implemented this")

    def getShortName(self):
        raise NotImplementedError("Should have implemented this")

    pass

    def to_dict(self):
        raise NotImplementedError("Should have implemented this")

    def _get_params(self):
        raise NotImplementedError("Should have implemented this")
