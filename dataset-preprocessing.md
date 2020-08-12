# Dataset preprocessing

The [ChestX-ray8 (a.k.a. ChestX-ray14) dataset](https://arxiv.org/abs/1705.02315) dataset needs to
be preprocessed to be visualized:

1. The diseases are stored in one column, separated by |. We will split them into separate columns.
   Theere will be one column for each diseases, with true/false indicating presence/absence (i.e.
   diseases will be _one-hot encoded_).
1. It is useful to inspect age groups, but age is stored as full years. We will add a column to
   group age ranges (i.e. age will be _binned_).
