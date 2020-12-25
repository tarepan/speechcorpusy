from corpuspy.components.download import download_GDrive_large_contents
from pathlib import Path
from tempfile import NamedTemporaryFile

import fsspec


def forward_from_GDrive(id_gdrive_contents: str, forward_to: str, size_GB: float) -> None:
    """Forward a file from Google Drive to specified adress.

    Forward GoogleDrive -> any_adress through fsspec (e.g. local, S3, GCP).

    Args:
        id_gdrive_contents: Google Drive contents ID
        forward_to: forward distination adress
    """

    forward_to_with_cache = f"simplecache::{forward_to}"
    # TempFile for garbage-less forwarding
    with NamedTemporaryFile("w+b") as tmp:
        download_GDrive_large_contents(id_gdrive_contents, Path(tmp.name), size_GB)
        tmp.seek(0)
        print("Forward: Writing to the adress...")
        with fsspec.open(forward_to_with_cache, "wb") as archive:
            archive.write(tmp.read())
        print("Forward: Written.")


if __name__ == "__main__":
    pass