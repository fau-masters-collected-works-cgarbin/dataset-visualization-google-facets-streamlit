# Streamlit

If you haven't done so yet, review the details of the [dataset we are using](../dataset.md).

[Streamlit](https://www.streamlit.io/) does more than visualization. It can also run models. We will
concentrate on the visualization part here.

Unlike [Google Facets](../google-facets/README.md), it requires coding. On the other hand, it
is more powerful and flexible.

For example, we can add more specific filters and transformations. In the example developed here, we
can select a specific disease and show it in percentages of the total images.

In the image below, the user interface controls to filter the data are provided by Streamlit. As
the values change, Streamlit runs the code with the new values to update the visualization. This
allows you to concentrate on writing the code that filters the data and creates the visualization.

The caption for each section (e.g. "All diseases by gender and age group") is created with markdown.
Combining markdown with code is used to create more complex visualizations and explanations.

![Streamlit example](./pics/streamlit-example.png)

[How to explore the visualizations](../README.md#if-you-want-to-explore-the-visualizations).
