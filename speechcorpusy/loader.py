"""Corpus Loaders"""

from typing import Optional
from copy import deepcopy

from speechcorpusy.interface import AbstractCorpus, ConfCorpus
from speechcorpusy import presets


def load_preset(
    name: Optional[str] = None,
    root: Optional[str] = None,
    download: Optional[bool] = None,
    conf: Optional[ConfCorpus] = None,
    ) -> AbstractCorpus:
    """Load preset corpus.

    Args:
        name: Preset corpus name ('Preset1&Preset2&...' results in merged corpus)
        root: Adress of the directory under which the corpus archive is found or downloaded
        download: Whether to download original corpus if it is not found in `root`
        conf: (Advanced) Corpus configuration containing all other arguments
    """

    # Design Notes:
    #     ConfCorpus is verbose wrapper, but useful when used with config manager.
    #     For both purpose, we provide both way.
    #     As a result, loader become dirty, but it is good for user.

    # Check config inconsistency
    # Both `name` and `conf` are provided, but different value
    if name and conf and (name != conf.name):
        raise RuntimeError(f"'name' and 'conf.name' is inconsistent: {name} vs {conf.name}")
    # Both `root` and `conf` are provided, but different value
    if root and conf and (root != conf.root):
        raise RuntimeError(f"'root' and 'conf.root' is inconsistent: {root} vs {conf.root}")
    # Both `download` and `conf` are provided, but different value
    if (download is not None) and conf and (download != conf.download):
        raise RuntimeError(f"'download' and 'conf.download' is inconsistent: {download} vs {conf.download}")

    checked_conf = conf or ConfCorpus(name, root, download or False)

    corpuses: list[AbstractCorpus] = []
    for corpus_name in checked_conf.name.split("&"):
        # Unit (non-merged) corpus' config
        conf_i = deepcopy(checked_conf)
        conf_i.name = corpus_name

        # Load corpus safely
        if conf_i.name in presets.corpus_list:
            corpus_cls: AbstractCorpus = getattr(presets, conf_i.name)
            corpuses.append(corpus_cls(conf_i))
        else:
            raise RuntimeError(f"Corpus '{conf_i.name}' is not supported by 'speechcurpusy'. Supported presets: {presets.corpus_list}")

    if len(corpuses) == 1:
        return corpuses[0]
    else:
        return sum(corpuses[1:], corpuses[0])
