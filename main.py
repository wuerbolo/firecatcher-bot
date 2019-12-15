from nasa import earth
from typing import NamedTuple, Any
from tqdm import tqdm
from PyInquirer import prompt
import pendulum
import pygame
import os


os.environ.setdefault(
    'NASA_API_KEY',
    '***REMOVED***',
)


class Size(NamedTuple):
    """
    Represents a size
    """

    width: int
    height: int


class Color(NamedTuple):
    """
    8-bit components of a color
    """

    r: int
    g: int
    b: int


class Shot(NamedTuple):
    """
    Represents a shot from Landsat. The asset is the output of the listing
    and the image contains details about the actual image.
    """

    asset: Any
    image: Any


DISPLAY_SIZE = Size(512, 512)
BLACK = Color(0, 0, 0)
MAX_CLOUD_SCORE = 0.5

LON = -120.70418
LAT = 38.32974


def bisect(n, mapper, tester):
    """
    Runs a bisection.

    - `n` is the number of elements to be bisected
    - `mapper` is a callable that will transform an integer from "0" to "n"
      into a value that can be tested
    - `tester` returns true if the value is within the "right" range
    """

    if n < 1:
        raise ValueError('Cannot bissect an empty array')

    left = 0
    right = n - 1

    while left + 1 < right:
        mid = int((left + right) / 2)

        val = mapper(mid)

        if tester(val):
            right = mid
        else:
            left = mid

    return mapper(right)


class LandsatImage:
    """
    Utility class to manage the display of a landsat image using
    pygame.
    """

    def __init__(self):
        self.image = None
        self._shot = None

    @property
    def shot(self):
        return self._shot

    @shot.setter
    def shot(self, value):
        self._shot = value
        self.image = None

    def blit(self, disp):
        if not self.image:
            img = self.shot.image
            pil_img = img.image
            buf = pil_img.tobytes()
            size = pil_img.width, pil_img.height
            self.image = pygame.image.frombuffer(buf, size, 'RGB')

        disp.blit(self.image, (0, 0))


class LandsatBisector:
    """
    Manages the different assets from landsat to facilitate the bisection
    algorithm.
    """

    def __init__(self, lon, lat):
        self.lon, self.lat = lon, lat
        self.shots = self.get_shots()
        self.image = LandsatImage()
        self.index = 0

        print(f'First = {self.shots[0].asset.date}')
        print(f'Last = {self.shots[-1].asset.date}')
        print(f'Count = {len(self.shots)}')

    @property
    def count(self):
        return len(self.shots)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self.image.shot = self.shots[index]
        self._index = index

    @property
    def date(self):
        return self.shots[self.index].asset.date

    def get_shots(self):
        """
        Not all returned assets are useful (some have clouds). This function
        does some filtering in order to remove those useless assets and returns
        pre-computed shots which can be used more easily.
        """

        begin = '2000-01-01'
        end = pendulum.now('UTC').date().isoformat()

        assets = earth.assets(lat=self.lat, lon=self.lon, begin=begin, end=end)

        out = []

        for asset in tqdm(assets):
            img = asset.get_asset_image(cloud_score=True)

            if (img.cloud_score or 1.0) <= MAX_CLOUD_SCORE:
                out.append(Shot(asset, img))

        return out

    def blit(self, disp):
        """
        Draws the current picture.
        """

        self.image.blit(disp)


def confirm(title):
    """
    Asks a yes/no question to the user
    """

    return prompt([{
        'type': 'confirm',
        'name': 'confirm',
        'message': f'{title} - do you see it?',
    }])['confirm']


def main():
    """
    Runs a bisection algorithm on a series of Landsat pictures in order
    for the user to find the approximative date of the fire.

    Images are displayed using pygame, but the interactivity happens in
    the terminal as it is much easier to do.
    """

    pygame.init()

    bisector = LandsatBisector(LON, LAT)
    disp = pygame.display.set_mode(DISPLAY_SIZE)

    def mapper(n):
        """
        In that case there is no need to map (or rather, the mapping
        is done visually by the user)
        """

        return n

    def tester(n):
        """
        Displays the current candidate to the user and asks them to
        check if they see wildfire damages.
        """

        bisector.index = n
        disp.fill(BLACK)
        bisector.blit(disp)
        pygame.display.update()

        return confirm(bisector.date)

    culprit = bisect(bisector.count, mapper, tester)
    bisector.index = culprit

    print(f"Found! First apparition = {bisector.date}")

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()
