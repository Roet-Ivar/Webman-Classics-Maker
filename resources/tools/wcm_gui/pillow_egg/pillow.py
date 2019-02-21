import os
import sys

DIR = os.path.dirname(__file__)
print('DIR: ' + DIR)
if sys.version_info[0] < 3:
    pillow_dir = 'Pillow_2.7_x86/Pillow-5.4.1-py2.7-win32.egg'
else:
    pillow_dir = 'Pillow_3.7_x86/Pillow-5.4.1-py3.7-win32.egg'
print('pillow_dir: ' + pillow_dir)
sys.path.append(os.path.join(DIR, pillow_dir))

from PIL import Image
from PIL import ImageTk