from landsat_manager import landsat_bisection_algorithm
from fire_catcher_bot import FireCatcherBot

import time

if __name__ == '__main__':

    bot = FireCatcherBot()
    last_update_id = None
    while True:
        print("getting updates")
        updates = bot.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = bot.get_last_update_id(updates) + 1
            chat_id = bot.get_triggered_chat_id(updates)
            if chat_id:
                bot.send_greetings(chat_id)
                bot.last_updates[chat_id] = last_update_id
                landsat_bisection_algorithm(bot, chat_id)
        time.sleep(0.5)
