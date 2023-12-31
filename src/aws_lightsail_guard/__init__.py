import logging

from dotenv import load_dotenv

logging.basicConfig(
    filename="logs/guard.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)
load_dotenv()
