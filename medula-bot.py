# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://git.io/JOmFw.
"""
import logging

from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from bs4 import BeautifulSoup
import requests
import re

medulaText = ["¿Quién puede donar médula?",
              "¿Cuál es la campaña actual?",
              "¿Cuál es el horario de registro en la UPM?"]
medulaRespuesta = ["Los requisitos imprescindibles para registrarse en España como donante de progenitores hematopoyéticos de médula ósea son tener entre 18 y 40 años, pesar más de 50 kilos y gozar de buen estado de salud. Para más datos entra en https://www.comunidad.madrid/servicios/salud/donacion-medula-osea",
                   "El horario actual de información y registro en la UPM es el siguiente:"]

randomPeopleUrl = "https://thispersondoesnotexist.com/image"
randomPImageUrl = "https://picsum.photos/1200"

likes = 0
dislikes = 0

allowedUsernames = ['IsThisLuis']


def startCommand(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(medulaText[0])],[KeyboardButton(medulaText[1])],[KeyboardButton(medulaText[2])]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to my bot!",
                             reply_markup=ReplyKeyboardMarkup(buttons))


def messageHandler(update: Update, context: CallbackContext):
    if update.effective_chat.username not in allowedUsernames:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not allowed to use this bot")
        return
    if medulaText[0] in update.message.text:
        context.bot.send_message(chat_id=update.effective_chat.id, text=medulaRespuesta[0])

    if medulaText[1] in update.message.text:
        context.bot.send_message(chat_id=update.effective_chat.id, text=getCampaign())

    if medulaText[2] in update.message.text:
        context.bot.send_message(chat_id=update.effective_chat.id, text=medulaRespuesta[1])
        context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open('horario.png', 'rb'))

# Extraer BeautifulSoup de url
def getSoup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

def getCampaign():
    mainPage = getSoup(f"https://equipomedula.org/")
    lema = mainPage.find("mark", class_="has-inline-color").text.strip()
    video = mainPage.find("meta", attrs={'name':'description'})['content']
    video = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+', video)[0]
    print(video)

    return f"Nuestra campaña actual es {lema} y nuestro vídeo {video}"


def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()

    global likes, dislikes

    if "like" in query:
        likes += 1

    if "dislike" in query:
        dislikes += 1

    print(f"likes => {likes} and dislikes => {dislikes}")


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5284473451:AAGTSFl__XEVaod2VqdE5XvRHvBDS4XFpk0")

    updater.dispatcher.add_handler(CommandHandler("start", startCommand))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
    updater.dispatcher.add_handler(CallbackQueryHandler(queryHandler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()