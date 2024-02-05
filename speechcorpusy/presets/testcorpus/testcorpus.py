"""TEST corpus handler"""


from __future__ import annotations
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

    def __init__(self, conf: ConfCorpus, variant: str | None = None) -> None:
        """Initialization without corpus contents acquisition.
        """

        super().__init__(conf)

        # Special import (you need manual install)
        from librosa.util import example # pyright: ignore [reportMissingImports] ; pylint: disable=import-outside-toplevel, import-error, no-name-in-module
        self._path_wav = Path(example("libri2"))

        # Hack for test
        self._ver = ""

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
            for subcorpus in [f"sub1{self._ver}", f"sub2{self._ver}"]
            for speaker in [f"spk1{self._ver}", f"spk2{self._ver}"]
            for name in [f"uttr1{self._ver}", f"uttr2{self._ver}"]
        ]

    def get_item_path(self, _: ItemId) -> Path:
        """Get path of the item.

        Args:
            _: Identity of target item.
        Returns:
            Path of the target item.
        """
        return self._path_wav

    def switch_version(self, ver: str) -> TEST:
        """Switch corpus item version for test/debug."""
        self._ver = ver
        return self


class TESTbeta(AbstractCorpus):
    """Archive/contents handler of TESTbeta corpus.

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

        # Hack for test
        self._ver = ""

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
            for subcorpus in [f"subb1{self._ver}", f"subb2{self._ver}"]
            for speaker in [f"spkb1{self._ver}", f"spkb2{self._ver}"]
            for name in [f"uttrb1{self._ver}", f"uttrb2{self._ver}"]
        ]

    def get_item_path(self, _: ItemId) -> Path:
        """Get path of the item.

        Args:
            _: Identity of target item.
        Returns:
            Path of the target item.
        """
        return self._path_wav

    def switch_version(self, ver: str) -> TEST:
        """Switch corpus item version for test/debug."""
        self._ver = ver
        return self
