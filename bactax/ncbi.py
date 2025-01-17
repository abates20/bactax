from typing import Optional
from itertools import zip_longest
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import gzip
from datetime import date

import polars as pl
import requests
from rich.progress import track

from . import utils


def update(show_progress: bool = True):
    """
    Update the taxonomy data that the package uses.

    Replaces the current taxonomy data with newly downloaded
    data from NCBI.
    """
    current_file = utils.get_taxonomy_data_filepath()
    new_file = utils.new_taxonomy_data_filepath()

    download_tax_data(new_file, show_progress=show_progress)

    if (
        current_file is not None
        and current_file != new_file
        and Path(new_file).exists()  # Delete old only if new exists
    ):
        Path(current_file).unlink()


def download_tax_data(save_path=None, show_progress: bool = True):
    """
    Downloads the bacterial taxonomy data from NCBI and saves it
    to a gzip-compressed csv.
    """
    if save_path is None:
        save_path = f"taxonomy_{date.today()}.gz"

    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Download the taxonomy info from NCBI
        tax_zip = tmpdir / "tax.zip"
        _download_url(
            "https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.zip",
            tax_zip,
            show_progress=show_progress,
            description="Downloading taxonomy data from NCBI...",
        )

        # Pull out the rankedlineage.dmp file
        extract_file = "rankedlineage.dmp"
        with ZipFile(tax_zip, "r") as z_obj:
            tax_file = z_obj.extract(extract_file, path=tmpdir)

        # Load the taxonomy data from the .dmp file
        columns = [
            "tax_id",
            "tax_name",
            "species",
            "genus",
            "family",
            "order",
            "class",
            "phylum",
            "kingdom",
            "superkingdom",
        ]
        taxdata = _read_dmp(tax_file, columns)

        # Save the bacteria taxonomy info in a compact format
        bacteria_tax = taxdata.filter(pl.col("superkingdom") == "Bacteria")
        with gzip.open(save_path, "wb") as f:
            bacteria_tax.write_csv(f)


def _download_url(
    url,
    save_path,
    chunk_size: int = 128,
    show_progress: bool = True,
    description: Optional[str] = None,
):
    """
    Downloads the file specified by the url to the
    indicated `save_path`.
    """
    if description is None:
        description = f"Downloading {url}..."

    r = requests.get(url, stream=True)
    total_size = r.headers.get("content-length", None)
    if total_size is not None:
        total_size = (int(total_size) / chunk_size) + 1

    with open(save_path, "wb") as fd:
        if show_progress:
            download_iter = track(
                r.iter_content(chunk_size=chunk_size),
                description=description,
                total=total_size,
            )
        else:
            download_iter = r.iter_content(chunk_size=chunk_size)

        for chunk in download_iter:
            fd.write(chunk)

    return save_path


def _read_dmp(file: str, columns: list):
    """
    Reads a .dmp file from NCBI and returns a polars
    DataFrame with the data.
    """
    data = {c: [] for c in columns}
    with open(file, "r") as f:
        for line in f:
            items = line.rstrip("\t|\n").split("\t|\t")

            for col, item in zip_longest(columns, items):
                data[col].append(item)

    dataframe = pl.DataFrame(data)
    return dataframe
