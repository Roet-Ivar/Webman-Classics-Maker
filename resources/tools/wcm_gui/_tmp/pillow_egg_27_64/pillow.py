import os
import sys

DIR = os.path.dirname(__file__)
pillow_dir = 'Pillow-5.4.1-py2.7-win-amd64.egg'

print('DIR: ' + DIR)
print('pillow_dir: ' + pillow_dir)
sys.path.append(os.path.join(DIR, pillow_dir))

from PIL import Image
from PIL import ImageTk
from PIL.ImageTk import PhotoImage