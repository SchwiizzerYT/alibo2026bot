import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.exceptions import TelegramBadRequest

TOKEN = os.getenv("BOT_TOKEN", "8989853757:AAH0OBx9KH1XeVF22U7gZSqwGyv2920vuD0")

# Kanal ID si yoki username'i (@ kanalingiz_nomi)
# Eslatma: Bot kanalingizda ADMIN bo'lishi SHART!
CHANNEL_ID = "@codialuz"  # Masalan: "@my_channel_uz"
CHANNEL_LINK = "https://t.me/codialuz"  # Kanal havolasi

ALPHABET = {
    "o": ("O' o'", "Ö ö"),
    "g": ("G' g'", "Ğ ğ"),
    "sh": ("Sh sh", "Ş ş"),
    "ch": ("Ch ch", "Ç ç"),
}

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Obuna bo'lish tugmasi tugmalari
def sub_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📢 Kanalga obuna bo'lish", url=CHANNEL_LINK)],
        [InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_sub")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Harflar tugmasi
def letters_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text=old, callback_data=f"letter:{key}")
        for key, (old, _new) in ALPHABET.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons[:2], buttons[2:]])


# Obunani tekshiruvchi funksiya
async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # Obuna bo'lgan yoki admin/yaratuvchi bo'lsa True qaytaradi
        return member.status in ["member", "administrator", "creator"]
    except TelegramBadRequest:
        return False


@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    if await is_subscribed(user_id):
        await message.answer(
            "Assalomu alaykum! Harf tanlang:",
            reply_markup=letters_keyboard(),
        )
    else:
        await message.answer(
            "Botdan foydalanish uchun iltimos, avval kanalimizga obuna bo'ling!",
            reply_markup=sub_keyboard(),
        )


@dp.callback_query(F.data == "check_sub")
async def check_subscription(callback: CallbackQuery):
    user_id = callback.from_user.id
    if await is_subscribed(user_id):
        await callback.message.edit_text(
            "Rahmat! Obuna tasdiqlandi. Harf tanlang:",
            reply_markup=letters_keyboard(),
        )
    else:
        await callback.answer(
            "Siz hali kanalga obuna bo'lmadingiz! ❌", show_alert=True
        )


@dp.callback_query(F.data.startswith("letter:"))
async def show_letter(callback: CallbackQuery):
    user_id = callback.from_user.id
    # Foydalanuvchi tugmani bosganda ham obunasi borligini tekshiramiz
    if not await is_subscribed(user_id):
        await callback.message.edit_text(
            "Botdan foydalanish uchun kanalka obuna bo'lishingiz kerak!",
            reply_markup=sub_keyboard(),
        )
        return

    key = callback.data.split(":", 1)[1]
    old, new = ALPHABET[key]
    await callback.message.edit_text(
        f"{old}\nYangi alifbodagi yozilishi -> {new}",
        reply_markup=letters_keyboard(),
    )
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
