from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from config import WHATS_APP_URL, INST_URL, TIKTOK_URL

def get_kb_start():
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(KeyboardButton('/help'),KeyboardButton('/info'), KeyboardButton('/contacts')).add(KeyboardButton('/order'))



def get_kb_contacts():
    return InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text="Instagram", url=INST_URL)).add(InlineKeyboardButton(text="WhatsApp", url=WHATS_APP_URL)).add(InlineKeyboardButton(text="TikTok", url=TIKTOK_URL))
