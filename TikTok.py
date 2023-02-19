import re
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '5665091234:AAGXtHM_U7LPMyH-R-baN4uswsxzhPldXRA'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class download(StatesGroup):
    name = State()

headers = {
    'Accept-language': 'en',
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) '
                  'Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:10'
}

def download_video(url):
    request_url = f'https://api.douyin.wtf/api?url={url}'
    response = requests.get(request_url, headers=headers)
    video_link = response.json()['video_data']['nwm_video_url_HQ']
    return video_link

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    btn_download = InlineKeyboardButton('📥 Скачать', callback_data='download')
    markup = InlineKeyboardMarkup().add(btn_download)
    await message.reply(f'👋 Добро пожаловать, {message.chat.first_name}!\n\nДля скачивания видео из TikTok нажмите на кнопку *📥 Скачать*.\n\nПример ссылки: `https://vm.tiktok.com/abcdefg/`', reply_markup=markup, parse_mode=ParseMode.MARKDOWN)

@dp.callback_query_handler(Text(equals='download'))
async def send_video(call: types.CallbackQuery):
    await download.name.set()
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.message.chat.id, '🔗 Пришлите мне ссылку на видео: ')

@dp.callback_query_handler(Text(equals='help'))
async def send_help(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    btn_back = InlineKeyboardButton('↩️ Назад', callback_data='back')
    markup = InlineKeyboardMarkup().add(btn_back)
    await bot.send_message(call.message.chat.id, 'ℹ️ Вам нужна помощь? Просто отправьте мне ссылку на видео TikTok, и я загружу его для вас.\n\n👨‍💻 Если возникли вопросы, пишите @drenix_x', reply_markup=markup)

@dp.callback_query_handler(Text(equals='download_again'))
async def send_video_again(call: types.CallbackQuery):
    await download.name.set()
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.message.chat.id, '🔗 Пришлите мне ссылку на видео: ')

async def send_video_again(message: types.Message):
    btn_download = InlineKeyboardButton('📥 Скачать ещё видео', callback_data='download')
    markup = InlineKeyboardMarkup().add(btn_download)
    await message.answer(reply_markup=markup)

@dp.message_handler(state=download.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    if re.compile('https://[a-zA-Z]+.tiktok.com/').match(message.text):
        video_link = download_video(message.text)
        await bot.send_video(message.chat.id, video_link, caption='👾 Скачано через: @x_downloader_tt_bot', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('📥 Скачать ещё видео', callback_data='download')))
    else:
        btn_help = InlineKeyboardButton('ℹ️ Справка', callback_data='help')
        btn_back = InlineKeyboardButton('↩️ Назад', callback_data='back')
        markup = InlineKeyboardMarkup().add(btn_help, btn_back)
        await bot.send_message(
    message.chat.id, 
    '*⚠️ Вы отправили недействительную ссылку!*\n\nНажмите на кнопку *ℹ️ Справка*, чтобы получить дополнительную информацию.\n\nНажмите на кнопку *↩️ Назад*, чтобы ввести ссылку заново.', 
    reply_markup=markup,
    parse_mode=ParseMode.MARKDOWN)

@dp.callback_query_handler(Text(equals='back'))
async def send_back(call: types.CallbackQuery):
    await send_video(call)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)