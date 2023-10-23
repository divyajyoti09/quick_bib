#!/usr/bin/env python
# coding: utf-8

# ## Import packages

# In[187]:


import bibtexparser as bp
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase


# In[188]:


bw = BibTexWriter()
db_master = BibDatabase()


# ## Define base functions

# In[189]:


def in_nested_list(my_list, item):
    """
    Determines if an item is in my_list, even if nested in a lower-level list.
    """
    if item in my_list:
        return True
    else:
        return any(in_nested_list(sublist, item) for sublist in my_list if isinstance(sublist, list))


# In[190]:


def flip_dict(my_dict):
    """
    Returns flipped dictionary with values as keys and vice versa
    
    Eg.
    If my_dcit = {'key1':'val1', 'key2':'val2', 'key3':'val2'}
    then returns: {'val1':['key1'], 'val2':['key2', 'key3']}
    """
    flipped = {}
    for key, value in my_dict.items():
        if value not in flipped:
            flipped[value] = [key]
        else:
            flipped[value].append(key)
    return(flipped)


# In[191]:


def find_key_for_value(my_dict, val):
    """
    Finds the key(s) for a given value of a dictionary.
    
    Returns:
    --------
    [key(s)]
    """
    try:
        flipped_dict = flip_dict(my_dict)
        return(flipped_dict[val])
    
    except KeyError:
        pass


# In[192]:


def find_repeated_values_in_dict(my_dict):
    """
    If key1 and key2 have same repeated_val1; and key3, key4, and key5 have the same repeated_val2; then
    Returns a dictionary of the form: {repeated_val1: [key1, key2], repeated_val2: [key3, key4, key5]}
    """
    flipped_dict = flip_dict(my_dict)

    repeated = {}
    for key in flipped_dict.keys():
        if len(flipped_dict[key])!=1:
            repeated[key] = flipped_dict[key]
    return(repeated)


# ## Define BibDatabase functions

# In[193]:


def is_inspire_HEP_key(my_string):
    first = my_string.split(':')[0]
    rest = ''.join(my_string.split(':')[1:])
    year = rest[:4]
    last = rest[4:]
    hyphenated_name_remove_hyphen = ''.join(first.split('-'))
    if first.isalpha() and year.isnumeric() and last.isalpha():
        return(True)
    elif hyphenated_name_remove_hyphen.isalpha() and year.isnumeric() and last.isalpha():
        return(True)
    elif len(my_string.split(':'))>2:
        return(False)
    else:
        return(False)


# In[194]:


def check_inspire_HEP_key(bib_entry):
    """
    Checks if the bib_entry has the ID of the format of inspire HEP eg. Mishra:2014xyz
    
    Returns:
    ----------
    Boolean 
    """
    ID = bib_entry['ID']
    if is_inspire_HEP_key(ID):
        return(True)
    else:
        return(False)


# In[195]:


def get_non_inspire_HEP_entries(bib_database):
    """
    Returns a list of all the keys in the bib_database which don't have Inspire HEP format
    """
    lst = []
    for entry in bib_database.entries:
        if not check_inspire_HEP_key(entry):
            lst.append(entry['ID'])
    return(lst)


# In[196]:


def get_arxiv_ID(bib_entry):
    if 'eprint' in bib_entry.keys():
        return(bib_entry['eprint'].split(':')[-1])
    else:
        #print('No eprint found for bib_entry ID "{}".'.format(bib_entry['ID']))
        pass


# In[197]:


def get_arxiv_IDs(bib_database):
    arxiv_IDs = {}
    for key in bib_database.entries_dict.keys():
        arxiv_ID = get_arxiv_ID(bib_database.entries_dict[key])
        if arxiv_ID != None:
            arxiv_IDs[key] = arxiv_ID
    return(arxiv_IDs)


# In[198]:


def no_arxiv_IDs(bib_database):
    """
    Returns keys in bib_database without arxiv IDs.
    """
    keys_lst = []
    for key in bib_database.entries_dict.keys():
        arxiv_ID = get_arxiv_ID(bib_database.entries_dict[key])
        if arxiv_ID==None:
            keys_lst.append(key)
    return(keys_lst)


# In[199]:


def get_doi(bib_entry):
    if 'doi' in bib_entry.keys():
        if 'https' in bib_entry['doi']:
            doi = bib_entry['doi'].split('https://')[-1]
        else:
            doi = bib_entry['doi']
        return(doi)
    else:
        #print('No doi found in bib_entry ID "{}".'.format(bib_entry['ID']))
        pass


# In[200]:


def get_dois(bib_database):
    dois = {}
    for key in bib_database.entries_dict.keys():
        doi = get_doi(bib_database.entries_dict[key])
        if doi != None:
            dois[key] = doi
    return(dois)


# In[201]:


def repeats_in_db(bib_database):
    """
    checks for repeated entries in a single bib_database
    Returns repeated IDs if found.
    """
    arxiv_IDs = get_arxiv_IDs(bib_database)
    dois = get_dois(bib_database)

    if len(arxiv_IDs.values())==len(set(arxiv_IDs.values())) and len(dois.values())==len(set(dois.values())):
        print('No duplicates found.')
        return({}, {})
    else:
        repeated_arxiv = find_repeated_values_in_dict(arxiv_IDs)
        repeated_doi = find_repeated_values_in_dict(dois)
        return(repeated_doi, repeated_arxiv)


# In[202]:


def check_repeats_in_db(bib_database):
    """
    Returns True if repeated entries are present in bib_database else returns False.
    """
    rd, ra = repeats_in_db(bib_database)
    if len(rd)==0 and len(ra)==0:
        return(False)
    else:
        return(True)


# In[203]:


def repeats_in_two_dbs(bib_database1, bib_database2):
    """
    Warning: Please make sure the two databases don't have repeated values among themselves.

    Checks the entries from bib_database2 against those in bib_database1

    Returns:
    ------------
    Repeated IDs (if found) as dictionary in the format:
    {repeated_val1:[db1_key, db2_key], repeated_val2: [db1_key, db2_key]}
    where db1_key corresponds to key for the repeated value in database1 and so on.
    repeated_val can be a DOI or arxiv ID of the repeated bib_entry
    """
    arxiv_IDs1 = get_arxiv_IDs(bib_database1)
    arxiv_IDs2 = get_arxiv_IDs(bib_database2)

    dois1 = get_dois(bib_database1)
    dois2 = get_dois(bib_database2)

    if len(arxiv_IDs1.values())!=len(set(arxiv_IDs1.values())) or len(dois1.values())!=len(set(dois1.values())):
        print('Database1 has repeated entries. Please eliminate all repeated entries then proceed.')
        return
    if len(arxiv_IDs2.values())!=len(set(arxiv_IDs2.values())) or len(dois2.values())!=len(set(dois2.values())):
        print('Database2 has repeated entries. Please eliminate all repeated entries then proceed.')
        return

    repeated_arxiv = {}
    for key2, val2 in arxiv_IDs2.items():
        if val2 in arxiv_IDs1.values():
            key1 = find_key_for_value(arxiv_IDs1, val2)[0]
            repeated_arxiv[val2] = [key1, key2]
    if len(repeated_arxiv)==0:
        print('No duplicate arxiv IDs found.')

    repeated_doi = {}
    for key2, val2 in dois2.items():
        if val2 in dois1.values():
            key1 = find_key_for_value(dois1, val2)[0]
            repeated_doi[val2] = [key1, key2]
    if len(repeated_doi)==0:
        print('No duplicate DOIs found.')

    return(repeated_doi, repeated_arxiv)


# In[204]:


def check_repeats_in_two_dbs(bib_database1, bib_database2):
    """
    Returns True if there are entries with duplicate DOIs or arxiv_IDs between the two databases else returns False.
    """
    rd, ra = repeats_in_two_dbs(bib_database1, bib_database2)
    if len(rd)==0 and len(ra)==0:
        return(False)
    else:
        return(True)


# In[205]:


def merge_bib_entries(entry1, entry2):
    """
    Merges entry2 into entry1 by adding any missing fields in entry1. 
    If one or both of the entries have 'ID' in the inspire HEP format, 
    the inspire HEP ID will be used for final entry. Else, the ID of 
    Warning: It replaces the old values of entry1 with the corresponding values of entry2.

    Returns:
    --------
    Final entry as a dictionary.
    """
    a1 = get_arxiv_ID(entry1)
    a2 = get_arxiv_ID(entry2)

    d1 = get_doi(entry1)
    d2 = get_doi(entry2)

    if a1!=a2 and d1!=d2:
        print('Both entries have different DOI or arxiv IDs. Cannot confirm that they are the same entry. Please merge them manually.')
        return

    else:
        final_entry = entry1.copy()
        final_entry.update(entry2)
        if is_inspire_HEP_key(final_entry['ID']):
            return(final_entry)
        else:
            if is_inspire_HEP_key(entry1['ID']):
                final_entry['ID'] = entry1['ID']
                return(final_entry)
            elif is_inspire_HEP_key(entry2['ID']):
                final_entry['ID'] = entry2['ID']
                return(final_entry)
            else:
                return(final_entry)


# In[206]:


def merge_duplicates_in_db(bib_database):
    """
    Merges all duplicate entries (duplicates in terms of arxiv ID or doi).

    Returns:
    --------
    BibDatabase without duplicates.
    """
    repeated_doi, repeated_arxiv = repeats_in_db(bib_database)

    combined_repeats = repeated_doi.copy()
    combined_repeats.update(repeated_arxiv)

    merged_db = BibDatabase()
    merged_db.entries = []
    
    seen = {}
    for key in bib_database.entries_dict.keys():
        if in_nested_list(combined_repeats.values(), key)==False:
            merged_db.entries.append(bib_database.entries_dict[key])
        else:
            lst = []
            for repeat_key in combined_repeats.keys():
                if key in combined_repeats[repeat_key]:
                    lst = lst+combined_repeats[repeat_key]
            lst = [*set(lst)]

            entry1_key = lst[0]
            entry1 = bib_database.entries_dict[entry1_key]

            for other_keys in lst[1:]:
                merged_entry = merge_bib_entries(entry1, bib_database.entries_dict[other_keys])
                entry1 = merged_entry
            
            seen[entry1['ID']] = entry1
                
            
    for key in seen.keys():
        merged_db.entries.append(seen[key])
    return(merged_db)


# In[207]:


def merge_two_databases(bib_database1, bib_database2):
    """
    First checks for any duplicates in the individual databases and removes them.
    Then merges database2 into database1 such that any entry which is repeated is merged.

    Returns:
    ----------
    Merged BibDatabase without duplicates.
    """
    print('Checking for duplicates in database 1...')
    bdb1 = merge_duplicates_in_db(bib_database1)
    print('Checking for duplicates in database 2...')
    bdb2 = merge_duplicates_in_db(bib_database2)
    print('\n')

    print('Checking for repeats between databases...')
    repeated_doi, repeated_arxiv = repeats_in_two_dbs(bdb1, bdb2)

    combined_repeats = repeated_doi.copy()
    combined_repeats.update(repeated_arxiv)

    final_db = BibDatabase()
    final_db.entries = []

    for key1 in bdb1.entries_dict.keys():
        final_db.entries.append(bdb1.entries_dict[key1])

    for key2 in bdb2.entries_dict.keys():
        if in_nested_list(combined_repeats.values(), key2)==False:
            final_db.entries.append(bdb2.entries_dict[key2])
        else:
            if in_nested_list(repeated_doi.values(), key2)==True:
                key1 = repeated_doi[bdb2.entries_dict[key2]['doi']][0]
            elif in_nested_list(repeated_arxiv.values(), key2)==True:
                key1 = repeated_arxiv[bdb2.entries_dict[key2]['eprint']][0]
                
            merged_bib_entry = merge_bib_entries(final_db.entries_dict[key1], bdb2.entries_dict[key2])
            final_db.entries_dict[key1].update(merged_bib_entry)

    print('Done')
    return(final_db)


# ## Define functions for bib files

# In[210]:

def get_bib_database_from_file(file):
    """
    Returns bib_database from a bib file. This can then be used for various other functions.
    """
    with open(file) as f:
        db = bp.load(f)
        f.close()
    return(db)

def remove_repeats_from_file(file):
    """
    Merges all the repeated entries in the file and overwrites the existing file.
    """
    with open(file) as f:
        db = bp.load(f)
        f.close()
        
    if check_repeats_in_db(db)==False:
        print('No repeated entries found. Exiting.')
        return
    else:
        db_new = merge_duplicates_in_db(db)
        with open(file, 'w') as f:
            f.write(bw.write(db_new))
            f.close()


# In[211]:


def remove_repeats_from_file_to_new(new_file, old_file):
    """
    Merges all the repeated entries in the old_file and writes into new_file.
    Old file is left untouched.
    If no repeated entries are found, the new file will have the exact same entries as the old one but in alphabetical order.
    Caution: If two entries have the same key, the function does not distinguish between them. These are loaded as a single entry into the bib database and hence not counted as repeated. The new file will only have one of the two.
    """
    with open(old_file) as f:
        db_old = bp.load(f)
        f.close()
        
    if check_repeats_in_db(db_old)==False:
        print('No repeated entries found. The old file will have the same entries (in alphabetical order) as new except repeated keys which have only been counted once (see docstring for details).')
        with open(new_file, 'w') as f:
            f.write(bw.write(db_old))
            f.close()
        return
    else:
        db_new = merge_duplicates_in_db(db_old)
        with open(new_file, 'w') as f:
            f.write(bw.write(db_new))
            f.close()


# In[212]:


def append_file_to_master(master_file, file1):
    """
    Appends the bib entries of file1 to master_file after checking for duplicates.
    Parameters:
    ------------
    master_file: path of the file to which contents of file1 will be appended
    format: master_file.bib
    
    file1: path of the file whose contents will be appended to master_file
    format: file1.bib
    """
    
    with open(master_file) as f:
        master_db = bp.load(f)
        f.close()
        
    with open(file1) as f:
        file1_db = bp.load(f)
        f.close()
            
    if check_repeats_in_db(master_db)==True:
        print(master_file + ' has repeated entries. First eliminate repeats in master then proceed.')
        print('You can remove repeats from the master file by using the functions:\
                remove_repeats_from_file() or remove_repeats_from_file_to_new().')
        return
    if check_repeats_in_db(file1_db)==True:
        print(file1 + ' has repeated entries. First eliminate repeats in the file then proceed.')
        print('You can remove repeats from the file by using the function: remove_repeats_from_file().')
        return
    
    if check_repeats_in_two_dbs(master_db, file1_db)==False:
        with open(master_file, 'a') as f:
            f.write('\n')
            f.write(bw.write(file1_db))
            f.close()
    else:
        print('Repeated entries found between master and the file. Merging the repeated entries.')
        final_db = merge_two_databases(master_db, file1_db)
        with open(master_file, 'w') as f:
            f.write('\n')
            f.write(bw.write(final_db))
            f.close()


# In[213]:


def merge_two_files_to_new(new_file, file1, file2):
    """
    Merges repeated entries in individual bib files.
    Then merges the repeated entries amongst two bib files and puts the database in new_file.
    """
    with open(file1) as f:
        db1 = bp.load(f)
        f.close()
    
    with open(file2) as f:
        db2 = bp.load(f)
        f.close()
        
    db1_merged = merge_duplicates_in_db(db1)
    db2_merged = merge_duplicates_in_db(db2)
    
    db_final = merge_two_databases(db1_merged, db2_merged)
    
    with open(new_file, 'w') as f:
        f.write(bw.write(db_final))
        f.close()


# In[214]:


def check_missing_arxiv_in_file(file):
    with open(file) as f:
        db = bp.load(f)
        f.close()
        
    return(no_arxiv_IDs(db))


# In[215]:


def check_if_repeats_in_file(file):
    with open(file) as f:
        db = bp.load(f)
        f.close()
    if check_repeats_in_db(db)==False:
        print('There are no duplicate entries in file.')
    else:
        print('The duplicates are:')
        return(repeats_in_db(db))


