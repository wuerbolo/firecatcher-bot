from PyInquirer import prompt
import pygame

from landsat_entities import LandsatBisector
from settings import BLACK, LON, LAT, DISPLAY_SIZE
# from fire_catcher_bot import FireCatcherBot
from wuerso_test_bot import WuersoTestBot


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


def confirm(title):
    """
    Asks a yes/no question to the user
    """

    return prompt([{
        'type': 'confirm',
        'name': 'confirm',
        'message': f'{title} - do you see it?',
    }])['confirm']


def landsat_bisection_algorithm():
    """
    Runs a bisection algorithm on a series of Landsat pictures in order
    for the user to find the approximative date of the fire.
    Images are displayed using pygame, but the interactivity happens in
    the terminal as it is much easier to do.
    """

    # pygame.init()

    bisector = LandsatBisector(LON, LAT)
    bot = WuersoTestBot()
    # disp = pygame.display.set_mode(DISPLAY_SIZE)

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

        bot.send_pic(bisector.image.shot.image, 186562423)
        # disp.fill(BLACK)
        
        # bisector.blit(disp)
        # pygame.display.update()

        return confirm(bisector.date)

    culprit = bisect(bisector.count, mapper, tester)
    bisector.index = culprit

    print(f"Found! First apparition = {bisector.date}")

    # pygame.quit()
    exit()
