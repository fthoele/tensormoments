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
