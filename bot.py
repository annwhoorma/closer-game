from typing import Optional
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram import ChatAction
from telegram.utils.types import FileInput
import os

from game import Game
from pathlib import Path

APP_NAME = os.environ.get('APP_NAME', 'app_name')
PORT = int(os.environ.get('PORT', '8443'))
TOKEN = os.getenv('TOKEN')


def reply_text(update: Update, message: str):
    update.message.reply_chat_action(ChatAction.TYPING)
    update.message.reply_text(message)

def reply_photo(update: Update, fp: FileInput, caption=None):
    update.message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
    update.message.reply_photo(photo=fp, caption=caption)


def start(update: Update, context: CallbackContext):
    global current_card, game_deck

    cards_path = Path('./images')
    game = Game(cards_path)
    game_deck = game.get_deck()
    current_card = 0
    reply_text(update, f'новая колода сгенерирована :) тыкни /help, чтобы посмотреть правила')


def get_next(update: Update, context: CallbackContext):
    global game_deck, current_card
    if game_deck is None or current_card is None:
        reply_text(update, 'уверены, что тыкнули /start?')
        return
    if current_card >= len(game_deck):
        reply_text(update, 'правда больше нет :(')
        return
    reply_photo(update, fp=open('images/'+game_deck[current_card], 'rb'))
    current_card += 1
    if current_card >= len(game_deck):
        reply_text(update, 'это была последняя! <3')



def get_rules(update: Update, context: CallbackContext):
    caption = ('в игре есть три вида карт: R (Reverse), Q (Question), and A (Action). '
    'карта R означает, что тому/той, кто ходил_а последним, придется ходить еще раз. '
    'остальные карты объясняют сами себя :) '
    f'ах да, чтобы получать карты из колоды, тыкай /next')
    reply_photo(update, fp=open('images/rules/RulesCard.png', 'rb'), caption=caption)


def finish(update: Update, context: CallbackContext):
    global game, game_deck, current_card
    game = None
    game_deck = None
    current_card = None
    reply_text(update, 'есть слух, что ты солнышко :)')


# set use_content=False if not needed
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('next', get_next))
dispatcher.add_handler(CommandHandler('help', get_rules))
dispatcher.add_handler(CommandHandler('finish', finish))


def main():
    global game, game_deck, current_card
    game = None
    game_deck = None
    current_card = None
    # comment next 4 lines if you run locally
    updater.start_webhook(listen='0.0.0.0',
                        port=int(PORT),
                        url_path=TOKEN,
                        webhook_url=f'https://{APP_NAME}.herokuapp.com/{TOKEN}')
    # updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()