import asyncio
import logging
import os
from datetime import timedelta, timezone
from pathlib import Path
from telethon import TelegramClient
import pytz

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_DIR = PROJECT_ROOT / "envpath"

ENV_FILE_VAR = os.getenv("CONFIG_ENV_FILE", "bot1.env")
if os.path.isabs(ENV_FILE_VAR):
    DOTENV_FILE = Path(ENV_FILE_VAR)
else:
    DOTENV_FILE = ENV_DIR / ENV_FILE_VAR if (ENV_DIR / ENV_FILE_VAR).exists() else PROJECT_ROOT / ENV_FILE_VAR

def load_dotenv_file(path):
    values = {}
    try:
        with open(path, encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if value:
                    values[key] = value
    except FileNotFoundError:
        return {}
    return values

def parse_int_list(value, default=None):
    if value is None or value == "":
        return default if default is not None else []
    return [int(item.strip()) for item in value.split(",") if item.strip()]

_env = load_dotenv_file(DOTENV_FILE)
for key, value in _env.items():
    if key not in os.environ:
        os.environ[key] = value

API_ID = int(os.getenv("API_ID", "35873646"))
API_HASH = os.getenv("API_HASH", "3eaf9faf00e794125b7330d4978ffdce")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_IDS = parse_int_list(os.getenv("OWNER_IDS", "6866643730"), default=[6866643730])

BOT_NAME_TAG = DOTENV_FILE.stem.replace(".env", "").replace("env", "") or "default"
if not BOT_NAME_TAG or BOT_NAME_TAG == ".":
    BOT_NAME_TAG = "default"

BOT_DATA_DIR = PROJECT_ROOT / f"data_{BOT_NAME_TAG}"
BOT_DATA_DIR.mkdir(parents=True, exist_ok=True)

SESSION_NAME = str(BOT_DATA_DIR / "bot_session")
DB_FILE = str(BOT_DATA_DIR / "periodic_tasks.db")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
)
logger = logging.getLogger(f"NighthavenPesan-{BOT_NAME_TAG}")

bot = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Timezone WIB (Asia/Jakarta)
WIB = pytz.timezone("Asia/Jakarta")
