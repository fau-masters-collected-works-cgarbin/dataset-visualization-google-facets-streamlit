# Dataset

We will explored the ChestX-ray8 (a.k.a. ChestX-ray14) dataset from the National Institutes of
Health. It is explained [in this paper](https://arxiv.org/abs/1705.02315) and stored
[here](https://nihcc.app.box.com/v/ChestXray-NIHCC).

The dataset is a collection of frontal x-ray images for patients of hte National Institutes of
Health Clinical Center. A patient may have multiple images, taken over several visits to the center.
Each image is annotated with the diseases the image may indicate. The diseases where extracted from
the image reports with natural langugage processing (NLP).
[The paper](https://arxiv.org/abs/1705.02315) describes the extraction process in details.

The dataset has the following information for each patient:

- File name: the complete name of the image file, including the extension. The name of the file encodes the patient ID. For example, the file 00000003_000.png is an image for the patient ID 3.
- Finding labels: a list of diseases labels extracted from the radiological report.
- Follow-up #: the follow-up sequence number.
- Patient ID: a number that uniquely identifies a patient. It is a sequential number that does not encode any other information.
- Patient age: patient age in years at the time the image was taken.
- Patient gender: biological gender (male or female) of the patient.
- View position: either PA (posterioranterior) or AP (anteriorposterior).
- Original image width: the width of the original image in DICOM in pixels.
- Original image height: the height of the original image in DICOM in pixels.
- Original image pixel spacing X: original image column spacing from DICOM.
- Original image pixel spacing Y: original image row spacing from DICOM.

In addition to that, it also has a documented split for trainig and test sets. Patients are either
the training of the test set.

## Retrieving the dataset

The dataset is available [in this NIH site](https://nihcc.app.box.com/v/ChestXray-NIHCC). It may be
updated from time to time. To make this experiment reproducible, we stored a copy of the current
version with this repository. See details of the local copy [here](./data/README.md).

## Preprocessing the dataset

The [ChestX-ray8 (a.k.a. ChestX-ray14) dataset](https://arxiv.org/abs/1705.02315) dataset needs to
be preprocessed to be visualized:

1. The diseases are stored in one column, separated by |. We will split them into separate columns.
   Theere will be one column for each diseases, with true/false indicating presence/absence (i.e.
   diseases will be _one-hot encoded_).
1. It is useful to inspect age groups, but age is stored as full years. We will add a column to
   group age ranges (i.e. age will be _binned_).
1. Some images are meant to be used for training and some for test, but this is not indicated in the
   dataset. There is a separate list of training images. We will add a column to indicate of an
   image is supposed to be used for training or for test.
