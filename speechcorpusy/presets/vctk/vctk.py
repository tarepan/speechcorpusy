"""VCTK corpus handler"""


from pathlib import Path

from speechcorpusy.interface import AbstractCorpus, ConfCorpus, ItemId
from speechcorpusy.helper.adress import get_adress
from speechcorpusy.helper.contents import get_contents
from speechcorpusy.helper.forward import forward
from speechcorpusy.components.taudio import extract_archive
from .missings import MISSINGS_MIC2


# VCTK: 'English Multi-speaker Corpus for CSTR Voice Cloning Toolkit'
# 108 en speakers (Total 109+1 speakers - mic2-missing 2 speakers)
# https://doi.org/10.7488/ds/2645
#
# Directory structure:
# ```
# wav48_silence_trimmed/
#     p225/
#         p225_001_mic1.flac
#         p225_001_mic2.flac
#         p225_001_mic1.flac
#         ...
#         p225_366.mic2.flac
#     p226/
#         ...
# txt/
# ```


# 109 speakers
SPKS_MIC2: list[str] = [
                                            'p225', 'p226', 'p227', 'p228', 'p229',
    'p230', 'p231', 'p232', 'p233', 'p234',         'p236', 'p237', 'p238', 'p239',
    'p240', 'p241',         'p243', 'p244', 'p245', 'p246', 'p247', 'p248', 'p249',
    'p250', 'p251', 'p252', 'p253', 'p254', 'p255', 'p256', 'p257', 'p258', 'p259',
    'p260', 'p261', 'p262', 'p263', 'p264', 'p265', 'p266', 'p267', 'p268', 'p269',
    'p270', 'p271', 'p272', 'p273', 'p274', 'p275', 'p276', 'p277', 'p278', 'p279',
            'p281', 'p282', 'p283', 'p284', 'p285', 'p286', 'p287', 'p288',
                    'p292', 'p293', 'p294', 'p295',         'p297', 'p298', 'p299',
    'p300', 'p301', 'p302', 'p303', 'p304', 'p305', 'p306', 'p307', 'p308',
    'p310', 'p311', 'p312', 'p313', 'p314',         'p316', 'p317', 'p318',
                            'p323',                 'p326',                 'p329',
    'p330',                 'p333', 'p334', 'p335', 'p336',                 'p339',
    'p340', 'p341',         'p343',         'p345',         'p347',
    'p351',
    'p360', 'p361', 'p362', 'p363', 'p364',
                                    'p374',         'p376',
    's5',
]

# Maximum utterance serial number of each speaker
MAX_UTTR_MIC2: list[int] = [
                                              366,    370,    402,    371,    392,
      417,    476,    415,    392,    361,            503,    351,    460,    503,
      380,    374,            398,    424,    359,    361,    479,    376,    354,
      496,    374,    411,    410,    403,    381,    320,    434,    414,    481,
      357,    474,    394,    473,    495,    352,    424,    421,    411,    403,
      462,    454,    412,    436,    470,    429,    465,    463,    410,    406,
              460,    370,    471,    425,    403,    468,    424,    412,
                      424,    400,    424,    424,            424,    405,    405,
      400,    411,    316,    353,    424,    422,    360,    424,    423,
      424,    423,    419,    423,    423,            423,    423,    424,
                              423,                    400,                    424,
      423,                    424,    424,    423,    424,                    424,
      424,    410,            400,            400,            424,
      424,
      424,    424,    418,    423,    309,
                                      424,            424,
      400,
]


class VCTK(AbstractCorpus):
    """Archive/contents handler of VCTK corpus.

    ItemID:
        corpus:    {self.__class__.__name__}
        subcorpus: mic2
        speaker:   vctk_{p|s}{N}
        name:      {N.zfill(3)}
    """

    # Version and so on
    _variant: str = "ds2019"
    # Archive file base name == 1st layer directory name of extracted archive
    _archive_name: str = "DS_10283_3443.zip"
    _adress_origin: str = "https://datashare.ed.ac.uk/download/DS_10283_3443.zip"
    _inner_archive_name: str = "VCTK-Corpus-0.92.zip"

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
        # Extraction of zip in zip
        if not (self._path_contents / "wav48_silence_trimmed").exists():
            print("Extracting #2 ...")
            extract_archive(str(self._path_contents / self._inner_archive_name), self._path_contents)
            print("Finally extracted.")

    def get_identities(self) -> list[ItemId]:
        """Get corpus item identities.

        Returns:
            Full item identity list.
        """

        ids: list[ItemId] = []

        for spk, num_max, spk_missings in zip(SPKS_MIC2, MAX_UTTR_MIC2, MISSINGS_MIC2):
            for serial in range(1, num_max+1):
                if serial not in spk_missings:
                    ids.append(ItemId(self.__class__.__name__, "mic2", f"vctk_{spk}", str(serial).zfill(3)))

        return ids

    def get_item_path(self, item_id: ItemId) -> Path:
        """Get path of the item.

        Args:
            item_id: Identity of target item.
        Returns:
            Path of the target item.
        """
        return self._path_contents / "wav48_silence_trimmed" / item_id.speaker[5:] / f"{item_id.speaker[5:]}_{item_id.name}_mic2.flac"
