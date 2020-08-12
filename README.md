# Dataset visualization with Facets and Streamlit

Explore dataset visualization with [Google Facets](https://pair-code.github.io/facets/) and
[Streamlit](https://www.streamlit.io/).

We use these visualization tools to explore the characteristics of the patients in the
[ChestX-ray8 (a.k.a. ChestX-ray14) dataset](https://arxiv.org/abs/1705.02315) available
[here](https://nihcc.app.box.com/v/ChestXray-NIHCC):

For this analysis we are interested in the characteristics of the patients, not the images. We want
to understand the representativeness of the dataset across genres and ages. We will explore
questions such as:

- What is the overall genre distribution?
- What is the distribution of diseases across the genres?
- What is the distribution of diseases across the ages? Across age groups?
- Is the disease distribution the same in the training and test sets?
- Is the disease distribution the same across genres and ages in the training and test sets?
- What diseases coccur in the same image?

## Google Facets

[Google Facets](https://pair-code.github.io/facets/) was created to explore data with machine
learning in mind. It has two visualization modes (quotes from its website):

- [Overview](https://github.com/PAIR-code/facets#facets-overview): _quick understanding of the
  distribution of values across the features of their dataset(s). Uncover several uncommon and
  common issues such as unexpected feature values, missing feature values for a large number of
  observation, training/serving skew and train/test/validation set skew._
- [Dive](https://github.com/PAIR-code/facets#facets-dive): _an interactive interface for exploring
  the relationship between data points across all of the different features of a dataset. Each
  individual item in the visualization represents a data point. Position items by "faceting" or
  bucketing them in multiple dimensions by their feature values._

Note the disclaimer that this is not a Google product. It was developed and released as part of
their work [PAIR (people + AI research)](https://pair.withgoogle.com/) with the machine learning
community.

See Google Facets is used to explore the dataset [in this file](./google-facets.md).

## Streamlit

[Streamlit](https://www.streamlit.io/) is a general-purpose, interactive visualization framework.
