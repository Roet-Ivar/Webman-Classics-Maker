import os
import sys

DIR = os.path.dirname(__file__)
pillow_dir = 'Pillow-5.4.1-py3.7-win32.egg'

print('DIR: ' + DIR)
print('pillow_dir: ' + pillow_dir)
sys.path.append(os.path.join(DIR, pillow_dir))

from PIL import Image
from PIL.ImageTk import PhotoImage
from PIL import ImageTk
