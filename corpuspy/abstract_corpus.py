"""Corpus interfaces and handling functions.

Common interface and functions for corpus.
Inheritance of the interface and method implementation with handling functions improve corpus handler.

    Typical usage example:

    ```python
    Id = NamedTuple("subtype", "serial_num")
    class MyCorpus(AbstractCorpus[Id]):
        ...
    ```

## Glossary
- archive: Single archive file.
- contents: A directory in which archive's contents exist.
"""


from typing import Generic, TypeVar, Callable, Optional, List
from abc import ABC, abstractmethod
from pathlib import Path
import shutil

import fsspec

from .archive import try_to_acquire_archive_contents


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


def save_archive(path_contents: Path, path_archive_local: Path, adress_archive: str) -> None:
    """Save contents as ZIP archive.

    Args:
        path_contents: Contents root directory path
        path_archive_local: Local path of newly generated archive file
        adress_archive: Saved adress
    """
    shutil.make_archive(str(path_archive_local.with_suffix("")), "zip", root_dir=path_contents)

    # write (==upload) the archive
    with open(path_archive_local, mode="rb") as stream_zip:
        with fsspec.open(f"simplecache::{adress_archive}", "wb") as f:
            f.write(stream_zip.read())


def get_contents(adress: str, extract_to: Path, download_origin: bool, forwarder: Callable[[], None]) -> None:
    """Get the archive and extract the contents from adress or origin.

    Try to get contents from the archive in the `fsspec`-compatible adress.
    If cannot get, forward original archive to the adress, then retry get process.

    Args:
        adress: 
        extract_to:
        download_origin:
        forwarder: 
    """

    # Design Notes:
    #   Forwarding is corpus-specific parts, so it is separated as forwarder callback.
    #     e.g. 'S3 through fsspec' vs 'large Google Drive file'

    acquired = try_to_acquire_archive_contents(adress, extract_to)
    if not acquired:
        if download_origin:
            forwarder()
            acquired_in_retry = try_to_acquire_archive_contents(adress, extract_to)
            if not acquired_in_retry:
                raise RuntimeError("Failed to acquire contents from the adress & origin.")
        else:
            raise RuntimeError(f"Specified corpus archive (`{adress}`) cannot be acquired. Enable `download_origin`")
