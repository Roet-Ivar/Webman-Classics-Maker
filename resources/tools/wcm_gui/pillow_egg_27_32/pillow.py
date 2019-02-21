import os
import sys

DIR = os.path.dirname(__file__)
print('DIR: ' + DIR)
pillow_dir = 'Pillow-5.4.1-py2.7-win32.egg'

print('pillow_dir: ' + pillow_dir)
sys.path.append(os.path.join(DIR, pillow_dir))

from PIL import Image
from PIL import ImageTk