class TaxonomyFileNotFoundError(FileNotFoundError):

    def __init__(self):
        msg = "No taxonomy data file was found. Please download it using `bactax.ncbi.update_tax_data()`"
        super().__init__(msg)


class NoTaxonomyDataError(Exception):

    def __init__(self, **kwargs):
        constraints = [f"{k}={repr(v)}" for k, v in kwargs.items()]
        msg = f"Taxonomy information was not found for the provided input: {', '.join(constraints)}"
        super().__init__(msg)
