'''Generates the HTML page for the Google Facets Overview for ChestX-ray14.

See the "Overview" section in https://pair-code.github.io/facets/.

Based on https://github.com/PAIR-code/facets/blob/master/facets_overview/Overview_demo.ipynb.

Note that the statistics are embedded in the HTML in BASE64 format.
'''
from facets_overview.generic_feature_statistics_generator import GenericFeatureStatisticsGenerator
import base64

# Works as long as it's not in a package  - https://stackoverflow.com/a/27876800
import sys
sys.path.append('..')
from data import dataset  # noqa


if __name__ == "__main__":
    ds = dataset.get_dataset()
    ds = dataset.reduce_size(ds, remove_indicators=False)

    gfsg = GenericFeatureStatisticsGenerator()
    proto = gfsg.ProtoFromDataFrames([{'name': 'ChestX-ray14', 'table': ds}])
    protostr = base64.b64encode(proto.SerializeToString()).decode('utf-8')

    HTML_TEMPLATE = (
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/webcomponentsjs/1.3.3/webcomponents-lite.js"></script>'  # noqa
        '<link rel="import" href="https://raw.githubusercontent.com/PAIR-code/facets/1.0.0/facets-dist/facets-jupyter.html">'  # noqa
        '<facets-overview id="elem"></facets-overview>'
        '<script>'
        '   document.querySelector("#elem").protoInput = "{protostr}";'
        '</script>')

    html = HTML_TEMPLATE.format(protostr=protostr)

    FILE = 'google-facets-overview.html'
    with open(FILE, 'w') as file:
        print(html, file=file)

    print('Open {} in a Chrome browser (must be Chrome)'.format(FILE))
    print('It will take a many seconds to load')
