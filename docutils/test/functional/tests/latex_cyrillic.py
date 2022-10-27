# Default settings for all tests.

settings_overrides = {
    '_disable_config': True,
    'report_level': 2,
    'halt_level': 5,
    'warning_stream': '',
    'input_encoding': 'utf-8',
    'embed_stylesheet': False,
    'auto_id_prefix': '%',
    # avoid "Pygments not found"
    'syntax_highlight': 'none'
}

# Source and destination file names.
test_source = "cyrillic.txt"
test_destination = "cyrillic.tex"

# Keyword parameters passed to publish_file.
reader_name = "standalone"
parser_name = "rst"
writer_name = "latex"

# Extra setting we need

settings_overrides['font_encoding'] = 'T1,T2A'
settings_overrides['stylesheet'] = 'cmlgc'
settings_overrides['language_code'] = 'ru'

settings_overrides['smart_quotes'] = True
settings_overrides['legacy_column_widths'] = False
settings_overrides['use_latex_citations'] = True
