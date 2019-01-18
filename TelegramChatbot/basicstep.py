import requests
import json
import datetime
import time
import pandas as pd
import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Updater: to receive the updates from Telegram and to deliver them to said dispatcher.
# CommandHandler: Commands are Telegram messages that start with /, optionally followed by an @ and the bot’s name.
# MessageHandler:  text, media or status updates
# CallbackQueryHandler: handle Telegram callback queries


#터미널에 봇에서 일어날 정보 전달
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# botfather token
token = "~your token"


# 첫 시작
def start(bot, update):
    #username 받기
    print(update.message.chat.username)
    t = ("안녕 %s!, 나는 맥주 추천봇이야!" + "\n" + "아직 서비스 준비 중이지만.." + "\n" + "내가 누군지 궁금하면 /who 를 눌러줘.") % update.message.chat.first_name
    bot.sendMessage(chat_id=update.message.chat_id, text=t)

# 사용자가 예상이외에 답변을 했을때 첫 멘트로 제공
def echo(bot, update):
    #t = update.message.text + " eccome"
    print(update.message.chat.username)
    t =("안녕 %s, 나는 맥주 추천봇이야!" + "\n" + "아직 서비스 준비 중이지만.."+"\n" +"내가 누군지 궁금하면 /who 를 눌러줘") % update.message.chat.first_name
    bot.send_message(chat_id=update.message.chat_id, text=t)

# /who commend
def who(bot, update):
    t = "나는 맥주 데이터를 모아 분석해서 오늘 너의 기분에 따라 맥주 추천해주는 똑똑한 너의 술친구야!!" + "\n" + "이제 날 알겠지?" + "\n" + "/test 를 누르면 내가 맥주 하나 추천해줄게"
    bot.send_message(chat_id=update.message.chat_id, text=t)

# 버튼 메뉴 설정
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    #첫번째 버튼
    if header_buttons:
        menu.insert(0, header_buttons)
    #두버내 버튼
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

# /test commend
def test(bot, update):
    t = "오늘은 날씨가 추우니깐 이런 날은 진한~ 흑맥주가 잘 어울려!"
    bot.sendMessage(chat_id=update.message.chat_id, text=t)
    time.sleep(0.3)
    bot.send_photo(chat_id=update.message.chat_id, photo='https://www.gwine.com/images/labels/guinness-guinness-extra-stout.gif')
    time.sleep(0.3)
    t1 = "기네스 어때?!"
    bot.send_message(chat_id=update.message.chat_id, text=t1)
    time.sleep(0.3)
    # 키보드에 대답 넣기
    show_list = []
    show_list.append(InlineKeyboardButton("좋아", callback_data="좋아"))
    show_list.append(InlineKeyboardButton("별로야", callback_data="별로야"))
    show_markup = InlineKeyboardMarkup(build_menu(show_list, len(show_list) - 1)) # make markup
    update.message.reply_text("내 추천이 어떤지 알려 줄래?", reply_markup=show_markup)

# 버튼의 callback 값에 따라 답변 제공
def callback_get(bot, update):
    print("callback")
    if update.callback_query.data == "좋아":
        bot.edit_message_text(text="진짜? 내 추천 좋지?! 오늘 술 잘 마시고 지나친 음주는 몸에 안 좋은 거 알지?!" + "\n" + "다음에 또 놀러와!",
                          chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id)

    if update.callback_query.data == '별로야' :
        bot.edit_message_text(text= "솔직한 의견 고마워" + "\n" + "다음에 또 놀러와!",
                        chat_id = update.callback_query.message.chat_id,
                        message_id = update.callback_query.message.message_id)

# error 처리
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

# command & function 활성
def main():
    updater = Updater(token=token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    #this one is for the echo function, slightly different from the others
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CommandHandler('who', who))
    dp.add_handler(CommandHandler('test', test))
    dp.add_handler(CallbackQueryHandler(callback_get))

    # log all errors
    dp.add_error_handler(error)
    # polling시작, 걸리는 시간 최대치 정해줌 너무 낮은 경우는 poll이 제대로 작동이 안됨
    # clean =true 기존의 텔레그램 서버에 저장되어있던 업데이트 사항 지우기
    updater.start_polling(timeout=3)
    # idle은 updater가 종료되지 않고 계속 실행
    updater.idle()


if __name__ == '__main__':
    main()