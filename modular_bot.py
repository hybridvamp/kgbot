import telegram
import logging
import sys
from telegram.ext import Updater
from telegram.error import (
    TelegramError,
    Unauthorized,
    BadRequest,
    TimedOut,
    ChatMigrated,
    NetworkError)
from telegram.ext import CommandHandler, ConversationHandler
from telegram.ext import MessageHandler, Filters, RegexHandler, CallbackQueryHandler
from channeladmin import UI
from channeladmin import XMLOps
from listitems import Listing


def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized as e:
        print(e)
        # remove update.message.chat_id from
        # conversation list
    except BadRequest as e:
        print(e)
        # handle malformed requests
        # read more below!
    except TimedOut as e:
        print(e)
        # handle slow connection problems
    except NetworkError as e:
        print(e)
        # handle other connection problems
    except ChatMigrated as e:
        print(e)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError as e:
        print(e)
        # handle all other telegram related errors


def cancel(bot, update):
    # Cancel message here
    update.message.reply_text('Bye! I hope we can talk again some day.')
    return ConversationHandler.END
    

def main():
    xmlops = XMLOps()
    Channel = UI(xmlops)
    listsui = Listing()
    TOKEN = sys.argv[1]
    updater = Updater(token=TOKEN)
    bot = telegram.Bot(token=TOKEN)
    print(bot.getMe())
    dispatcher = updater.dispatcher
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    dispatcher.add_error_handler(error_callback)
    channelAdmin_handler = ConversationHandler(
        entry_points=[CommandHandler('channelAdmin', Channel.addEntry)],
        states={
            listsui.FINPUT: [RegexHandler('(Rules)', listsui.rules),
                     RegexHandler('(Groups)', listsui.groupsEntry)],
                     # ~ RegexHandler('(Channels)', listsui.channels),
                     # ~ RegexHandler('Stickers|Previous|Next', listsui.stick_er),
                     # ~ CommandHandler('addsticker', listsui.stickerStart),
                     # ~ RegexHandler('(Cancel)', cancel),
                     # ~ RegexHandler('(Bots)', listsui.bo_t),
                     # ~ RegexHandler('(Know telegram)', listsui.know_tg),
                     # ~ RegexHandler('(GoBack)', listsui.start)],
            listsui.GDIV: [CallbackQueryHandler(listsui.groupsInfo)],
            # ~ listsui.STICKER_NAME: [MessageHandler(Filters.text, listsui.stickerName)],
            # ~ listsui.STICKER_URL: [MessageHandler(Filters.text, listsui.stickerURL)],
            # ~ listsui.STICKER_IMG: [MessageHandler(Filters.photo, listsui.stickerImage)],
            # ~ listsui.KNWTG: [CallbackQueryHandler(listsui.button)],
            # ~ listsui.CHNL: [CallbackQueryHandler(listsui.button_channel)],
            # ~ listsui.BOT: [CallbackQueryHandler(listsui.button_bot)],
			Channel.NEW_CATEG: [RegexHandler('(Yes)', Channel.addNewCategory),
                                RegexHandler('(No, add to existing category)',
                                             Channel.showCategory)],
            Channel.SAVE_CATEG: [MessageHandler(Filters.text,
                                                Channel.addSaveCategory),
                                CallbackQueryHandler(Channel.addSaveCategory)],
            Channel.TITLE: [MessageHandler(Filters.text, Channel.addTitle),
                           CallbackQueryHandler(Channel.addTitle)],
            # Channel.SHOW_CATEG: [
            Channel.URL: [MessageHandler(Filters.text, Channel.addUrl)],
            Channel.WRITE: [MessageHandler(Filters.text, Channel.addWrite)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    listingfun_handler =  ConversationHandler(
        entry_points=[CommandHandler('start', listsui.start)],
        states={
            listsui.FINPUT: [RegexHandler('(Rules)', listsui.rules),
                     RegexHandler('(Groups)', listsui.groupsEntry),
                     RegexHandler('(Channels)', listsui.channels),
                     RegexHandler('Stickers|Previous|Next', listsui.stick_er),
                     CommandHandler('addsticker', listsui.stickerStart),
                     RegexHandler('(Cancel)', cancel),
                     RegexHandler('(Bots)', listsui.bo_t),
                     RegexHandler('(Know telegram)', listsui.know_tg),
                     RegexHandler('(GoBack)', listsui.start)],
            listsui.GDIV: [CallbackQueryHandler(listsui.groupsInfo)],
            listsui.STICKER_NAME: [MessageHandler(Filters.text, listsui.stickerName)],
            listsui.STICKER_URL: [MessageHandler(Filters.text, listsui.stickerURL)],
            listsui.STICKER_IMG: [MessageHandler(Filters.photo, listsui.stickerImage)],
            listsui.KNWTG: [CallbackQueryHandler(listsui.button)],
            listsui.CHNL: [CallbackQueryHandler(listsui.button_channel)],
            listsui.BOT: [CallbackQueryHandler(listsui.button_bot)]
			
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(channelAdmin_handler)
    dispatcher.add_handler(listingfun_handler)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
