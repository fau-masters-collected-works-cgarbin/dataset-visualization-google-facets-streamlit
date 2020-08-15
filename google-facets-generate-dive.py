'''Generates the HTML page for the Google Facets Dive for ChestX-ray14.

See the "Dive" section in https://pair-code.github.io/facets/.

Based on https://github.com/PAIR-code/facets/blob/master/facets_dive/Dive_demo.ipynb.

Note that the dataset is embedded in the HTML in JSON format. An improvement would be to embbed it
in CSV format and convert to JSON when the page is loaded.
'''

import dataset


def get_sprite_size(dataset_rows: int) -> int:
    '''Sets the sprite_size based on the number of records in dataset.

    Larger datasets can crash the browser if the size is too large (>50000).

    Args:
        dataset_rows: The number of rows in the dataset.

    Returns:
        The sprite size, adjusted for the dataset size.
    '''
    if dataset_rows > 100000:
        return 16
    else:
        return 32 if dataset_rows > 50000 else 64


if __name__ == "__main__":
    ds = dataset.get_dataset()
    ds = dataset.reduce_size(ds, remove_indicators=False)

    jsonstr = ds.to_json(orient='records')

    sprite_size = get_sprite_size(len(ds.index))

    HTML_TEMPLATE = (
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/webcomponentsjs/1.3.3/webcomponents-lite.js"></script>'  # noqa
        '<link rel="import" href="https://raw.githubusercontent.com/PAIR-code/facets/1.0.0/facets-dist/facets-jupyter.html">'  # noqa
        '<facets-dive sprite-image-width="{sprite_size}" sprite-image-height="{sprite_size}" id="elem"></facets-dive>'  # noqa
        '<script>'
        '   var data = {jsonstr};'
        '   document.querySelector("#elem").data = data;'
        '</script>')

    html = HTML_TEMPLATE.format(jsonstr=jsonstr, sprite_size=sprite_size)

    FILE = 'google-facets-dive.html'
    with open(FILE, 'w') as file:
        print(html, file=file)

    print('Open {} in a Chrome browser (must be Chrome)'.format(FILE))
    print('It will take a few seconds to load')
