"""LJ corpus handler"""


from typing import List
from pathlib import Path

from speechcorpusy.interface import AbstractCorpus, ConfCorpus, ItemId
from speechcorpusy.helper.adress import get_adress
from speechcorpusy.helper.contents import get_contents
from speechcorpusy.helper.forward import forward


# JSUT: 'Japanese speech corpus of Saruwatari-lab., University of Tokyo'
# single ja female speaker


class JSUT(AbstractCorpus):
    """Archive/contents handler of JSUT corpus.

    ItemID:
        subcorpus: "basic5000"
        speaker: "default"
        name: f"BASIC5000_{N.zfill(4)}"
    """

    _corpus_name: str = "JSUT"
    # Version and so on
    _variant: str = "ver1_1"
    # Archive file base name == 1st layer directory name of extracted archive
    _archive_base: str = "jsut_ver1.1"
    _archive_name: str = "jsut_ver1.1.zip"
    _adress_origin: str = "http://ss-takashi.sakura.ne.jp/corpus/jsut_ver1.1.zip"

    def __init__(self, conf: ConfCorpus) -> None:
        """Initialization without corpus contents acquisition.
        """

        super().__init__(conf)
        self.conf = conf
        self._adress_archive, self._path_contents = get_adress(
            conf.root,
            self._corpus_name,
            self._variant,
            self._archive_name,
        )

    def get_contents(self) -> None:
        """Get corpus contents into local.
        """

        get_contents(
            self._adress_archive,
            self._path_contents,
            self.conf.download,
            lambda: forward(self._adress_origin, self._adress_archive),
        )

    def get_identities(self) -> List[ItemId]:
        """Get corpus item identities.

        Returns:
            Full item identity list.
        """

        return [
            ItemId("basic5000", "default", f"BASIC5000_{str(i).zfill(4)}")
            for i in range(1, 5001)
        ]

    def get_item_path(self, item_id: ItemId) -> Path:
        """Get path of the item.

        Args:
            item_id: Identity of target item.
        Returns:
            Path of the target item.
        """
        root = self._path_contents / self._archive_base
        return root / item_id.subtype / "wav" / f"{item_id.name}.wav"
