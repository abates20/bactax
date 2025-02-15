# bactax
A simple python tool for getting bacterial taxonomy and gram stain information from NCBI taxonomy data.

## Installation

Currently, bactax can only be installed from Github:

```sh
pip install git+https://github.com/abates20/bactax
```

## Usage

### Getting taxonomic information for a bacteria

```python
import bactax

genus = "akkermansia"
taxonomy = bactax.get_taxonomy(genus=genus) # returns a Taxonomy object
```

This will return a `Taxonomy` object with all the information above the level of genus filled in (i.e., family, order, class, etc.).

### Determining gram stain

```python
import bactax

genus = "escherichia"
gram_stain = bactax.gram_stain(genus=genus) # returns Gram.NEGATIVE
```

### Updating the taxonomy data

bactax uses data from NCBI's taxonomy database. This data is downloaded and stored in a gzip file within the package. Since NCBI regularly updates their data, bactax provides an method to download the latest taxonomy database from NCBI.

```python
import bactax
bactax.update()
```
