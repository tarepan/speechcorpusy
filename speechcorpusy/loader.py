"""Corpus Loaders"""

from speechcorpusy.interface import AbstractCorpus, ConfCorpus
from speechcorpusy import presets


def load_preset(name: str, conf: ConfCorpus) -> AbstractCorpus:
    """Load preset corpus.

    Args:
        name: Preset corpus name
        conf: Corpus configuration
    """

    if name in presets.corpus_list:
        corpus_cls = getattr(presets, name)
        corpus = corpus_cls(conf)
    else:
        msg1 = f"Corpus '{name}' is not supported by 'speechcurpusy'."
        msg2 = f"Supported presets: {presets.corpus_list}"
        raise Exception(msg1+msg2)

    return corpus
