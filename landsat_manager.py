from PyInquirer import prompt
import pygame

from landsat_entities import LandsatBisector
from settings import BLACK, LON, LAT, DISPLAY_SIZE


def bisect(n, mapper, tester, chat_id):
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

        if tester(val, chat_id):
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


def landsat_bisection_algorithm(bot, chat_id):
    """
    Runs a bisection algorithm on a series of Landsat pictures in order
    for the user to find the approximative date of the fire.
    Images are displayed using pygame, but the interactivity happens in
    the terminal as it is much easier to do.
    """

    bisector = LandsatBisector(LON, LAT)

    def mapper(n):
        """
        In that case there is no need to map (or rather, the mapping
        is done visually by the user)
        """

        return n

    def tester(n, chat_id):
        """
        Displays the current candidate to the user and asks them to
        check if they see wildfire damages.
        """

        bisector.index = n

        bot.send_pic(bisector.image.shot.image, chat_id)
        bot.send_message(f'{bisector.date} - do you see it? (Y/n)', chat_id)
        return bot.get_player_confirmation(chat_id)

    culprit = bisect(bisector.count, mapper, tester, chat_id)
    bisector.index = culprit


    bot.send_message(f"Found! First apparition = {bisector.date}", chat_id)
