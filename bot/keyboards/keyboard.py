from aiogram.types import KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def confirm():
    rkm_b = ReplyKeyboardBuilder()
    rkm_b.add(KeyboardButton(text="Ha"))
    rkm_b.add(KeyboardButton(text="Yo'q"))
    rkm = rkm_b.as_markup(resize_keyboard=True)

    return rkm


def delete():
    rmr = ReplyKeyboardRemove()
    return rmr


def my_info():
    rkm_b = ReplyKeyboardBuilder()
    rkm_b.add(KeyboardButton(text="Mening ma'lumotlarim"))
    rkm = rkm_b.as_markup(resize_keyboard=True)

    return rkm


def gender():
    rkm_b = ReplyKeyboardBuilder()
    rkm_b.add(KeyboardButton(text="Erkak"))
    rkm_b.add(KeyboardButton(text="Ayol"))
    rkm = rkm_b.as_markup(resize_keyboard=True)

    return rkm


def share_contact():
    rkm_b = ReplyKeyboardBuilder()
    rkm_b.add(KeyboardButton(
        text="Telefon raqamni ulashish", request_contact=True))
    rkm = rkm_b.as_markup(resize_keyboard=True)

    return rkm


def share_location():
    rkm_b = ReplyKeyboardBuilder()
    rkm_b.add(KeyboardButton(
        text="Telefon raqamni ulashish", request_location=True))
    rkm = rkm_b.as_markup(resize_keyboard=True)

    return rkm


def location_ignore():
    rkm_b = ReplyKeyboardBuilder()
    rkm_b.add(KeyboardButton(
        text="Manzilni ulashish", request_location=True))
    rkm_b.add(KeyboardButton(
        text="Tashlab ketish"))
    rkm = rkm_b.as_markup(resize_keyboard=True)

    return rkm


def location():
    rkm_b = ReplyKeyboardBuilder()
    rkm_b.add(KeyboardButton(
        text="Manzilni ulashish", request_location=True))
    rkm = rkm_b.as_markup(resize_keyboard=True)

    return rkm


def ignore():
    rkm_b = ReplyKeyboardBuilder()
    rkm_b.add(KeyboardButton(
        text="Tashlab ketish"))
    rkm = rkm_b.as_markup(resize_keyboard=True)

    return rkm


def confirm_save_to_database():
    rkm_b = ReplyKeyboardBuilder()
    rkm_b.add(KeyboardButton(text="Ha saqlansin"))
    rkm_b.add(KeyboardButton(text="Bekor qilish"))
    rkm_b.add(KeyboardButton(text="Tahrirlash"))
    rkm = rkm_b.adjust(2, True).as_markup(resize_keyboard=True)

    return rkm


def start_counter():
    rkm_b = ReplyKeyboardBuilder()
    rkm_b.add(KeyboardButton(text="Boshlash"))
    rkm = rkm_b.adjust(2, True).as_markup(resize_keyboard=True)

    return rkm
