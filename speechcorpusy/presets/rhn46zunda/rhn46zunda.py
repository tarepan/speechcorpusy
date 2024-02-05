"""RHN46ZND corpus handler"""


from typing import List
from pathlib import Path

from speechcorpusy.interface import AbstractCorpus, ConfCorpus, ItemId
from speechcorpusy.helper.adress import get_adress
from speechcorpusy.helper.contents import get_contents
from speechcorpusy.helper.forward import forward


# RHN46ZND: 'ROHAN4600 corpus by ずんだもん (CV：伊藤ゆいな)'
#
# Directory structure:
# ```
# ROHAN4600_zundamon_voice/
#     ROHAN4600_0001.wav
#     ...
#     ROHAN4600_4600.wav
# ```


class RHN46ZND(AbstractCorpus):
    """Archive/contents handler of RHN46ZND corpus.

    ItemID:
        corpus:    {self.__class__.__name__}
        subcorpus: default
        speaker:   zundamon
        name:      NNNN
    """

    # Version and so on
    _variant: str = "ver1_0_0"
    _archive_name: str = "ROHAN4600_zundamon_voice.zip"
    _adress_origin: str = "<You need individual agreement for download (don't worry, it is no fee)"

    def __init__(self, conf: ConfCorpus, variant: str | None = None) -> None:
        """Initialization without corpus contents acquisition.
        """

        super().__init__(conf)
        self.conf = conf
        variant = variant or self._variant
        self._adress_archive, self._path_contents = get_adress(
            conf.root,
            self.__class__.__name__,
            variant,
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

        return [ItemId(self.__class__.__name__, "default", "zundamon", str(i).zfill(4)) for i in range(1, 4601)]

    def get_item_path(self, item_id: ItemId) -> Path:
        """Get path of the item.

        Args:
            item_id: Identity of target item.
        Returns:
            Path of the target item.
        """
        root = self._path_contents
        return root / "ROHAN4600_zundamon_voice" / f"ROHAN4600_{item_id.name}.wav"
