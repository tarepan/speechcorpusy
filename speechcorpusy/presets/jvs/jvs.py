"""JVS corpus handler"""

from typing import List, Tuple
from pathlib import Path

from speechcorpusy.interface import AbstractCorpus, ItemId, ConfCorpus
from speechcorpusy.helper.adress import get_adress
from speechcorpusy.helper.contents import get_contents
from speechcorpusy.helper.forward import forward_from_gdrive


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

    # Version and so on
    _variant: str = "ver1_0_0"
    # Archive file base name == 1st layer directory name of extracted archive
    _archive_base: str = "jvs_ver1"
    _archive_name: str = "jvs_ver1.zip"
    # Google Drive item ID
    _origin_content_id: str = "19oAw8wWn3Y7z6CKChRdAyGOB9yupL_Xt"

    def __init__(self, conf: ConfCorpus, variant: str | None = None) -> None:
        """Initialization without corpus contents acquisition.
        """

        super().__init__(conf)
        variant = variant or self._variant
        self.conf = conf
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
            ("jvs030", "45"), ("jvs074", "94"), ("jvs089", "19"), # Missing
            ("jvs009", "95"), # 0sec length
            ("jvs098", "60"), ("jvs098", "99"), # contain cough
        ]
        candidates: List[ItemId] = [
            ItemId(self.__class__.__name__, "parallel100", f"jvs{str(spk).zfill(3)}", str(utt))
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
        f_name = f"VOICEACTRESS100_{item_id.name.zfill(3)}.wav"
        return root / item_id.speaker / "parallel100" / "wav24kHz16bit" / f_name
