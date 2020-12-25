from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from hashlib import md5
from shutil import make_archive

import fsspec
from fsspec.utils import get_protocol
from torchaudio.datasets.utils import extract_archive


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
        raise RuntimeError(f"contents ({str(extract_to)}) should be directory or empty, but it is file.")

    # contents directory already exists.
    if extract_to.exists():
        return True
    else:
        fs: fsspec.AbstractFileSystem = fsspec.filesystem(get_protocol(pull_from))
        # todo: get_protocol with cache
        archiveExists = fs.exists(pull_from)
        archiveIsFile = fs.isfile(pull_from)

        # No corresponding archive. Failed to acquire.
        if not archiveExists:
            return False
        else:
            # validation
            if not archiveIsFile:
                raise RuntimeError(f"Archive ({pull_from}) should be file or empty, but is directory.")

            # A dataset file exists, so pull and extract.
            pull_from_with_cache = f"simplecache::{pull_from}"
            extract_to.mkdir(parents=True, exist_ok=True)
            with fsspec.open(pull_from_with_cache, "rb") as archive:
                with NamedTemporaryFile("wb") as tmp:
                    tmp.write(archive.read())
                    tmp.seek(0)
                    print("extracting...")
                    extract_archive(tmp.name, str(extract_to))
                    print("extracted.")
            return True


def save_archive(path_contents: Path, adress_archive: str) -> None:
    """Save contents as a ZIP archive.

    Save contents of specified local path as ZIP archive in the specified adress through `fsspec`.

    Args:
        path_contents: Contents root directory path.
        adress_archive: Saved adress.
    """

    with TemporaryDirectory() as tmpdir:
        # zip with deflate compression
        make_archive(f"{tmpdir}/tmp", "zip", root_dir=path_contents)
        # write (==upload) the archive
        with fsspec.open(f"simplecache::{adress_archive}", "wb") as target:
            with open(f"{tmpdir}/tmp.zip", "rb") as archive:
                target.write(archive.read())


def hash_args(*args) -> str:
    """Hash all arguments.
    """

    contents = ""
    for c in args:
        contents = f"{contents}_{str(c)}"
    contents = md5(contents.encode('utf-8')).hexdigest()
    return contents
