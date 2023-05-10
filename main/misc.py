import os


SOFTWARE_DIR_PTH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOFTWARE_NAME = os.path.basename(SOFTWARE_DIR_PTH)
SOFTWARE_VER = '1.0.1'

SAVED_NETWORK_DIR_PTH = os.path.join(SOFTWARE_DIR_PTH, 'saved_network')

THEME_BACKGROUND = '#101110'
THEME_BORDER_COLOR = '#dcdddc'
THEME_FONT_COLOR = '#fafbfa'