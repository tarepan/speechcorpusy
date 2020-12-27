from typing import Generic, TypeVar, Optional, List
from abc import ABC, abstractmethod
from pathlib import Path


# Corpus item identity.
Id = TypeVar('Id')


class AbstractCorpus(ABC, Generic[Id]):
    """Interface of corpus archive/contents handler.
    """
    
    @abstractmethod
    def __init__(self, adress: Optional[str] = None, download_origin: bool = False) -> None:
        """Initiate AbstractCorpus with archive options.

        Args:
            adress: Private mirror (e.g. path, S3) from/to which corpus archive will be read/written through `fsspec`.
            download_origin: Download original corpus when there is no corpus in the adress.
        """

        # Design Notes:
        #   High-frequency access to the origin corpus (discribution site) should be avoided.
        #   On ther other hand, cloud-native learning environment (e.g. Docker-based ML) become popular,
        #   and it needs corpus access each time.
        #   Private mirror of the corpus resolve this problem, so `adress` argument is introduced.
        #   This handler first try to access the private `adress`.
        #   If failed (e.g. no mirror file) and `download_origin`==True,
        #   the handler call `forward_from_origin` for origin->mirror archive forwarding.
        #   Now the archive is in the mirror adress, retry mirror access.

        pass

    @abstractmethod
    def get_contents(self) -> None:
        """Get corpus contents into local.
        """

        # Helpers:
        #   `get_contents`:
        #       `get_contents` is a function in `corpuspy.helper.contents` module.
        #       This helper get corpus contents from private adress with origin->private forwarding fallback-callback.

        pass

    @abstractmethod
    def forward_from_origin(self) -> None:
        """Forward original corpus archive to the adress.
        """

        # Helpers:
        #  `forward_from_GDrive`:
        #     `forward_from_GDrive` is a function in `corpuspy.helper.forward` module.
        #     This helper forward an big (>1GB) archive file in Google Drive to any your private adress.

        pass

    @abstractmethod
    def get_identities(self) -> List[Id]:
        """Get corpus item identities.

        Returns:
            Full item identity list.
        """

        # Design Notes:
        #   Path acquisition through ID is responsibility of corpus handler.
        #   Sometimes corpus lost items (e.g. lost #77 in 100-item corpus).
        #   If users handle serial number for item access, users have to be conscious of missing items.
        #   If corpus handler provide IDs and users handle the ID, the handler can manage missings during ID generation.

        # Implementation Notes:
        #   This is corpus-specific part, so this is your responsibility.
        #   ID class inheriting NamedTuple may be easy to handle.

        pass

    @abstractmethod
    def get_item_path(self, id: Id) -> Path:
        """Get a path of the item.

        Args:
            id: Target item identity.
        Returns:
            Path of the specified item.
        """

        # Implementation Notes:
        #   This is corpus-specific part, so this is your responsibility.
        #   In most cases, simply making Path based on ID argument is enough.

        pass