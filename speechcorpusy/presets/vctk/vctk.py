"""LJ corpus handler"""


from typing import List, Tuple
from pathlib import Path

from speechcorpusy.interface import AbstractCorpus, ConfCorpus, ItemId
from speechcorpusy.helper.adress import get_adress
from speechcorpusy.helper.contents import get_contents
from speechcorpusy.helper.forward import forward

from .missings import MISSINGS

# VCTK: 'English Multi-speaker Corpus for CSTR Voice Cloning Toolkit'
# 109 en speakers
# https://doi.org/10.7488/ds/2645
#
# Directory structure:
# ```
# wav48/
#     p225/
#         p225_001.wav
#         ...
#         p225_366.awv
#     p226/
#         ...
# txt/
# ```


# 109 speakers
SPKS: List[str] = [
    'p225', 'p226', 'p227', 'p228', 'p229',
    'p230', 'p231', 'p232', 'p233', 'p234',         'p236', 'p237', 'p238', 'p239',
    'p240', 'p241',         'p243', 'p244', 'p245', 'p246', 'p247', 'p248', 'p249',
    'p250', 'p251', 'p252', 'p253', 'p254', 'p255', 'p256', 'p257', 'p258', 'p259',
    'p260', 'p261', 'p262', 'p263', 'p264', 'p265', 'p266', 'p267', 'p268', 'p269',
    'p270', 'p271', 'p272', 'p273', 'p274', 'p275', 'p276', 'p277', 'p278', 'p279',
    'p280', 'p281', 'p282', 'p283', 'p284', 'p285', 'p286', 'p287', 'p288',
                    'p292', 'p293', 'p294', 'p295',         'p297', 'p298', 'p299',
    'p300', 'p301', 'p302', 'p303', 'p304', 'p305', 'p306', 'p307', 'p308',
    'p310', 'p311', 'p312', 'p313', 'p314', 'p315', 'p316', 'p317', 'p318',
                            'p323',                 'p326',                 'p329',
    'p330',                 'p333', 'p334', 'p335', 'p336',                 'p339',
    'p340', 'p341',         'p343',         'p345',         'p347',
    'p351',
    'p360', 'p361', 'p362', 'p363', 'p364',
                                    'p374',         'p376'
]

# Maximum utterance serial number of each speaker
MAX_UTTR: List[int] = [
    366, 370, 402, 371, 392, 417, 476, 415, 392, 361, 503, 351, 460, 503, 380, 374,
    398, 424, 359, 361, 479, 376, 354, 496, 374, 411, 410, 403, 381, 320, 434, 414,
    481, 357, 474, 394, 473, 495, 352, 424, 421, 411, 403, 462, 454, 412, 436, 470,
    429, 465, 463, 410, 406, 410, 460, 370, 471, 425, 403, 468, 424, 412, 424, 400,
    424, 424, 424, 405, 405, 400, 411, 316, 353, 424, 423, 360, 424, 423, 424, 423,
    419, 423, 423, 421, 423, 424, 424, 424, 400, 424, 424, 424, 424, 424, 424, 424,
    424, 410, 400, 400, 424, 424, 424, 424, 424, 423, 309, 424, 295
]

# Broken utterances (0sec silence)
BROKENS: List[Tuple[str, int]] = [
    ("p295", 47), ("p345", 387), ("p317", 424), ("p305", 423)
]


class VCTK(AbstractCorpus):
    """Archive/contents handler of VCTK corpus.

    ItemID:
        subcorpus: "wav"
        speaker: f"vctk_p{N.zfill(3)}"
        name: f"{N.zfill(3)}"
    """

    _corpus_name: str = "VCTK"
    # Version and so on
    _variant: str = "ver0_92"
    # Archive file base name == 1st layer directory name of extracted archive
    _archive_base: str = "VCTK-Corpus"
    _archive_name: str = "VCTK-Corpus.tar.gz"
    _adress_origin: str = "http://www.udialogue.org/download/VCTK-Corpus.tar.gz"

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

        ids: List[ItemId] = []

        for spk, num_max, spk_missings in zip(SPKS, MAX_UTTR, MISSINGS):
            for serial in range(1, num_max+1):
                #       missing utterances               broken utterances
                if (serial not in spk_missings) and ((spk, serial) not in BROKENS):
                    ids.append(ItemId("wav", f"vctk_{spk}", str(serial).zfill(3)))

        return ids

    def get_item_path(self, item_id: ItemId) -> Path:
        """Get path of the item.

        Args:
            item_id: Identity of target item.
        Returns:
            Path of the target item.
        """
        root = self._path_contents / self._archive_base
        return root / "wav48" / item_id.speaker[5:] / f"{item_id.speaker[5:]}_{item_id.name}.wav"
