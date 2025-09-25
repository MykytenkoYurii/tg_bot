import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage


API_TOKEN = "8246523084:AAHtVhY5SzFIwFe3ltZbj-QUBIIzEqmhaFw"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Тут будемо зберігати зареєстрованих користувачів (у форматі {username: password})
users_db = {}

# Стан машини для реєстрації
class RegisterState(StatesGroup):
    username = State()
    password = State()

# Стан машини для логіну
class LoginState(StatesGroup):
    username = State()
    password = State()


# Start command
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привіт! 👋 Я твій Recommendation Assistant.\n"
                         "Надішли /recommend, щоб отримати пораду."
                         "\nНадішли /register, щоб зареєструватися."
                         "\nНадішли /login, щоб увійти."
                         "\nНадішли /exit, щоб вийти.")
    
# Exit command
@dp.message(Command("exit"))
async def exit_cmd(message: types.Message):
    # тут можна очистити дані користувача, якщо вони зберігаються
    await message.answer("Ви вийшли. Для повторного входу використайте /start.")


# Recommend command
@dp.message(Command("recommend"))
async def recommend_handler(message: Message):
    await message.answer("Тут згодом буде твоя персональна рекомендація 🎬📚🎵")


# ======================
#       РЕЄСТРАЦІЯ
# ======================
@dp.message(Command("register"))
async def register_start(message: types.Message, state: FSMContext):
    await message.answer("Введіть логін для реєстрації:")
    await state.set_state(RegisterState.username)

@dp.message(RegisterState.username)
async def register_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Тепер введіть пароль:")
    await state.set_state(RegisterState.password)

@dp.message(RegisterState.password)
async def register_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data["username"]
    password = message.text

    if username in users_db:
        await message.answer("Такий користувач вже існує!")
    else:
        users_db[username] = password
        await message.answer(f"✅ Реєстрація успішна! Тепер ви можете /login")

    await state.clear()


# ======================
#         ЛОГІН
# ======================
@dp.message(Command("login"))
async def login_start(message: types.Message, state: FSMContext):
    await message.answer("Введіть ваш логін:")
    await state.set_state(LoginState.username)

@dp.message(LoginState.username)
async def login_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Тепер введіть пароль:")
    await state.set_state(LoginState.password)

@dp.message(LoginState.password)
async def login_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data["username"]
    password = message.text

    if username in users_db and users_db[username] == password:
        await message.answer(f"✅ Вітаю, {username}, ви успішно увійшли!")
    else:
        await message.answer("❌ Невірний логін або пароль.")

    await state.clear()

# 🔹 Головна функція
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
