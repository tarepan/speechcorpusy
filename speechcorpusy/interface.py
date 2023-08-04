"""speechcorpusy Interface"""


from typing import Optional, List
from abc import ABC, abstractmethod
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class ItemId:
    """Identity of corpus item.

    Args:
        corpus:  Name of corpus to which this item belong
        subtype: Sub-corpus name
        speaker: Speaker ID
        name:    Item name
    """
    corpus:  str
    subtype: str
    speaker: str
    name:    str
    # Design Note: Audio Length
    #   Why not audio length? -> 'Effective' length differ case by case.


@dataclass
class ConfCorpus:
    """Configuration of corpus.

    Args:
        name: Corpus name
        root: Adress of the directory under which the corpus archive is found or downloaded
        download: Whether to download original corpus if it is not found in `root`
    """

    # Design Notes:
    #   `root` & `download` are matched with `torchaudio.datasets`
    # Design Notes:
    #   name="" is for omegaconf
    name: str = ""
    root: Optional[str] = None
    download: bool = False

class AbstractCorpus(ABC):
    """Interface of corpus archive/contents handler.
    """

    @abstractmethod
    def __init__(self, conf: ConfCorpus) -> None:
        """Initialization without contents download/extraction.
        """

        # Design Notes:
        #   High-frequency access to the origin corpus (distribution site) should be avoided.
        #   At the same time, cloud-native environment (e.g. Docker-based ML) become popular
        #   and it needs corpus access each time.
        #   Private mirror of the corpus resolve this problem,
        #   so `adress_archive_root` is introduced.
        #   This handler first try to access the private `adress_archive_root`.
        #   If failed (i.e. no mirror file) and `download`==True,
        #   the handler call forwarding function for origin->mirror archive forwarding.
        #   Now the archive is in the mirror adress, retry mirror access.

        # Helpers:
        #     `get_adress`:
        #         `get_adress` is a function in `speechcorpusy.helper.adress` module.
        #         This helper get path of corpus archive file and contents directory.

    @abstractmethod
    def get_contents(self) -> None:
        """Get corpus contents into local.
        """

        # Helpers:
        #     `get_contents`:
        #         `get_contents` is a function in `speechcorpusy.helper.contents` module.
        #         This helper get corpus contents from private adress
        #         with origin->private forwarding fallback-callback.
        #    `forward`:
        #         `forward` is a function in `speechcorpusy.helper.forward` module.
        #         This helper forward any source file to any target adress.
        #    `forward_from_GDrive`:
        #         `forward_from_GDrive` is a function in `speechcorpusy.helper.forward` module.
        #         This helper forward an big (>1GB) archive file
        #         in Google Drive to any your private adress.

    @abstractmethod
    def get_identities(self) -> List[ItemId]:
        """Get corpus item identities.

        Returns:
            Full item identity list.
        """

        # Design Notes:
        #   Path acquisition through ID is responsibility of corpus handler.
        #   Sometimes corpus lost items (e.g. lost #77 in 100-item corpus).
        #   If users handle serial number for item access,
        #   users have to be conscious of missing items.
        #   If corpus handler provide IDs and users handle the ID,
        #   the handler can manage missings during ID generation.

        # Implementation notes:
        #   You should NOT have contents dependency.
        #   Corpus handler can be used without corpus itself.
        #   (e.g. Get item identities for a preprocessed dataset).
        #   Hard-coded identity list enable contents-independent identity acquisition.

    def get_identities_per_speaker(self) -> list[list[ItemId]]:
        """Get corpus item identities, grouped by `.speaker` attribute.

        Returns:
            - Utterance identities, grouped by speaker. e.g. [[spk0_uttr0, spk0_uttr1, ...], [spk2_uttr0, spk2_uttr1, ...]]
        """

        utterances = self.get_identities()
        speakers = sorted(list(set(map(lambda utter_id: utter_id.speaker, utterances))))
        utters_per_spks = [list(filter(lambda utter_id: utter_id.speaker == spk, utterances)) for spk in speakers] # pylint: disable = cell-var-from-loop

        return utters_per_spks

    @abstractmethod
    def get_item_path(self, item_id: ItemId) -> Path:
        """Get a path of the item.

        Args:
            item_id: Identity of target item.
        Returns:
            Path of the specified item.
        """

        # Implementation Notes:
        #   This is corpus-specific part, so this is your responsibility.
        #   In most cases, simply making Path based on ID argument is enough.
