"""LJ corpus handler"""


from typing import List
from pathlib import Path

from speechcorpusy.interface import AbstractCorpus, ConfCorpus, ItemId
from speechcorpusy.helper.adress import get_adress


# AdHoc: A local directory which is recognized as a corpus ad hoc.
# Data depends on your choice.


class AdHoc(AbstractCorpus):
    """Archive/contents handler of AdHoc corpus.

    AdHoc corpus is special 'ad hoc' corpus.
    Data comes from local data, not from remote 'origin' corpus.
    You should prepare data as specified below locally.
    This is ad hoc, so data will never be forwarded to anywhere.

    [Data structure]
    ./tmp/corpuses/AdHoc/default/contents/
        {subtype_1}/
            {speaker_1}/
                {utterance_1}.wav
                {utterance_2}.wav
                ...
            {speaker_2}/
                ...
        {subtype_2}/
        ...

    ItemID:
        subtype: f"{subtype_X_name}"
        speaker: f"{speaker_X_name}"
        name: f"{utterance_X_stem}"
    """

    _corpus_name: str = "AdHoc"
    # Version and so on
    _variant: str = "default"
    # Archive file base name == 1st layer directory name of extracted archive
    _archive_base: str = "not_exists"
    _archive_name: str = "not_exists.zip"
    _adress_origin: str = "not_exists"

    def __init__(self, conf: ConfCorpus) -> None:
        """Initialization without corpus contents acquisition.
        """

        super().__init__(conf)
        self.conf = conf
        _, self._path_contents = get_adress(
            conf.root,
            self._corpus_name,
            self._variant,
            self._archive_name,
        )

    def get_contents(self) -> None:
        """Get corpus contents into local.
        """

    def get_identities(self) -> List[ItemId]:
        """Get corpus item identities.

        Returns:
            Full item identity list.
        """

        # List up data information from local directories and files.
        ids: List[ItemId] = []
        for subtype in filter(lambda p: p.is_dir(), self._path_contents.iterdir()):
            for speaker in filter(lambda p: p.is_dir(), subtype.iterdir()):
                for uttr in filter(lambda p: p.is_file(), speaker.iterdir()):
                    ids.append(
                        ItemId(
                            subtype.name,
                            speaker.name,
                            uttr.stem,
                    ))

        return ids

    def get_item_path(self, item_id: ItemId) -> Path:
        """Get path of the item.

        Args:
            item_id: Identity of target item.
        Returns:
            Path of the target item.
        """
        return self._path_contents / item_id.subtype / item_id.speaker / f"{item_id.name}.wav"
