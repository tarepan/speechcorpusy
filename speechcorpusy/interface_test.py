"""Test interface methods."""

from .loader import load_preset


def test_get_identities_per_speaker(): # pylint: disable=invalid-name
    """Test 'TEST' preset."""

    # items: for subcorpus in ["sub1", "sub2"] for speaker in ["spk1", "spk2"] for name in ["uttr1", "uttr2"]
    test_corpus = load_preset("TEST")

    ids_per_spks = test_corpus.get_identities_per_speaker()

    # The number of speakers
    assert len(ids_per_spks) == 2, "There should be 2 speakers."

    # The number of utterances spk#0
    assert len(ids_per_spks[0]) == 4, "There should be 4 utterances in speaker #0."

    # The number of utterances spk#1
    assert len(ids_per_spks[1]) == 4, "There should be 4 utterances in speaker #1."
