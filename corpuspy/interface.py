from typing import Generic, TypeVar, Optional, List
from abc import ABC, abstractmethod
from pathlib import Path


# Corpus item identity.
Id = TypeVar('Id')


class AbstractCorpus(ABC, Generic[Id]):
    """Interface of corpus archive/contents handler.
    """
    
    @abstractmethod
    def __init__(self, adress: Optional[str] = None, download_origin : bool = False) -> None:
        """Initiate AbstractCorpus with archive options.

        Args:
            adress: Corpus archive adress (e.g. path, S3) from/to which archive will be read/written through `fsspec`.
            download_origin: Download original corpus when there is no corpus in local and specified adress.
        """
        pass

    @abstractmethod
    def get_contents(self) -> None:
        """Get corpus contents into local.
        """
        pass

    @abstractmethod
    def forward_from_origin(self) -> None:
        """Forward original corpus archive to the adress.
        """
        pass

    @abstractmethod
    def get_identities(self) -> List[Id]:
        """Get corpus item identities.

        Returns:
            Full item identity list.
        """
        pass

    @abstractmethod
    def get_item_path(self, id: Id) -> Path:
        """Get a path of the item.

        Args:
            id: Target item identity.
        Returns:
            Path of the specified item.
        """
        pass