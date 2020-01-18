import pendulum
from nasa import earth
from tqdm import tqdm

from entities import Shot
from settings import MAX_CLOUD_SCORE

from os import listdir
from os.path import isfile, join
import pickle


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
    
    @staticmethod
    def save_asset(asset, number):
       
        path_asset = 'F:/development/repos/firecatcher-bot/assets/'
        with open(join(path_asset, 'asset_{}'.format(number)), 'wb') as asset_file:
            pickle.dump(asset, asset_file)

    @staticmethod
    def load_asset(asset_file, asset_path='F:/development/repos/firecatcher-bot/assets/'):
        with open(join(asset_path, asset_file), 'rb') as asset_file:
            return pickle.load(asset_file)

    def load_pics_assets(self, pics_path):

        file_imgs = [f for f in listdir(pics_path) if isfile(join(pics_path, f))]
        out = []
        
        for file_img in file_imgs:
            asset_file = 'asset_{0}'.format(file_img[4:-4])
            asset = self.load_asset(asset_file)
            out.append(Shot(asset,open(join(pics_path, file_img), 'rb')))

        return out

    def get_shots(self, download=False):
        """
        Not all returned assets are useful (some have clouds). This function
        does some filtering in order to remove those useless assets and returns
        pre-computed shots which can be used more easily.
        """

        debug_pics_path = 'F:/development/repos/firecatcher-bot/debug_pics/'
        last_image_path = join(debug_pics_path, 'img_181.png')

        if isfile(last_image_path) and not download:
            print ("Images found")
            return self.load_pics_assets(debug_pics_path)
        
        begin = '2000-01-01'
        end = pendulum.now('UTC').date().isoformat()

        assets = earth.assets(lat=self.lat, lon=self.lon, begin=begin, end=end)

        out = []

        for num, asset in tqdm(enumerate(assets, start=1)):
            img = asset.get_asset_image(cloud_score=True)

            if (img.cloud_score or 1.0) <= MAX_CLOUD_SCORE:
                out.append(Shot(asset, img))
                path = 'F:/development/repos/firecatcher-bot/debug_pics/img_{}.png'.format(str(num))
                img.image.save(path, 'PNG')
                self.save_asset(asset, num)

        return out