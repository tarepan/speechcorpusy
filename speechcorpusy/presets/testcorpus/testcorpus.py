"""TEST corpus handler"""


from typing import List
from pathlib import Path

from speechcorpusy.interface import AbstractCorpus, ConfCorpus, ItemId


# TEST: 'test corpus'

class TEST(AbstractCorpus):
    """Archive/contents handler of TEST corpus.

    For usage, you have to install `librosa` manually (not automatically installed by this package)

    ItemID:
        corpus:    {self.__class__.__name__}
        subcorpus: sub1 | sub2
        speaker:   spk1 | spk2
        name:      uttr1 | uttr2
    """

    # Version and so on
    _variant: str = "ver0_0_0"
    _archive_name: str = "<place-holder>"
    _adress_origin: str = "<place-holder>"

    def __init__(self, conf: ConfCorpus) -> None:
        """Initialization without corpus contents acquisition.
        """

        super().__init__(conf)

        # Special import (you need manual install)
        from librosa.util import example # pyright: ignore [reportMissingImports] ; pylint: disable=import-outside-toplevel, import-error, no-name-in-module
        self._path_wav = Path(example("libri2"))

    def get_contents(self) -> None:
        """Get corpus contents into local.
        """

    def get_identities(self) -> List[ItemId]:
        """Get corpus item identities.

        Returns:
            Full item identity list.
        """

        return [
            ItemId(self.__class__.__name__, subcorpus, speaker, name)
            for subcorpus in ["sub1", "sub2"]
            for speaker in ["spk1", "spk2"]
            for name in ["uttr1", "uttr2"]
        ]

    def get_item_path(self, _: ItemId) -> Path:
        """Get path of the item.

        Args:
            _: Identity of target item.
        Returns:
            Path of the target item.
        """
        return self._path_wav
