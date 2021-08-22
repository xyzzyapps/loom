project = 'Loom'
copyright = '2021, Xyzzy Apps'
author = 'Xyzzy'
release = '2021'
extensions = ['myst_parser', 'sphinx.ext.todo']
html_baseurl = "https://xyzzyapps.github.io/loom/"

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'

html_static_path = ['_static']
html_js_files = [
        'analytics.js',
        ('https://analytics.xyzzyapps.link/count.js', {'data-goatcounter': "https://analytics.xyzzyapps.link/count", 'async': "async"}),
    ]
