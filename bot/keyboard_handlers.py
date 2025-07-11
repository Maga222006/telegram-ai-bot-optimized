# --- keyboard_handlers.py ---
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from database.config import create_or_update_config

router = Router()

# Define FSM states
class ConfigStates(StatesGroup):
    openai_key = State()
    openai_base = State()
    model = State()
    image_model = State()
    stt_model = State()
    weather_key = State()
    github_token = State()
    tavily_key = State()

# Button triggers
@router.message(F.text == "🔑 Set OpenAI API Key")
async def ask_openai_key(msg: Message, state: FSMContext):
    await msg.answer("Please send your OpenAI API Key:")
    await state.set_state(ConfigStates.openai_key)

@router.message(F.text == "🌐 Set OpenAI API Base")
async def ask_openai_base(msg: Message, state: FSMContext):
    await msg.answer("Please send your OpenAI API Base URL:")
    await state.set_state(ConfigStates.openai_base)

@router.message(F.text == "🧠 Set Model")
async def ask_model(msg: Message, state: FSMContext):
    await msg.answer("Please enter the model name (e.g. gpt-4, gpt-3.5-turbo):")
    await state.set_state(ConfigStates.model)

@router.message(F.text == "🖼️ Set Image Model")
async def ask_image_model(msg: Message, state: FSMContext):
    await msg.answer("Please enter the image model name:")
    await state.set_state(ConfigStates.image_model)

@router.message(F.text == "🎧 Set STT Model")
async def ask_stt_model(msg: Message, state: FSMContext):
    await msg.answer("Please enter the STT (Speech-to-Text) model name:")
    await state.set_state(ConfigStates.stt_model)

@router.message(F.text == "☁️ Set OpenWeatherMap Key")
async def ask_weather_key(msg: Message, state: FSMContext):
    await msg.answer("Please enter your OpenWeatherMap API key:")
    await state.set_state(ConfigStates.weather_key)

@router.message(F.text == "💙 Set GitHub Token")
async def ask_github_token(msg: Message, state: FSMContext):
    await msg.answer("Please enter your GitHub token:")
    await state.set_state(ConfigStates.github_token)

@router.message(F.text == "🔍 Set Tavily API Key")
async def ask_tavily_key(msg: Message, state: FSMContext):
    await msg.answer("Please enter your Tavily API key:")
    await state.set_state(ConfigStates.tavily_key)

# Handlers to save inputs
@router.message(F.text, ConfigStates.openai_key)
async def save_openai_key(msg: Message, state: FSMContext):
    await create_or_update_config(str(msg.from_user.id), openai_api_key=msg.text)
    await msg.answer("✅ OpenAI API Key saved.")
    await state.clear()

@router.message(F.text, ConfigStates.openai_base)
async def save_openai_base(msg: Message, state: FSMContext):
    await create_or_update_config(str(msg.from_user.id), openai_api_base=msg.text)
    await msg.answer("✅ OpenAI API Base saved.")
    await state.clear()

@router.message(F.text, ConfigStates.model)
async def save_model(msg: Message, state: FSMContext):
    await create_or_update_config(str(msg.from_user.id), model=msg.text)
    await msg.answer("✅ Model name saved.")
    await state.clear()

@router.message(F.text, ConfigStates.image_model)
async def save_image_model(msg: Message, state: FSMContext):
    await create_or_update_config(str(msg.from_user.id), image_model=msg.text)
    await msg.answer("✅ Image model saved.")
    await state.clear()

@router.message(F.text, ConfigStates.stt_model)
async def save_stt_model(msg: Message, state: FSMContext):
    await create_or_update_config(str(msg.from_user.id), stt_model=msg.text)
    await msg.answer("✅ STT model saved.")
    await state.clear()

@router.message(F.text, ConfigStates.weather_key)
async def save_weather_key(msg: Message, state: FSMContext):
    await create_or_update_config(str(msg.from_user.id), openweathermap_api_key=msg.text)
    await msg.answer("✅ OpenWeatherMap API key saved.")
    await state.clear()

@router.message(F.text, ConfigStates.github_token)
async def save_github_token(msg: Message, state: FSMContext):
    await create_or_update_config(str(msg.from_user.id), github_token=msg.text)
    await msg.answer("✅ GitHub token saved.")
    await state.clear()

@router.message(F.text, ConfigStates.tavily_key)
async def save_tavily_key(msg: Message, state: FSMContext):
    await create_or_update_config(str(msg.from_user.id), tavily_api_key=msg.text)
    await msg.answer("✅ Tavily API key saved.")
    await state.clear()
