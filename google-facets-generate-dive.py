'''Generates the HTML page for the Google Facets Dive for ChestX-ray14.

See the "Dive" section in https://pair-code.github.io/facets/.

Based on https://github.com/PAIR-code/facets/blob/master/facets_dive/Dive_demo.ipynb.

Note that the dataset is embedded in the HTML in JSON format. Converting from CSV to JSON at runtime
took too long (Chrome showed the 'page unresponsive' alert). A simple-minded optimization is to
replace some of the most common substrings with a short version, as the code does now. That
reduces the size from 54 MB to about 17 MB.
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

    # Replace some common findings combinations with a shorter version

    compress = [
        # Most common finding: no finding
        ('"D: Atelectasis":0,"D: Cardiomegaly":0,"D: Consolidation":0,"D: Edema":0,"D: Effusion":0,"D: Emphysema":0,"D: Fibrosis":0,"D: Hernia":0,"D: Infiltration":0,"D: Mass":0,"D: No Finding":1,"D: Nodule":0,"D: Pleural_Thickening":0,"D: Pneumonia":0,"D: Pneumothorax":0',  # noqa
            '_NF'),
        (',"Finding Labels":"No Finding",', '_LNF'),

        # Second most common finding: infiltration and no other finding
        ('"D: Atelectasis":0,"D: Cardiomegaly":0,"D: Consolidation":0,"D: Edema":0,"D: Effusion":0,"D: Emphysema":0,"D: Fibrosis":0,"D: Hernia":0,"D: Infiltration":1,"D: Mass":0,"D: No Finding":0,"D: Nodule":0,"D: Pleural_Thickening":0,"D: Pneumonia":0,"D: Pneumothorax":0',  # noqa
            '_INF'),

        # Third most common finding: effusion and no other finding
        ('"D: Atelectasis":0,"D: Cardiomegaly":0,"D: Consolidation":0,"D: Edema":0,"D: Effusion":1,"D: Emphysema":0,"D: Fibrosis":0,"D: Hernia":0,"D: Infiltration":0,"D: Mass":0,"D: No Finding":0,"D: Nodule":0,"D: Pleural_Thickening":0,"D: Pneumonia":0,"D: Pneumothorax":0',  # noqa
            '_EFF'),

        # Columns with well-defined values
        ('"Train\\/Test":"Train"},{', '_Tr'), (',"Train\\/Test":"Test"},{', '_Tt'),
        ('"Patient Age Group":"(45-64) Middle age"', '_MA'),
        ('"Patient Age Group":"(65-79) Aged"', '_AG'),

        # Diseases
        ('Atelectasis', '_d1'), ('Cardiomegaly', '_d2'), ('Consolidation', '_d3'), ('Edema', '_d4'),
        ('Effusion', '_d5'), ('Emphysema', '_d6'), ('Fibrosis', '_d7'), ('Hernia', '_d8'),
        ('Infiltration', '_d9'), ('Mass', '_da'), ('No Finding', '_db'), ('Nodule', '_dc'),
        ('Pleural_Thickening', '_dd'), ('Pneumonia', '_de'), ('Pneumothorax', '_df'),

        # All other headers
        ('Image Index', '_h1'), ('Finding Labels', '_h2'), ('Follow-up #', '_h3'),
        ('Patient ID', '_h4'), ('Patient Age', '_h5'), ('Patient Gender', '_h6'),
        ('View Position', '_h7'), ('Patient Age Group', '_h8'),
    ]

    jsmap = ''
    jsregex = ''
    for i, e in enumerate(compress):
        jsonstr = jsonstr.replace(e[0], e[1])
        jsmap = jsmap + '{} {}:`{}`'.format(',' if i > 0 else '', e[1], e[0])
        jsregex = jsregex + '{}{}'.format('|' if i > 0 else '', e[1])

    sprite_size = get_sprite_size(len(ds.index))

    HTML_TEMPLATE = (
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/webcomponentsjs/1.3.3/webcomponents-lite.js"></script>\n'  # noqa
        '<link rel="import" href="https://raw.githubusercontent.com/PAIR-code/facets/1.0.0/facets-dist/facets-jupyter.html">\n'  # noqa
        '<facets-dive sprite-image-width="{sprite_size}" sprite-image-height="{sprite_size}" id="elem"></facets-dive>\n'  # noqa
        '<script>\n'
        '   var data_as_string = `{jsonstr}`;\n'
        '   const mapObj = {{ {jsmap} }};\n'
        '   data_as_string = data_as_string.replace(/{jsregex}/g, function(m){{ return mapObj[m] }});\n'  # noqa
        '   data_json = JSON.parse(data_as_string);\n'
        '   data_as_string = null;\n'
        '   document.querySelector("#elem").data = data_json;\n'
        '</script>')

    html = HTML_TEMPLATE.format(jsonstr=jsonstr, sprite_size=sprite_size,
                                jsmap=jsmap, jsregex=jsregex)

    FILE = 'google-facets-dive.html'
    with open(FILE, 'w') as file:
        print(html, file=file)

    print('Open {} in a Chrome browser (must be Chrome)'.format(FILE))
    print('It will take a few seconds to load')
