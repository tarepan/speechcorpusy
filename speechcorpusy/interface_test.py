"""Test interface methods."""

import pytest

from .loader import load_preset
from .interface import ItemId


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


def test_merge():
    """Test corpus merge."""

    # items: ["sub1", "sub2"] x ["spk1", "spk2"] x ["uttr1", "uttr2"]
    corpus_a = load_preset("TEST").switch_version("A")
    corpus_b = load_preset("TEST").switch_version("B")
    corpus_c = load_preset("TESTbeta").switch_version("C")
    corpuses = [corpus_a, corpus_b, corpus_c]
    merged_corpus = sum(corpuses[1:], corpuses[0])

    item_ids = merged_corpus.get_identities()
    assert len(item_ids) == 3*8

    # Failed if the corresponding corpus does not exist
    list(map(merged_corpus.get_item_path, item_ids))

    assert merged_corpus.get_item_path(ItemId("TEST", "sub1A", "spk1A", "spk1A")) is not None
    with pytest.raises(RuntimeError) as err:
        merged_corpus.get_item_path(ItemId("TESTZ", "sub1A", "spk1A", "spk1A"))
    assert str(err.value) == "Corresponding corpus is not found, TESTZ not in ['TEST', 'TEST', 'TESTbeta']"

    item_ids_per_spk = merged_corpus.get_identities_per_speaker()
    assert len(item_ids_per_spk) == 6
    for item_ids_spk in item_ids_per_spk:
        assert len(item_ids_spk) == 4
