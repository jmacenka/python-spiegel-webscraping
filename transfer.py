import os
from shutil import move

from_dir = '/var/lib/docker/volumes/webscraping/_data'
to_dir = 'files'

to_dir_abs = os.path.join(os.getcwd(),to_dir)

print(to_dir_abs)

if not os.path.exists(to_dir_abs):
    os.makedirs(to_dir_abs)

all_files = [f for f in os.listdir(from_dir) if 'html' in f]

for f in all_files:
    from_path = os.path.join(from_dir,f)
    to_path = os.path.join(to_dir_abs,f)
    move(from_path,to_path)
    print(f'Copied: {f}')

print('\nAll Done')
