# Dataset visualization with Facets and Streamlit

Explore dataset visualization with [Google Facets](./google-facets/README.md) and
[Streamlit](./streamlit/README.md).

We use these visualization tools to explore the characteristics of the patients in the
[ChestX-ray8 (a.k.a. ChestX-ray14) dataset](https://arxiv.org/abs/1705.02315) available
[here](https://nihcc.app.box.com/v/ChestXray-NIHCC).

For this analysis we are interested in the characteristics of the patients, not the images. We want
to understand the representativeness of the dataset across genres and ages. We will explore
questions such as:

- What is the overall genre distribution?
- What is the distribution of diseases across the genres?
- What is the distribution of diseases across the ages? Across age groups?
- Is the disease distribution the same in the training and test sets?
- Is the disease distribution the same across genres and ages in the training and test sets?
- What diseases coccur in the same image?

## If you want to explore the visualizations

Clone this repository, then:

### Google Facets visualization quick guide

Note that Google Facets works only with Chrome.

- Google Facets Dive: open Chrome, then choose _Open File..._ in the _File_ and open the file
    `google-facets/google-facets-dive.html`.
- Google Facets Overview: open Chrome, then choose _Open File..._ in the _File_ and open the file
    `google-facets/google-facets-overview.html`.

### Streamlit visualization quick guide

- Set up the environment as explained [here](#if-you-want-to-change-the-code).
- `cd streamlit`
- `streamlit run streamlit-viz.py`

The dataset is fairly large. It may take several seconds to show the page.

## If you want to change the code

These are the quick instructions to work with the code for the visualizations.

- Install Python 3
- Clone this repository
- Go into the repository directory
- Create a Python [environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment):
  `python3 -m venv env`
- Activate the environmnet: `source env/bin/activate` (Linux/Mac) or `.\env\Scripts\activate` (Windows)
- Install the Python packages: `pip install -r requirements.txt`

## Google Facets

See how Google Facets is used to explore the dataset [in this file](./google-facets/README.md).

## Streamlit

See how Streamlit is used to explore the dataset [in this file](./streamlit/README.md).
