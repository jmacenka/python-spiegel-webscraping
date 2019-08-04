import os
from shutil import copyfile

from_dir = '/var/lib/docker/volumes/webscraping/_data'
to_dir = '/files'

to_dir_abs = os.path.abspath(to_dir)

if not os.path.exists(to_dir_abs):
    os.mkdirs(to_dir_abs)

all_files = [f for f in os.listdir(from_dir) if 'html' in f]

for f in all_files:
    from_path = os.path.join(from_dir,f)
    copyfile(from_path,to_dir_abs)
    print(f'Copied: {f}')

print('\nAll Done')
