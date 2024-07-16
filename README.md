This is a bibliography package to assist in managing bib files and bib entries. It contains various functions: append entries to bib files, search whether bib entries have arxiv links, remove duplicates from bib file, merge two bib files, and so on.

## Installation instructions:

### Create a new conda env
```
conda create --name myenv python=3.10
conda activate myenv
```

### Clone and install the package
```
pip install bibtexparser
git clone https://github.com/divyajyoti09/quick_bib.git # or clone with ssh link git@github.com:divyajyoti09/quick_bib.git
cd quick_bib
pip install .

#python setup.py install # this has been deprecated in some versions of setuptools
```

### Add the env to jupyter-notebook
```
# Using it for jupyter-notebook
pip install ipykernel
python -m ipykernel install --user --name myenv
```

## Top features:

- Check for and merge the repeated entries in your bib file. This not only includes repeated keys (which is also checked by other platforms like overleaf), but also checks for repeated entries where DOI or arxiv ID is identical. 
- Arrange your bib file in alphabetical order while making sure that there are no repeated entries. This can be done by using the function: `quick_bib.remove_repeats_from_file_to_new`.
- Merge two bib files into one (merges the repeated entries between the two files).
- For those who like to cite only from InspireHEP (but their collaborators might not), `quick_bib` can be used to identify entries in a .bib which are not in InspireHEP format.

## Planned upgrades:

I'm always looking forward to suggestions. Please create issues for suggestions and any bugs that you encounter in the package. Here are some upgrades that I'm planning to implement in the future:
- Convert some of the functions to CLI functions.
- Identify missing journal entries and query from web (arxiv.org) whether the paper has been published since the entry was last included in the bib file.
- 
