import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

BOT_TOKEN = "8596497022:AAELMTybSJXiXi30F2zC_SQwW4ugiVHbEHc"
CRYPTO_TOKEN = "534306:AAeEQbrOHjChtvdLakQAqhPKwgcp05Ra650"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

PRICE = 100
VK_INVITE = "https://vk.com/invite/vRdplI8"

async def create_invoice():
    url = "https://pay.crypt.bot/api/createInvoice"
    headers = {"Crypto-Pay-API-Token": CRYPTO_TOKEN}
    data = {
        "asset": "USDT",
        "amount": 1,
        "description": "Доступ в закрытый клуб"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as resp:
            result = await resp.json()
            return result["result"]["bot_invoice_url"]

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Получить доступ за 100₽", callback_data="buy")]
    ])

    await message.answer(
        "🔥 VAULT BLACK 🔥\n\n"
        "Закрытый клуб с эксклюзивным контентом.\n\n"
        "💰 Цена сейчас 100₽\n"
        "⚠️ После набора участников будет дороже\n\n"
        "Нажми кнопку ниже 👇",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "buy")
async def buy(callback: types.CallbackQuery):
    invoice_url = await create_invoice()
    await callback.message.answer(f"Оплатите по ссылке:\n{invoice_url}")
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
