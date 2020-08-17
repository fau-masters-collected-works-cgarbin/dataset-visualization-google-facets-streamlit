# Dataset copy

This folder contains a copy of the dataset files. The original repository for the dataset is this
[folder in the NIH](https://nihcc.app.box.com/v/ChestXray-NIHCC).

This copy is used to make the experiments reproducible. The NIH folder is not under version control,
so we are not able to retrieve a specific version of the dataset. To get around that, we keep this
local copy.

At the time this folder was created, the timestamp of the files in the NIH folder are:

- Data_Entry_2017_v2020.csv: April 15th, 2020
- train_val_list.txt: December 14th, 2017
- test_list.txt: December 14th, 2017

The folder also contains the code to preprocess the dataset and the cached copy of the
preprocessed dataset.

See more details about the dataset and the preprocessing [here](../dataset.md).
