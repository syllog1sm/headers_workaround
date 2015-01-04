from __future__ import unicode_literals

from os import path
import os
import shutil

import pytest
import headers_workaround


def dir_exists(directory):
    return path.exists(directory) and path.isdir(directory)

def file_exists(loc):
    return path.exists(loc) and not path.isdir(loc)


def local_path(filename):
    return path.join(path.dirname(__file__), filename)


@pytest.fixture
def headers_dir():
    directory =  local_path('headers_dir')
    if path.exists(directory):
        assert path.isdir(directory)
        shutil.rmtree(directory)
    os.mkdir(directory)
    return directory


def test_numpy(headers_dir):
    headers_workaround.install_headers('numpy', include_dir=headers_dir)
    assert dir_exists(headers_dir)
    assert dir_exists(path.join(headers_dir, 'numpy'))
    # Test some arbitrary files --- if any break, add them to the test later...
    assert file_exists(path.join(headers_dir, 'numpy', 'ndarrayobject.h'))
    assert file_exists(path.join(headers_dir, 'numpy', 'npy_endian.h'))
    assert file_exists(path.join(headers_dir, 'numpy', 'npy_math.h'))


def test_murmurhash(headers_dir):
    headers_workaround.install_headers('murmurhash', include_dir=headers_dir)
    assert dir_exists(headers_dir)
    assert dir_exists(path.join(headers_dir, 'murmurhash'))
    assert file_exists(path.join(headers_dir, 'murmurhash', 'MurmurHash2.h'))
    assert file_exists(path.join(headers_dir, 'murmurhash', 'MurmurHash3.h'))
