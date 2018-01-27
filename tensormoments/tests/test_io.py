import os
import pytest
from tensormoments import io


@pytest.fixture(scope="module")
def this_dir():
    return os.path.dirname(os.path.realpath(__file__))


def test_readElkOutput(this_dir):
    filename = os.path.join(this_dir, 'test_data/test_1_small.txt')
    d = io.readElkOutput(filename)
    assert len(d['value']) == 16


def test_readVaspOutput(this_dir):
    filename = os.path.join(this_dir, "test_data/TENSMOM.R1.OUT.small")
    df = io.readVaspOutput(filename, return_dataframe=True)

    assert len(df) == 36
    assert set(df.columns) == {"atom", "k", "l1", "l2", "nu", "p", "r", "species", "t", "value"}
    assert df.atom.unique() == [1]
    assert df.nu.unique() == [0]
    assert df.l1.unique() == [0]
    assert set(df.l2.unique()) == {0, 1, 2}
    assert len(df[df.k == 2]) == 20
    assert len(df[(df.k == 2) & (df.r == 3)]) == 7