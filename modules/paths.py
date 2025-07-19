import os

dir = os.path.dirname(__file__)
out_dir = os.path.dirname(dir)
path_AIMP = os.path.join(out_dir, "AIMP")

PATHS = {
    'download_folder' : path_AIMP,
}