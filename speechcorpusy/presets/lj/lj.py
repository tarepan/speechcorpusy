"""LJ corpus handler"""


from typing import List
from pathlib import Path

from speechcorpusy.interface import AbstractCorpus, ConfCorpus, ItemId
from speechcorpusy.helper.adress import get_adress
from speechcorpusy.helper.contents import get_contents
from speechcorpusy.helper.forward import forward


# LJ: 'LJSpeech corpus'
# single en female speaker
#
# Directory structure:
# ```
# wavs/
#     LJ001-0001.wav
#     ...
#     LJ050-0278.awv
# ```


class LJ(AbstractCorpus):
    """Archive/contents handler of LJSpeech corpus.

    ItemID:
        subcorpus: "default"
        speaker: "lj_default"
        name: f"LJ{N.zfill(3)}-{N.zfill(4)}"
    """

    # Version and so on
    _variant: str = "ver1_1"
    # Archive file base name == 1st layer directory name of extracted archive
    _archive_base: str = "LJSpeech-1.1"
    _archive_name: str = "LJSpeech-1.1.tar.bz2"
    _adress_origin: str = "https://data.keithito.com/data/speech/LJSpeech-1.1.tar.bz2"

    def __init__(self, conf: ConfCorpus) -> None:
        """Initialization without corpus contents acquisition.
        """

        super().__init__(conf)
        self.conf = conf
        self._adress_archive, self._path_contents = get_adress(
            conf.root,
            self.__class__.__name__,
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

        # Maximum serial number of each groups
        maxes: List[int] = [186, 338, 349, 250, 300, 308, 243, 319, 304, 317, 293,
             296, 268, 340, 314, 446, 284, 398, 399, 108, 210, 203, 141, 143, 176,
             166, 180, 519, 213, 255, 233, 275, 214, 219, 210, 218, 269, 306, 248,
             240, 203, 251, 188, 239, 250, 254, 250, 289, 230, 278]
        group_info = {i+1: list(range(1, num+1)) for i, num in enumerate(maxes)}

        # patch: Missing utterances
        # [index, missings]
        missings = [(2, [115]), (3, [272]), (4, [53]), (5, [81]), (6, [37]), (8, [179]),
        (14, [145, 270, 284, 319]), (16, [83, 269, 270, 345, 372, 437]), (17, [275, 279]),
        (21, [13]), (27, [140]), (28, [135]), (34, [139]), (38, [195, 196]),
        (42, [34, 243]), (44, [46, 216]), (48, [108]), (49, [131])]
        for msg in missings:
            group_info[msg[0]] = list(filter(lambda i: i not in msg[1], group_info[msg[0]]))


        ids: List[ItemId] = []
        for group in range(1,51):
            for num in group_info[group]:
                name = f"LJ{str(group).zfill(3)}-{str(num).zfill(4)}"
                ids.append(ItemId("default", "lj_default", name))
        return ids

    def get_item_path(self, item_id: ItemId) -> Path:
        """Get path of the item.

        Args:
            item_id: Identity of target item.
        Returns:
            Path of the target item.
        """
        root = self._path_contents / self._archive_base
        return root / "wavs" / f"{item_id.name}.wav"
