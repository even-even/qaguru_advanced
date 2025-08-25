""" Файл со строками и другими константами"""
import os

import dotenv

dotenv.load_dotenv()

USER_NOT_FOUND = "User not found"


APP_URL = os.getenv("APP_URL")


BLACK_LIST_CODES = (401, 403, 500, 501, 502, 503, 504)
