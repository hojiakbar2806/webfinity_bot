from random import randint

from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils import BallsCallbackFactory


def likee(like, dislike):
    ikm_b = InlineKeyboardBuilder()
    ikm_b.add(InlineKeyboardButton(
        text=f"👍 {like}", callback_data='action_like'))
    ikm_b.add(InlineKeyboardButton(
        text=f"👎 {dislike}", callback_data='action_dislike'))
    ikm_b.adjust(2)
    ikm = ikm_b.as_markup()
    return ikm


def require_channels():
    ikm_b = InlineKeyboardBuilder()
    ikm_b.add(InlineKeyboardButton(text="Saodat asri", url="https://t.me/SaodatAsrigaQaytib"))
    ikm_b.add(InlineKeyboardButton(text="Tekshirish", callback_data="check_subscriber"))
    ikm_b.adjust(2)
    ikm = ikm_b.as_markup()
    return ikm


def register_data():
    ikm_b = InlineKeyboardBuilder()
    ikm_b.add(InlineKeyboardButton(
        text="First Name", callback_data="register_edit_firstname"))
    ikm_b.add(InlineKeyboardButton(
        text="Last Name", callback_data="register_edit_lastname"))
    ikm_b.add(InlineKeyboardButton(
        text="Phone Number", callback_data="register_edit_phone"))
    ikm_b.add(InlineKeyboardButton(
        text="Gender", callback_data="register_edit_gender"))
    ikm_b.add(InlineKeyboardButton(
        text="Location", callback_data="register_edit_location"))
    ikm_b.add(InlineKeyboardButton(
        text="Profile Pic", callback_data="register_edit_profilepic"))

    ikm_b.adjust(2)
    ikm = ikm_b.as_markup()

    return ikm


def delete_user():
    ikm_b = InlineKeyboardBuilder()
    ikm_b.add(InlineKeyboardButton(
        text="O'chirish", callback_data="delete_user_info"))

    ikm_b.adjust(2)
    ikm = ikm_b.as_markup()

    return ikm


def generate_balls() -> InlineKeyboardMarkup:
    balls_mask = [False] * 9
    balls_mask[randint(0, 8)] = True
    balls = ["🔴", "🟢"]
    data = ["red", "green"]
    ikm_b = InlineKeyboardBuilder()
    for item in balls_mask:
        ikm_b.button(
            text=balls[item],
            callback_data=BallsCallbackFactory(color=data[item]).pack()
        )
    return ikm_b.adjust(3).as_markup()
