import re

from aiogram import Router, Bot, F, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import IntegrityError

from bot import keyboards as kb, utils
from bot.filters import ChatTypeFilter
from bot.states import RegisterState
from data.base import get_session
from data.models import User

register_state_router = Router()


@register_state_router.message(RegisterState.first_name, F.text)
async def register_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Familyangizni kiriting", reply_markup=kb.delete())
    await state.set_state(RegisterState.last_name)


@register_state_router.message(RegisterState.last_name, F.text)
async def register_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)

    await message.answer(text="Telefon raqamingizni kiriting", reply_markup=kb.share_contact())
    await state.set_state(RegisterState.phone_number)


@register_state_router.message(RegisterState.phone_number, F.text,
                               lambda message: re.match(r"^998\d{9}$", message.text))
async def register_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer(text="Jinsingizni tanlang", reply_markup=kb.gender())
    await state.set_state(RegisterState.gender)


@register_state_router.message(RegisterState.phone_number, F.text,
                               lambda message: not re.match(r"^998\d{9}$", message.text))
async def invalid_phone_number(message: types.Message):
    await message.answer(text="Telefon raqami noto'g'ri formatda. Iltimos, qaytadan kiriting. Masalan, '998993250628'")


@register_state_router.message(RegisterState.phone_number, F.contact)
async def register_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    await message.answer(text="Jinsingizni tanlang", reply_markup=kb.gender())
    await state.set_state(RegisterState.gender)


@register_state_router.message(RegisterState.gender, lambda message: message.text.lower() not in ['erkak', 'ayol'])
async def handle_invalid_gender(message: types.Message):
    await message.answer(text="Jinsingizni tanlashda xatolik qildingiz. Iltimos, 'Erkak' yoki 'Ayol' ni tanlang.")


@register_state_router.message(RegisterState.gender, lambda message: message.text.lower() in ['erkak', 'ayol'])
async def register_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text.lower())
    await message.answer(text="Manzilingizni ulashing", reply_markup=kb.location_ignore())
    await state.set_state(RegisterState.location)


@register_state_router.message(RegisterState.location, F.location)
async def register_location(message: types.Message, state: FSMContext):
    await state.update_data(latitude=message.location.latitude)
    await state.update_data(longitude=message.location.longitude)
    await message.answer(text="Profile uchun rasmingizni yuklang", reply_markup=kb.ignore())
    await state.set_state(RegisterState.profile_pic)


@register_state_router.message(RegisterState.location, F.text != "Tashlab ketish")
async def handle_invalid_location(message: types.Message):
    await message.answer(text="Manzilingizni aniqlab bo'lmadi.")


@register_state_router.message(RegisterState.location, F.text == "Tashlab ketish")
async def ignore(message: types.Message, state: FSMContext):
    await message.answer(text="Profile uchun rasmingizni yuklang", reply_markup=kb.ignore())
    await state.set_state(RegisterState.profile_pic)


@register_state_router.message(RegisterState.profile_pic, F.photo)
async def register_profile_pic(message: types.Message, state: FSMContext, bot: Bot):
    path = await utils.download_profile_pic(message, bot)
    await state.update_data(profile_pic=path)
    await message.answer("Malumotlaringiz saqlansinmi ?", reply_markup=kb.confirm_save_to_database())
    await state.set_state(RegisterState.confirmation)


@register_state_router.message(RegisterState.profile_pic, F.text == "Tashlab ketish")
async def ignore(message: types.Message, state: FSMContext):
    await message.answer("Malumotlaringiz saqlansinmi ?", reply_markup=kb.confirm_save_to_database())
    await state.set_state(RegisterState.confirmation)


@register_state_router.message(RegisterState.confirmation, F.text.contains("Bekor qilish"))
async def cancel_register(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    path = user_data.get('profile_pic', None)
    await utils.delete_profile_pic(path)
    await state.clear()
    await message.answer("Ro'yxatdan o'tish bekor qilindi", reply_markup=kb.delete())


@register_state_router.message(RegisterState.confirmation, F.text.contains("Tahrirlash"))
async def cancel_register(message: types.Message, state: FSMContext, bot: Bot):
    await message.answer("Ismingizni kiriting", reply_markup=kb.delete())
    await state.set_state(RegisterState.first_name)


@register_state_router.message(RegisterState.confirmation, F.text.contains("Ha"))
async def save_to_database(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    new_user = User(
        chat_id=user_data.get('chat_id'),
        first_name=user_data.get('first_name'),
        last_name=user_data.get('last_name'),
        phone_number=user_data.get('phone_number'),
        gender=user_data.get('gender'),
        latitude=user_data.get('latitude', None),
        longitude=user_data.get('longitude', None),
        profile_pic=user_data.get('profile_pic', None)
    )

    try:
        async with get_session() as session:
            session.add(new_user)
            await session.commit()

    except IntegrityError as e:
        await message.answer("Bu chat_id bilan foydalanuvchi allaqachon ro'yxatdan o'tgan.", reply_markup=kb.delete())
    except Exception as e:
        await state.clear()
        raise await message.answer("Nimadur xato ketdi. Iltimos keyinroq urinib ko'ring.", reply_markup=kb.delete())
    else:
        await message.answer("Muvafaqiyatli ro'yxatdan o'tdingiz", reply_markup=kb.delete())
        await state.clear()
    finally:
        await session.close()
