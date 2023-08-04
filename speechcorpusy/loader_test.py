"""Test loader."""

from .loader import load_preset


def test_load_merged_2preset():
    """Test corpus merge in `load_preset`."""

    corpus = load_preset("TEST&TESTbeta", "./", False)

    assert len(corpus.get_identities()) == 2*8


def test_load_merged_3preset():
    """Test corpus merge in `load_preset`."""

    corpus = load_preset("TEST&TESTbeta&TEST", "./", False)

    assert len(corpus.get_identities()) == 3*8
