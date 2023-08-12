import numpy as np
from scipy.spatial.distance import cosine
from scipy.spatial.distance import euclidean


class KNN:

    def __init__(self, items, descriptors):
        self.items = items
        self.descriptors = descriptors

    def calc_order(self, unknown_decs):
        distances = [euclidean(unknown_decs, desc) for desc in self.descriptors]
        results = dict(zip(self.items, distances))
        results = ([[str(key), float(results[key])] for key in sorted(results, key=results.get)])
        order = sorted(results, key=lambda x: x[1])
        order = [[_[0], max(1-_[1], 0)] for _ in order]
        return order



