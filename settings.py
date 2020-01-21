import os

from entities import Size, Color

NASA_API_KEY = os.environ['NASA_API_KEY']
TOKEN_FIREBOT = os.environ["TOKEN_FIREBOT"]
ASSETS_PATH = os.environ["ASSETS_PATH"]
DEBUG_PICS_PATH = os.environ["DEBUG_PICS_PATH"]


DISPLAY_SIZE = Size(512, 512)
MAX_CLOUD_SCORE = 0.5
BLACK = Color(0, 0, 0)
LON = -120.70418
LAT = 38.32974
