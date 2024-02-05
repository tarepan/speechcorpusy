"""Act100TKYM corpus handler"""


from typing import List
from pathlib import Path

from speechcorpusy.interface import AbstractCorpus, ConfCorpus, ItemId
from speechcorpusy.helper.adress import get_adress, extract_name_and_variant
from speechcorpusy.helper.contents import get_contents
from speechcorpusy.helper.forward import forward


# Act100TKYM: 'voiceactress100 (sub) corpus by つくよみちゃん/Tsukuyomi-chan'
#
# Directory structure:
# ```
# é┬é¡éµé▌é┐éßé±âRü[âpâX Vol.1 É║ùDô¥îvâRü[âpâXüiJVSâRü[âpâXÅÇïÆüj/
#     01 WAVüiÄ√ÿ^Ä₧é╠ë╣ù╩é╠é▄é▄üj/
#         VOICEACTRESS100_001.wav
#         ...
#         VOICEACTRESS100_100.wav
# ```


class Act100TKYM(AbstractCorpus):
    """Archive/contents handler of Act100TKYM corpus.

    ItemID:
        corpus:    {self.__class__.__name__}
        subcorpus: default
        speaker:   act100tkym
        name:      NNN
    """

    # Version and so on
    _variant: str = "ver1_0_0"
    _archive_name: str = "sozai-tyc-corpus1.zip"
    _adress_origin: str = "https://tyc.rei-yumesaki.net/files/sozai-tyc-corpus1.zip"

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

        Returns:
            Full item identity list.
        """

        return [ItemId(self.__class__.__name__, "default", "act100tkym", str(i).zfill(3)) for i in range(1, 101)]

    def get_item_path(self, item_id: ItemId) -> Path:
        """Get path of the item.

        Args:
            item_id: Identity of target item.
        Returns:
            Path of the target item.
        """
        root = self._path_contents
        d_1 = "é┬é¡éµé▌é┐éßé±âRü[âpâX Vol.1 É║ùDô¥îvâRü[âpâXüiJVSâRü[âpâXÅÇïÆüj"
        d_2 = "01 WAVüiÄ√ÿ^Ä₧é╠ë╣ù╩é╠é▄é▄üj"
        return root / d_1 / d_2 / f"VOICEACTRESS100_{item_id.name}.wav"
