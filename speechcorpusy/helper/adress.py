"""Corpus adress handling helpers"""


from pathlib import Path
from typing import Optional, Tuple


def get_adress(
    adress_archive_root: Optional[str],
    corpus_name: str,
    variant_type: str,
    archive_name: str,
    ) -> Tuple[str, Path]:
    """Get the adress of a archive file and a contents directory of the corpus.

    Args:
        adress_archive_root: The adress under which archive is/will_be placed
        corpus_name: Name of corpus
        variant_type: Corpus variant type (e.g. `v1.0` and `v1.1`)
        archive_name: Name of corpus archive file name
    Returns: [archive file adress, contents directory path]
    """

    # Design Notes:
    #   Why not `Path` object? -> Archive adress could be remote url
    #
    # Directory structure:
    #     corpuses/{corpus_name}/{variant_type}/
    #         archive/{archive_name}
    #         contents/{actual_data_here}

    # Contents: Placed under default local directory
    contents_root = local_root = "./tmp"
    # Archive: Placed under given adress or default local directory
    archive_root = adress_archive_root or local_root

    rel_corpus = f"corpuses/{corpus_name}/{variant_type}"
    archive_file = f"{archive_root}/{rel_corpus}/archive/{archive_name}"
    contents_dir = f"{contents_root}/{rel_corpus}/contents"
    return archive_file, Path(contents_dir)


def extract_name_and_variant(name_andor_variant: str, default_variant: str) -> tuple[str, str]:
    """Extract corpus name and variant specifier from `{name}[=={variant}]` string."""
    corpus_name_and_var = name_andor_variant.split("==")
    corpus_name = corpus_name_and_var[0]
    corpus_variant = default_variant if len(corpus_name_and_var) == 1 else corpus_name_and_var[1]
    return corpus_name, corpus_variant
