from dotenv import load_dotenv
import os

load_dotenv("../.meteo.env")
URL= os.getenv("URL")
MAX_CALLS_DAILY= int(os.getenv("MAX_CALLS_DAILY"))