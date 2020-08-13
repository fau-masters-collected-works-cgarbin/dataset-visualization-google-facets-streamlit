'''Preprocess the dataset

- Separate the diseases into indicator (true/false) columns
- Bin the ages into MeSH age groups
- Mark images as either training or test

See more details about the dataset in the data folder.
'''
import pandas as pd

_DATASET = 'data/Data_Entry_2017_v2020.csv'
_TRAIN_VAL_LIST = 'data/train_val_list.txt'
_TEST_LIST = 'data/test_list.txt'

_AGE_GROUP = 'Age Group'


def _verify_dataset(ds: pd.DataFrame):
    '''Checks a few basic things about the dataset before using it.

    Verifies that the dataset has the content we expect. If any of these checks fail, either the
    dataset itself has changed or we made a mistake when preprocessing it.

    If the dataset has changed, upddate the checks to match the new dataset.

    If the dataset has not changed, there may be a mistake in the preprocessig code.

    Args:
        ds: the dataset after it was preprocessed.
    '''

    # Number of rows must match the original dataset
    assert ds.shape[0] == 112120

    # Number of columns must match the original 11, plus:
    #    - 15 for disease indicators (14 + 'no finding')
    #    - 1 for the age group
    assert ds.shape[1] == 11 + 15 + 1

    # Check a few disease indicators and age group
    assert _AGE_GROUP in ds.columns
    assert 'Mass' in ds.columns
    assert 'No Finding' in ds.columns


def get_dataset() -> pd.DataFrame:
    '''Reads the raw files that comprise the dataset and creates a preprocessed dataset.

    Returns:
        The preprocessed dataset: diseases are split into indicator (true/false) columns and ages
        are binned.
    '''

    ds = pd.read_csv(_DATASET)

    # Split diseases into separate indicator columns
    indicators = ds['Finding Labels'].str.get_dummies('|')
    ds = pd.concat([ds, indicators], axis='columns')

    # Bin the ages according to MeSH age groups
    # Best reference I found for MeSH groups: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1794003/
    # We have only complete years, so we can't use 'newborn'
    bins = [0, 2, 6, 13, 19, 45, 65, 80, 120]
    labels = ['Infant', 'Preschool', 'Child', 'Adolescent',
              'Adult', 'Middle age', 'Aged', 'Aged 80']
    ds[_AGE_GROUP] = pd.cut(ds['Patient Age'], bins=bins, labels=labels, right=False)

    print(ds)
    # print(indicators)
    _verify_dataset(ds)
    return ds


# To allow standalone execution for tests
if __name__ == "__main__":
    dataset = get_dataset()
    print(dataset)
