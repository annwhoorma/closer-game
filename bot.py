from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram import ChatAction
from telegram.utils.types import FileInput

from game import Game
from pathlib import Path

TOKEN = "5089146854:AAH6Bi-7YYPpTpjb-nRRm1jeAzoS7zA4OoQ"

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher


def reply_text(update: Update, message: str):
    update.message.reply_chat_action(ChatAction.TYPING)
    update.message.reply_text(message)

def reply_photo(update: Update, fp: FileInput):
    update.message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
    update.message.reply_photo(photo=open('images/'+game_deck[current_card], 'rb'))

def command_handler(command):
    def decorator(func):
        handler = CommandHandler(command, func)
        dispatcher.add_handler(handler)
        return func
    return decorator


@command_handler('start')
def start(update: Update, context: CallbackContext):
    reply_text(update, 'щас она тебе все объяснит')

@command_handler('next')
def get_next(update: Update, context: CallbackContext):
    global current_card
    if current_card >= len(game_deck):
        reply_text(update, "правда больше нет :(")
        return
    reply_photo(update, fp=open('images/'+game_deck[current_card], 'rb'))
    current_card += 1
    if current_card >= len(game_deck):
        reply_text(update, 'это была последняя! <3')

@command_handler('finish')
def finish(update: Update, context: CallbackContext):
    reply_text(update, 'есть слух, что ты солнышко :) пока!')

def main():
    global current_card, game_deck

    cards_path = Path('./images')
    game = Game(cards_path)
    game_deck = game.get_deck()
    current_card = 0

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()