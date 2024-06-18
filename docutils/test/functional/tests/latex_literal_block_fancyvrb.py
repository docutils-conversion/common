# Source and destination file names
test_source = "latex_literal_block.txt"
test_destination = "latex_literal_block_fancyvrb.tex"

# Keyword parameters passed to publish_file()
writer = "latex"
settings_overrides = {
    'stylesheet': 'docutils',
    'legacy_column_widths': True,
    'use_latex_citations': False,
    'literal_block_env': 'Verbatim',
    }
