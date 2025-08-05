import os

current_path = os.path.dirname(__file__)
out_dir = os.path.dirname(current_path)
path_AIMP = os.path.join(out_dir, "AIMP")

PATHS = {
    'download_folder' : path_AIMP,
    'original_folder' : path_AIMP
}