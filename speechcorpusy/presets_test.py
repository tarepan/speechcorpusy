"""Test Preset testing"""

import librosa

from .loader import load_preset


def test_TEST_preset(): # pylint: disable=invalid-name
    """Test 'TEST' preset."""

    test_corpus = load_preset("TEST")
    ids = test_corpus.get_identities()

    # The number of ids
    assert len(ids) == 8

    # Data access
    wave = librosa.load(test_corpus.get_item_path(ids[0]), sr=None)
    assert len(wave) > 0
