"""ZR19 corpus handler"""


from typing import List
from pathlib import Path

from speechcorpusy.interface import AbstractCorpus, ItemId, ConfCorpus
from speechcorpusy.helper.adress import get_adress, extract_name_and_variant
from speechcorpusy.helper.contents import get_contents
from speechcorpusy.helper.forward import forward

from .zr19_items_unit import utterances_unit
from .zr19_items_voice import utterances_voice


# ZR19: 'Zero Resource Speech Challenge 2019 corpus'
#
# This corpus contains 4x2 sub-corpuses.
# x2 are Development(en)/Surprise(id), 4 are below.
#
# |          name          |    directory      |                                                                              | # pylint: disable=line-too-long
# |:----------------------:|:-----------------:|:----------------------------------------------------------------------------:|
# | `Train Voice`          | `train/voice/`    | 2 spk (Development) / 1 spk (Surprise)                                       |
# | `Train Unit Discovery` | `train/unit/`     | 100 spk (Development), 112 spk (Surprise)                                    |
# | `Train Parallel`       | `train/parallel/` | parallel spoken utterances from the Target Voice and from other speakers     |
# | `Test`                 | `test/`           | Unseen (not in Train) utterances by unseen speakers (Dev 24 spk, Sur 15 spk) |
#
# Directory structure:
# ```
# train/
#     parallel/
#         source/
#             S000_0000000000.wav
#         voice/
#             V001_0000000000.wav
#             V002_0000000000.wav
#     unit/
#         S000_0000000000.wav
#     voice/
#         V001_0000000000.wav
#         V002_0000000000.wav
# test/
#     S000_0000000000.wav
# ```
#
# Speakers
#     spk_unit: List[str] = ["S015", "S020", "S021", "S023", "S027", "S031", "S032", "S033",
#         "S034", "S035", "S036", "S037", "S038", "S039", "S040", "S041", "S042", "S043",
#         "S044", "S045", "S046", "S047", "S048", "S049", "S050", "S051", "S052", "S053",
#         "S054", "S055", "S056", "S058", "S059", "S060", "S061", "S063", "S064", "S065",
#         "S066", "S067", "S069", "S070", "S071", "S072", "S073", "S074", "S075", "S076",
#         "S077", "S078", "S079", "S080", "S082", "S083", "S084", "S085", "S086", "S087",
#         "S088", "S090", "S091", "S092", "S093", "S094", "S095", "S096", "S097", "S098",
#         "S099", "S100", "S101", "S102", "S103", "S104", "S105", "S106", "S107", "S109",
#         "S110", "S111", "S112", "S113", "S114", "S115", "S116", "S117", "S118", "S119",
#         "S120", "S121", "S122", "S123", "S125", "S126", "S127", "S128", "S129", "S131",
#         "S132", "S133"]
#     spk_voice: List[str] = ["V001","V002"]
#     spk_para_src: List[str] = ?
#     spk_para_vic: List[str] = ["V001","V002"]
#     spk_test: List[str] = ?


subtypes = ["train-parallel-source", "train-parallel-voice", "train-unit", "train-voice", "test"]

class ZR19(AbstractCorpus):
    """Archive/contents handler of Zero Resource Speech Challenge 2019 corpus.
    """

    # Version and so on
    _variant: str = "ver1_0_0_english"
    # Archive file base name == 1st layer directory name of extracted archive
    _archive_base: str = "english"
    _archive_name: str = "english.tgz"
    _adress_origin: str = "https://download.zerospeech.com/2019/english.tgz"
    # !wget --no-check-certificate

    def __init__(self, conf: ConfCorpus) -> None:
        """Initialization without corpus contents acquisition.
        """

        super().__init__(conf)
        self.conf = conf
        _, variant = extract_name_and_variant(conf.name, self._variant)
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

        Currently, train/unit & train/voice are provided.
        Returns:
            Full item identity list.
        """

        # No pattern in file name, so need hard-coded file name list
        ids: List[ItemId] = []
        for item in utterances_unit:
            ids.append(ItemId("train-unit", f"zr19_{item[0:4]}", item))
        for item in utterances_voice:
            ids.append(ItemId("train-voice", f"zr19_{item[0:4]}", item))
        return ids

    def get_item_path(self, item_id: ItemId) -> Path:
        """Get path of the item.

        Args:
            item_id: Identity of target item.
        Returns:
            Path of the target item.
        """
        root = self._path_contents / self._archive_base
        sub_dirs = Path(item_id.subtype.replace('-', '/'))
        return root / sub_dirs / f"{item_id.name}.wav"
