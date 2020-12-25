from typing import Callable
from pathlib import Path

from corpuspy.components.archive import try_to_acquire_archive_contents


def get_contents(adress_from: str, extract_to: Path, download_origin: bool, forwarder: Callable[[], None]) -> None:
    """Get the archive and extract the contents from adress or origin.

    Try to get contents from the archive in the `fsspec`-compatible adress.
    If cannot get, forward original archive to the adress, then retry get process.

    Args:
        adress_from: Adress from which archive is acquired.
        extract_to: Local path to archive is extracted (contents generated).
        download_origin: If True forward origin when the adress is empty.
        fallback_forward: Forward original archive to the adress.
    """

    # Design Notes:
    #   Forwarding is corpus-specific parts, so it is separated as forwarder callback.
    #     e.g. 'S3 through fsspec' vs 'large Google Drive file'

    acquired = try_to_acquire_archive_contents(adress_from, extract_to)
    if not acquired:
        if download_origin:
            forwarder()
            acquired_in_retry = try_to_acquire_archive_contents(adress_from, extract_to)
            if not acquired_in_retry:
                raise RuntimeError("Failed to acquire contents from the adress & origin.")
        else:
            raise RuntimeError(f"Specified corpus archive (`{adress_from}`) cannot be acquired. Enable `download_origin`")
