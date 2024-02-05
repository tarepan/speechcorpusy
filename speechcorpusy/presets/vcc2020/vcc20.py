"""VCC2020 corpus handler"""


from typing import List
from pathlib import Path
import zipfile

from speechcorpusy.interface import AbstractCorpus, ConfCorpus, ItemId
from speechcorpusy.helper.adress import get_adress
from speechcorpusy.helper.contents import get_contents
from speechcorpusy.helper.forward import forward

from .ids import item_ids


# VCC2020: 'Voice Conversion Challenge 2020'
# 8 en speakers (4male/4female), 2 Finnish/German/Mandarin speakers (2male/2female).
# https://github.com/nii-yamagishilab/VCC2020-database
#
# Directory structure:
# ```
# /
#     vcc2020_database_training_source.zip => source/
#         SE{F|M}{1|2}/
#             E10001.wav
#             ...
#             E10070.wav
#     vcc2020_database_training_target_task1.zip => target_task1/
#         TE{F|M}{1|2}/
#             E10051.wav
#             E10070.wav
#             E20001.wav
#             E20050.wav
#     vcc2020_database_training_target_task2.zip => target_task2/
#         T{F|G|M}{F|M}1/
#             {F|G|M}10001.wav
#             ...
#             {F|G|M}10070.wav
#     vcc2020_database_evaluation.zip => vcc2020_database_evaluation/
#         SE{F|M}{1|2}/
#             E30001.wav
#             ...
#             E30025.wav
#     vcc2020_database_groundtruth.zip => vcc2020_database_groundtruth/
#         TE{F|M}{1|2}/
#             E30001.wav
#             ...
#             E30025.wav
#         T{F|G|M}{F|M}1/
#             {F|G|M}30001.wav
#             ...
#             {F|G|M}30025.wav
# ```


# In VCC2020 challenge, trains a model with "train_..." data,
# submit converted (from "eval_source" to all target speakers) utterances.
# Ground truth has same ligual contents with "eval_source" and speaker identity is the targets.
SUBCORPUSES = [
    "train_source", "train_target_task1", "train_target_task2",
    "eval_source", "groundtruth"
]
SUBCORPUSES_ZIP = [
    "vcc2020_database_training_source.zip",
    "vcc2020_database_training_target_task1.zip",
    "vcc2020_database_training_target_task2.zip",
    "vcc2020_database_evaluation.zip",
    "vcc2020_database_groundtruth.zip",
]
SUBCORPUSES_DIR = {
    "train_source": "source",
    "train_target_task1": "target_task1",
    "train_target_task2": "target_task2",
    "eval_source": "vcc2020_database_evaluation",
    "groundtruth": "vcc2020_database_groundtruth",
}


LANGS = [
    "E", # English
    "F", # Finnish
    "G", # German
    "M", # Mandarin
]
_URL = "https://github.com/nii-yamagishilab/VCC2020-database/archive/refs/tags/v1.0.0.tar.gz"

class VCC20(AbstractCorpus):
    """Archive/contents handler of Voice Conversion Challenge 2020 corpus.

    ItemID:
        corpus:    {self.__class__.__name__}
        subcorpus: SUBCORPUSES
        speaker:   {"S"/source | "T"/target}{LANGS}{"M"/male | "F"/female}{1|2}
        name:      {LANGS}{N.zfill(5)}
    """

    # Version and so on
    _variant: str = "ver1_0_0"
    # Archive file base name == 1st layer directory name of extracted archive
    _archive_base: str = "VCC2020-database-1.0.0"
    _archive_name: str = "VCC2020-database-1.0.0.tar.gz"
    _adress_origin: str = _URL

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
        root = self._path_contents / self._archive_base
        # Only when there are only zip files, extract them.
        if all(map(lambda child: child.is_file(), root.iterdir())):
            for zip_name in SUBCORPUSES_ZIP:
                with zipfile.ZipFile(root / zip_name) as zip_f:
                    zip_f.extractall(root)

    def get_identities(self) -> List[ItemId]:
        """Get corpus item identities.

        Returns:
            Full item identity list.
        """
        return item_ids

    def get_item_path(self, item_id: ItemId) -> Path:
        """Get path of the item.

        Args:
            item_id: Identity of target item.
        Returns:
            Path of the target item.
        """

        root = self._path_contents / self._archive_base
        return root / SUBCORPUSES_DIR[item_id.subtype] / item_id.speaker[6:] / f"{item_id.name}.wav"
