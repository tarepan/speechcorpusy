"""Archive and contents handlers"""


from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from hashlib import md5
from shutil import make_archive

import fsspec
from fsspec.utils import get_protocol

from speechcorpusy.components.taudio import extract_archive


def try_to_acquire_archive_contents(pull_from: str, extract_to: Path) -> bool:
    """Try to acquire the contents of the archive.

    Priority:
      1. (already extracted) local contents
      2. adress-specified (local|remote) archive through fsspec

    Returns:
        True if success_acquisition else False
    """

    # validation
    if extract_to.is_file():
        msg = f"contents ({str(extract_to)}) should be directory or empty, but it is file."
        raise RuntimeError(msg)

    # contents directory already exists.
    if extract_to.exists():
        return True
    else:
        file_system: fsspec.AbstractFileSystem = fsspec.filesystem(get_protocol(pull_from))
        # todo: get_protocol with cache
        archive_exists = file_system.exists(pull_from)
        archive_is_file = file_system.isfile(pull_from)

        # No corresponding archive. Failed to acquire.
        if not archive_exists:
            return False
        else:
            # validation
            if not archive_is_file:
                msg = f"Archive ({pull_from}) should be file or empty, but is directory."
                raise RuntimeError(msg)

            # A dataset file exists, so pull and extract.
            pull_from_with_cache = f"simplecache::{pull_from}"
            extract_to.mkdir(parents=True, exist_ok=True)
            print("Accessing the archive in the adress...")
            with fsspec.open(pull_from_with_cache, "rb") as archive:
                with NamedTemporaryFile("ab") as tmp:
                    print("Reading the archive in the adress...")
                    while True:
                        # Read every 100 MB for large corpus.
                        d = archive.read(100*1000*1000)
                        if d:
                            tmp.write(d)
                        else:
                            break
                    tmp.seek(0)
                    print("Read.")

                    print("Extracting...")
                    extract_archive(tmp.name, str(extract_to))
                    print("Extracted.")
            return True


def save_archive(path_contents: Path, adress_archive: str) -> None:
    """Save contents as a ZIP archive.

    Save contents of specified local path as ZIP archive in the specified adress through `fsspec`.

    Args:
        path_contents: Contents root directory path.
        adress_archive: Saved adress.
    """

    # TempDir for garbage-less upload
    with TemporaryDirectory() as tmpdir:
        # zip with deflate compression
        print("Archiving...")
        make_archive(f"{tmpdir}/tmp", "zip", root_dir=path_contents)
        print("Archived.")

        # write (==upload) the archive
        with fsspec.open(f"simplecache::{adress_archive}", "wb") as destination:
            with open(f"{tmpdir}/tmp.zip", "rb") as archive:
                print("Writing archive...")
                destination.write(archive.read())
                print("Wrote.")


def hash_args(*args) -> str:
    """Hash all arguments.
    """

    contents = ""
    for arg in args:
        contents = f"{contents}_{str(arg)}"
    contents = md5(contents.encode('utf-8')).hexdigest()
    return contents
