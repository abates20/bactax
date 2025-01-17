from warnings import warn as _warn

from .utils import time_since_last_taxonomy_update as _time_since_last_update
from .ncbi import update as update
from .tax import Taxonomy as Taxonomy, get_taxonomy as get_taxonomy
from .gram import (
    gram_stain as gram_stain,
    is_gram_negative as is_gram_negative,
    is_gram_positive as is_gram_positive,
    Gram as Gram
)
from .errors import (
    NoTaxonomyDataError as NoTaxonomyDataError,
    TaxonomyFileNotFoundError as TaxonomyFileNotFoundError,
)


if _time_since_last_update().days > 365:
    _warn(
        "It has been more than a year since the taxonomy data was last "
        "updated. Please consider updating with `bactax.update()`"
    )
