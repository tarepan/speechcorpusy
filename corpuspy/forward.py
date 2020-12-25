from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

import fsspec
from tqdm import tqdm
import requests

def get_GDrive_large_contents(id: str, path_archive_local: Path, total_size_GB: float) -> None:
    """
    Get large contents in Google Drive.
    Large contents needs special handling for virus check procedure.
    This utility wrap the procedure.

    Args:
        id: Google Drive contents ID.
        path_archive_local: Contents will be saved in this path.
        total_size_GB: Estimated contents size specified by yourself (hacky way).
    """
    path_archive_local.parent.mkdir(parents=True, exist_ok=True)

    # Request cookies for big file download.
    url_for_cookies = f"https://drive.google.com/uc?export=download&id={id}"
    r = requests.get(url_for_cookies)
    code: Optional[str] = None
    for ck in r.cookies:
        if "download_warning" in ck.name:
            code = ck.value
    if code is None:
        raise RuntimeError("download code is `None`. Please make issue in GitHub.")

    # Request corpus with cookies.
    url = f"{url_for_cookies}&confirm={code}"
    # Auto content-length acquisition do not work in GDrive.
    # file_size = int(requests.head(url, cookies=r.cookies).headers["content-length"])
    file_size = int(total_size_GB*1000*1000*1000)
    res = requests.get(url, cookies=r.cookies, stream=True)
    pbar = tqdm(total=file_size, unit="B", unit_scale=True)
    with open(path_archive_local, mode="wb") as file:
        for chunk in res.iter_content(chunk_size=1024):
            file.write(chunk)
            pbar.update(len(chunk))
        pbar.close()


def forward_file_from_GDrive(id_gdrive_contents: str, forward_to: str, size_GB: float) -> None:
    forward_to = f"simplecache::{forward_to}"
    with NamedTemporaryFile("w+b") as tmp:
        get_GDrive_large_contents(id_gdrive_contents, Path(tmp.name), size_GB)
        tmp.seek(0)
        print("Writing to the adress...")
        with fsspec.open(forward_to, "wb") as archive:
            archive.write(tmp.read())
        print("Written.")


if __name__ == "__main__":
    get_GDrive_large_contents("1NyiZCXkYTdYBNtD1B-IMAYCVa-0SQsKX", Path("./jsss_auto.zip"))