import os

for path, directories, file_names in os.walk("~/..password-store/", followlinks=True):
    print()