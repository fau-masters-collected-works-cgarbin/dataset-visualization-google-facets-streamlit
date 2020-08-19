'''Visualizes the ChestX-ray14 dataset with Streamlit (https://www.streamlit.io/).
'''
import streamlit as st
import seaborn as sns
import matplotlib.ticker as mtick
# Works as long as it's not in a package  - https://stackoverflow.com/a/27876800
import sys
sys.path.append('..')
from data import dataset as ds  # noqa

sns.set_style("whitegrid")

df = ds.reduce_size(ds.get_dataset(), remove_indicators=False)

columns = [ds.PATIENT_GENDER_COL, ds.PATIENT_AGE_GROUP_COL, ds.TRAIN_TEST_COL]

all_diseases = ds.get_disease_names(df, remove_prefix=True)

disease = st.selectbox('Disease to inspect', all_diseases, index=0)
percent = st.checkbox('Percentages of total images')
same_scale = st.checkbox('Use same scale')


@st.cache
def all_diseases():
    tmp = df.groupby(columns).count().reset_index()
    if percent:
        tmp['Image Index'] = tmp['Image Index'] / ds.NUM_IMAGES * 100
    return tmp


def get_aggregated_data(disease):
    _df = df[df[ds.DISEASE_COLUMN_PREFIX + disease] == 1]
    tmp = _df.groupby(columns).count().reset_index()
    if percent:
        tmp['Image Index'] = tmp['Image Index'] / ds.NUM_IMAGES * 100
    return tmp


@st.cache
def get_max_images():
    return df.groupby(columns).count().reset_index()['Image Index'].max()


def plot_graph(df, row, col, hue):
    g = sns.catplot(x=row, y='Image Index', hue=hue, data=df, col=col, kind='bar',
                    col_wrap=2, palette=['blue', 'red'])
    g.set(ylabel='Number of Images')
    g.set_xticklabels(rotation=60)
    if same_scale:
        g.set(ylim=(0, 100) if percent else(0, get_max_images()))
    if percent:
        for ax in g.axes.flat:
            ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    sns.despine(left=True)
    st.pyplot()


df_agg_disease = get_aggregated_data(disease)
header = f'# {disease} by gender and age group'
st.markdown(header)
plot_graph(df_agg_disease, ds.PATIENT_AGE_GROUP_COL, ds.PATIENT_GENDER_COL, ds.TRAIN_TEST_COL)

st.markdown('# All diseases by gender and age group')
plot_graph(all_diseases(), ds.PATIENT_AGE_GROUP_COL, ds.PATIENT_GENDER_COL, ds.TRAIN_TEST_COL)
