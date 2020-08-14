'''Preprocess the dataset

- Separate the diseases into indicator (true/false) columns
- Bin the ages into MeSH age groups
- Mark images as either training or test

See more details about the dataset in the data folder.
'''
import pandas as pd

# Local copies of the dataset files
_DATASET = 'data/Data_Entry_2017_v2020.csv'
_TRAIN_VAL_LIST = 'data/train_val_list.txt'
_TEST_LIST = 'data/test_list.txt'

# Official dataset numbers and some often-used column names
_NUM_IMAGES = 112120
_NUM_PATIENTS = 30805
_PATIENT_ID = 'Patient ID'
_IMAGE_INDEX = 'Image Index'

# Columns and values we add to the dataset
_AGE_GROUP = 'Age Group'
_TRAIN_TEST = 'Train/Test'
_TRAIN = 'Train'
_TEST = 'Test'


def _verify_dataset(ds: pd.DataFrame):
    '''Checks a few basic things about the dataset before using it.

    Verifies that the dataset has the content we expect. If any of these checks fail, either the
    dataset itself has changed or we made a mistake when preprocessing it.

    If the dataset has changed, upddate the checks to match the new dataset.

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

    # Check if we added the new data as expected (check a few disease indicators and age group)
    assert _AGE_GROUP in ds.columns
    assert _TRAIN_TEST in ds.columns
    assert 'Mass' in ds.columns
    assert 'No Finding' in ds.columns

    # Check the train/test split
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


def get_dataset() -> pd.DataFrame:
    '''Reads the raw files that comprise the dataset and creates a preprocessed dataset.

    Returns:
        The preprocessed dataset: diseases are split into indicator (true/false) columns, ages
        are binned, and images (and thus patients) are marked as "test" or "train".
    '''

    ds = pd.read_csv(_DATASET)

    # Split diseases into separate indicator columns
    indicators = ds['Finding Labels'].str.get_dummies('|')
    ds = pd.concat([ds, indicators], axis='columns')

    # Bin the ages according to MeSH age groups
    # Best reference I found for MeSH groups: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1794003/
    # We have only complete years, so we can't use 'newborn'
    bins = [0, 2, 6, 13, 19, 45, 65, 80, 120]
    ages = ['Infant', 'Preschool', 'Child', 'Adolescent', 'Adult', 'Middle age', 'Aged', 'Aged 80']
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

    _verify_dataset(ds)
    return ds


# To allow standalone execution for tests
if __name__ == "__main__":
    dataset = get_dataset()
    print(dataset)
