'''Makes the ChestX-ray14 dataset more usable by augmenting it.

- Separate the diseases into indicator (true/false) columns
- Bin the ages into MeSH age groups
- Mark images as either training or test

See more details about the dataset in the data folder.
'''
import pandas as pd
import os

# To read from the local directory
# This works as long as we don't make a real package out of this code
# See https://importlib-resources.readthedocs.io/en/latest/using.html
_DATA_DIR = os.path.dirname(__file__)

# Local copies of the dataset files
_DATASET = os.path.join(_DATA_DIR, 'Data_Entry_2017_v2020.csv')
_TRAIN_VAL_LIST = os.path.join(_DATA_DIR, 'train_val_list.txt')
_TEST_LIST = os.path.join(_DATA_DIR, 'test_list.txt')

# Cached preprocessed dataset
_DATASET_CACHED = os.path.join(_DATA_DIR, 'chestx-ray14-preprocessed.csv')

# Official dataset numbers and some often-used column names
_NUM_IMAGES = 112120
_NUM_PATIENTS = 30805
_PATIENT_ID = 'Patient ID'
_IMAGE_INDEX = 'Image Index'

# Columns and values we add to the dataset
_AGE_GROUP = 'Patient Age Group'
_TRAIN_TEST = 'Train/Test'
_TRAIN = 'Train'
_TEST = 'Test'
_DISEASE_COLUMN_PREFIX = 'D: '


def _verify_dataset(ds: pd.DataFrame):
    '''Checks a few basic things about the dataset before using it.

    Verifies that the dataset has the content we expect. If any of these checks fail, either the
    dataset itself has changed or we made a mistake when preprocessing it.

    If the dataset has changed, update the checks to match the new dataset.

    If the dataset has not changed, there may be a mistake in the preprocessig code.

    Args:
        ds: the dataset after it was preprocessed.
    '''

    # Number of images and patients must match the original ChestX-ray14
    assert ds.shape[0] == _NUM_IMAGES
    assert len(ds[_PATIENT_ID].unique()) == _NUM_PATIENTS

    # Number of columns must match the original 11, plus:
    #    - 15 for disease indicators (14 + 'no finding')
    #    - 1 for the age group
    #    - 1 for the train/test label
    assert ds.shape[1] == 11 + 15 + 1 + 1

    # Check if we added the new columns
    assert _AGE_GROUP in ds.columns
    assert _TRAIN_TEST in ds.columns

    # Sample some of the disease indicators
    assert _DISEASE_COLUMN_PREFIX + 'Mass' in ds.columns
    assert _DISEASE_COLUMN_PREFIX + 'No Finding' in ds.columns

    # Check the train/test column contents (two labels, adding up to the total images)
    assert len(ds[_TRAIN_TEST].unique()) == 2
    assert (len(ds[ds[_TRAIN_TEST] == _TRAIN]) + len(ds[ds[_TRAIN_TEST] == _TEST])) == _NUM_IMAGES

    # Patients must be either in the train or the test set
    train_test_count = ds[[_PATIENT_ID, _IMAGE_INDEX, _TRAIN_TEST]
                          ].groupby(['Patient ID', _TRAIN_TEST]).count().unstack()
    train_test_count.columns = train_test_count.columns.droplevel()
    train_test_count.fillna(0, inplace=True)

    assert train_test_count.shape[0] == _NUM_PATIENTS
    assert (train_test_count[_TRAIN].sum() + train_test_count[_TEST].sum()) == _NUM_IMAGES
    in_both = train_test_count[(train_test_count[_TRAIN] > 0) & (train_test_count[_TEST] > 0)]
    assert len(in_both) == 0


def get_dataset(from_cache: bool = True) -> pd.DataFrame:
    '''Reads the raw files that comprise the dataset and creates a preprocessed dataset.

    The preprocessed dataset is cached and available to be read from that cache later.

    Args:
        from_cache: load from the cached, preprocessed dataset, if available. Set to `False` to read
            from the original dataset and run the preprocessing code again.

    Returns:
        The preprocessed dataset: diseases are split into indicator (true/false) columns, ages
        are binned, and images (and thus patients) are marked as "test" or "train".
    '''
    if from_cache and os.path.isfile(_DATASET_CACHED):
        ds = pd.read_csv(_DATASET_CACHED)
        try:
            _verify_dataset(ds)
        except AssertionError:
            # If we may have a bad cached file - rebuild it
            # Rebuild may not fix it though - that indicates a bug in the code
            os.remove(_DATASET_CACHED)
            return get_dataset()
        return ds

    ds = pd.read_csv(_DATASET)

    # Split diseases into separate indicator columns
    # Add a prefix to sort them together in visualizations
    indicators = ds['Finding Labels'].str.get_dummies('|')
    indicators = indicators.add_prefix(_DISEASE_COLUMN_PREFIX)
    ds = pd.concat([ds, indicators], axis='columns')

    # Bin the ages according to MeSH age groups
    # Best reference I found for MeSH groups: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1794003/
    # We have only complete years, so we can't use 'newborn'
    # Adding the age range helps groups them together in visualizations
    # Also prefix with zero because visualizers sort by ASCII code, not numeric value
    bins = [0, 2, 6, 13, 19, 45, 65, 80, 120]
    ages = ['(0-1) Infant', '(02-5) Preschool', '(06-12) Child', '(13-18) Adolescent',
            '(19-44) Adult', '(45-64) Middle age', '(65-79) Aged', '(80+) Aged 80']
    ds[_AGE_GROUP] = pd.cut(ds['Patient Age'], bins=bins, labels=ages, right=False)

    # Add train/test column for the images
    train = pd.read_csv(_TRAIN_VAL_LIST, header=None)
    test = pd.read_csv(_TEST_LIST, header=None)

    # Use sets for faster membership test
    train_set = set(train[0])
    test_set = set(test[0])

    # Check that we have the correct number of train/test instances and no overlap
    assert (len(train_set) + len(test_set)) == _NUM_IMAGES
    assert len(train_set & test_set) == 0

    ds[_TRAIN_TEST] = ds.apply(lambda r: _TRAIN if r[_IMAGE_INDEX]
                               in train_set else _TEST, axis='columns')

    # Rename some columns to fix the comma in their names
    ds = ds.rename(columns={'OriginalImage[Width': 'Original Width', 'Height]': 'Original Height',
                            'OriginalImagePixelSpacing[x': 'Original Spacing X',
                            'y]': 'Original Spacing Y'})

    _verify_dataset(ds)

    ds.to_csv(_DATASET_CACHED, index=False)
    return ds


def reduce_size(ds: pd.DataFrame, remove_indicators: bool = True) -> pd.DataFrame:
    '''Reduces the size of the dataframe by dropping some columns.

    Some visualizers, most notably Google Facets in a Jupter Notebook, a large amount of data in the
    dataset makes the visualization sluggish. Reducing the size of the dataframe helps with
    responsiveness (with the downside of fewer pieces of data, of course).

    Args:
        ds: The dataset to be reduced.
        remove_indicators: True to remove the disease indicator columns, of False to leave them in.

    Returns:
        A dataset with fewer columnns.
    '''

    # Drop the disease indicators columns
    if remove_indicators:
        indicators = [d for d in ds.columns if d.startswith(_DISEASE_COLUMN_PREFIX)]
        ds.drop(columns=indicators, inplace=True)

    # Drop original size and pixel spacing
    original = [d for d in ds.columns if d.startswith('Original')]
    ds.drop(columns=original, inplace=True)

    return ds


# To allow standalone execution for tests
if __name__ == "__main__":
    dataset = get_dataset()
    dataset = reduce_size(dataset)
    print(dataset)
