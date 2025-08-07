import os

CURRENT_PATH = os.path.dirname(__file__)
OUT_DIR = os.path.dirname(CURRENT_PATH)
PATH_AIMP = os.path.join(OUT_DIR, "AIMP")
PATHS = {
    'download_folder' : PATH_AIMP,
    'original_folder' : PATH_AIMP
}

SEPARATOR = '__'