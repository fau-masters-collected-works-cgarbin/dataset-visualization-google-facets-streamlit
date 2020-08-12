'''Preprocess the dataset

- Separate the diseases into indicator (true/false) columns
- Bin the ages
- Mark images as either training or test

See more details about the dataset in the data folder.
'''
import pandas as pd

_DATASET = 'data/Data_Entry_2017_v2020.csv'
_TRAIN_VAL_LIST = 'data/train_val_list.txt'
_TEST_LIST = 'data/test_list.txt'


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

    # Columns must match the original 11, plus:
    #    - 15 for each disease (14) + 'no finding'
    assert ds.shape[1] == 11 + 15


def get_dataset() -> pd.DataFrame:
    '''Reads the raw files that comprise the dataset and creates a preprocessed dataset.

    Returns:
        The preprocessed dataset.
    '''

    ds = pd.read_csv(_DATASET)

    # Split diseases into separate indicator columns
    indicators = ds['Finding Labels'].str.get_dummies('|')
    ds = pd.concat([ds, indicators], axis='columns')
    print(ds)
    print(indicators)
    _verify_dataset(ds)
    return ds


# To allow standalone execution for tests
if __name__ == "__main__":
    dataset = get_dataset()
    print(dataset)
