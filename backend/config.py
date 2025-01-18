import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env.local'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'