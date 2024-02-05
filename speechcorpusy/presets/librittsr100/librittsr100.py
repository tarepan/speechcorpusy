"""JVS corpus handler"""

from pathlib import Path

from speechcorpusy.interface import AbstractCorpus, ItemId, ConfCorpus
from speechcorpusy.helper.adress import get_adress
from speechcorpusy.helper.contents import get_contents
from speechcorpusy.helper.forward import forward
from speechcorpusy.presets.librittsr100.items import items


# LiTTSR100: 'LibriTTS-R train-clean-100 corpus'
#
# Directory structure:
# ```
# NN/
#     MMMMMM/
#         NN_MMMMMM_AAAAAA_BBBBBB.wav
# ...
# NNNN/
# ```


subtypes = ["clean100"]

class LiTTSR100(AbstractCorpus):
    """Archive/contents handler of LibriTTS-R train-clean-100 corpus.

    ItemID:
        corpus:    {self.__class__.__name__}
        subcorpus: default
        speaker:   zundamon
        name:      NNNN
    """

    _variant: str = "ver1_0_0" # Version and so on
    _archive_name: str = "train_clean_100.tar.gz"
    _adress_origin: str = "https://www.openslr.org/resources/141/train_clean_100.tar.gz"

    def __init__(self, conf: ConfCorpus, variant: str | None = None) -> None:
        """Initialization without corpus contents acquisition.
        """

        super().__init__(conf)
        self.conf = conf
        variant = variant or self._variant
        self._adress_archive, self._path_contents = get_adress(conf.root, self.__class__.__name__, variant, self._archive_name)

    def get_contents(self) -> None:
        """Get corpus contents into local.
        """

        get_contents(
            self._adress_archive, self._path_contents, self.conf.download,
            lambda: forward(self._adress_origin, self._adress_archive),
        )

    def get_identities(self) -> list[ItemId]:
        """Get corpus item identities.

        Returns:
            Full item identity list.
        """
        #                                                                                      spk                     cptr      name1     name2
        return list(map(lambda item: ItemId(self.__class__.__name__, "clean100", f"LiTTSR{str(item[0]).zfill(4)}", f"{item[1]}_{item[2]}_{item[3]}"), items))

    def get_item_path(self, item_id: ItemId) -> Path:
        """Get path of the item.

        Args:
            item_id: Identity of target item.
        Returns:
            Path of the target item.
        """

        spk = int(item_id.speaker[-4:])
        cptr, name1, name2 = item_id.name.split("_")
        f_name = f"{spk}_{cptr}_{name1.zfill(6)}_{name2.zfill(6)}.wav"

        return self._path_contents / "LibriTTS_R" / "train-clean-100" / str(spk) / str(cptr) / f_name
