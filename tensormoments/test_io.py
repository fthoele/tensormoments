import pytest
from . import io

@pytest.fixture(scope="module")
def needsIo():
    import os
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

def test_readElkOutput(needsIo):
    filename = 'testData/test_1_small.txt'
    d = io.readElkOutput(filename)
    assert len(d['value']) == 16