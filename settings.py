import os

from entities import Size, Color

os.environ.setdefault(
    'NASA_API_KEY',
    '***REMOVED***',
)


DISPLAY_SIZE = Size(512, 512)
MAX_CLOUD_SCORE = 0.5
BLACK = Color(0, 0, 0)
LON = -120.70418
LAT = 38.32974
