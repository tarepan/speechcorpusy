"""Corpus contents handling helpers"""


from typing import Callable
from pathlib import Path

from corpuspy.components.archive import try_to_acquire_archive_contents


def get_contents(
    adress_archive_file: str,
    adress_contents_dir: Path,
    download_origin: bool,
    forwarder: Callable[[], None]
) -> None:
    """Get the archive and extract the contents from adress or origin.

    Try to get contents from the archive in the `fsspec`-compatible adress.
    If cannot get, forward original archive to the adress, then retry get process.

    Args:
        adress_archive_file: Archive file adress.
        adress_contents_dir: Contents directory, to which archive is extracted.
        download_origin: Whether to forward origin when the archive adress is empty.
        fallback_forward: Forward original archive to the adress.
    """

    # Design Notes:
    #   Forwarding is corpus-specific parts, so it is separated as forwarder callback.
    #     e.g. 'S3 through fsspec' vs 'large Google Drive file'

    acquired = try_to_acquire_archive_contents(adress_archive_file, adress_contents_dir)
    if not acquired:
        if download_origin:
            forwarder()
            acquired_in_retry = try_to_acquire_archive_contents(
                adress_archive_file,
                adress_contents_dir
            )
            if not acquired_in_retry:
                raise RuntimeError("Failed to acquire contents from the adress & origin.")
        else:
            m_1 = f"Specified corpus archive (`{adress_archive_file}`) cannot be acquired."
            m_2 = "Enable `download`"
            raise RuntimeError(f"{m_1} {m_2}")
