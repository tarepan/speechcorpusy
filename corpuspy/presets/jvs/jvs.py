"""JVS corpus handler"""

from typing import List, Tuple
from pathlib import Path

from corpuspy.interface import AbstractCorpus, ItemId, ConfCorpus
from corpuspy.helper.adress import get_adress
from corpuspy.helper.contents import get_contents
from corpuspy.helper.forward import forward_from_gdrive


# JVS: 'Japanese versatile speech corpus'
#
# Directory structure:
# ```
# jvs001/
#     parallel100/
#         wav24kHz16bit/
#             VOICEACTRESS100_001.wav
#             ...
#             VOICEACTRESS100_100.wav
#     nonpara30/
#     falset10/
#     whisper10/
# ...
# jvs100/
# ```


subtypes = ["parallel100"]

class JVS(AbstractCorpus):
    """Archive/contents handler of JVS corpus.
    """

    _corpus_name: str = "JVS"
    # Version and so on
    _variant: str = "ver1_0_0"
    # Archive file base name == 1st layer directory name of extracted archive
    _archive_base: str = "jvs_ver1"
    _archive_name: str = "jvs_ver1.zip"
    # Google Drive item ID
    _origin_content_id: str = "19oAw8wWn3Y7z6CKChRdAyGOB9yupL_Xt"

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
            lambda: forward_from_gdrive(self._origin_content_id, self._adress_archive, 3.29),
        )

    def get_identities(self) -> List[ItemId]:
        """Get corpus item identities.

        Currently only 'parallel100' is provided.
        Returns:
            Full item identity list.
        """

        # Items which should be excluded. (spk, name)
        excluded: List[Tuple[int, int]] = [
            ("30", "45"), ("74", "94"), ("89", "19"), # Missing
            ("9", "95"), # 0sec length
            ("98", "60"), ("98", "99"), # contain cough
        ]
        candidates: List[ItemId] = [
            ItemId("parallel100", str(spk), str(utt))
            for utt in range(1, 101)
            for spk in range(1, 101)
        ]
        # Remove `excluded` from `candidates`
        ids = list(filter(lambda candidate: all([
            not (candidate.speaker == rm[0] and candidate.name == rm[1]) for rm in excluded
        ]), candidates))
        return ids

    def get_item_path(self, item_id: ItemId) -> Path:
        """Get path of the item.

        Args:
            item_id: Identity of target item.
        Returns:
            Path of the target item.
        """
        root = self._path_contents / self._archive_base
        spk_dir = f"jvs{item_id.speaker.zfill(3)}"
        f_name = f"VOICEACTRESS100_{item_id.name.zfill(3)}.wav"
        return root / spk_dir / "parallel100" / "wav24kHz16bit" / f_name
