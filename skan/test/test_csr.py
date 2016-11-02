import os, sys
import numpy as np
from numpy.testing import assert_equal, assert_almost_equal
from skan import csr

rundir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(rundir)

from skan._testdata import tinycycle, skeleton1, skeleton2


def test_tiny_cycle():
    g, idxs, degimg = csr.skeleton_to_csgraph(tinycycle)
    expected_indptr = [0, 0, 2, 4, 6, 8]
    expected_indices = [2, 3, 1, 4, 1, 4, 2, 3]
    expected_data = np.sqrt(2)

    assert_equal(g.indptr, expected_indptr)
    assert_equal(g.indices, expected_indices)
    assert_almost_equal(g.data, expected_data)

    expected_degrees = np.array([[0, 2, 0], [2, 0, 2], [0, 2, 0]])
    assert_equal(degimg, expected_degrees)
    assert_equal(idxs, [0, 1, 3, 5, 7])


def test_skeleton1_stats():
    args = csr.skeleton_to_csgraph(skeleton1)
    stats = csr.branch_statistics(*args)
    assert_equal(stats.shape, (4, 4))
    keys = map(tuple, stats[:, :2].astype(int))
    dists = stats[:, 2]
    types = stats[:, 3].astype(int)
    ids2dist = dict(zip(keys, dists))
    assert (13, 8) in ids2dist
    assert (8, 13) in ids2dist
    d0, d1 = sorted((ids2dist[(13, 8)], ids2dist[(8, 13)]))
    assert_almost_equal(d0, 1 + np.sqrt(2))
    assert_almost_equal(d1, 5*d0)
    assert_equal(np.bincount(types), [0, 2, 2])
    assert_almost_equal(np.unique(dists), [d0, 2 + np.sqrt(2), d1])


def test_3skeletons():
    df = csr.summarise(skeleton2)
    assert_almost_equal(np.unique(df['euclidean-distance']),
                        np.sqrt([5, 10]))
    assert_equal(np.unique(df['skeleton-id']), [1, 2])
    assert_equal(np.bincount(df['branch-type']), [0, 4, 4])
