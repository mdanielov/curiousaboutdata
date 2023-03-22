import configparser
import os

config=configparser.RawConfigParser()
config.optionxform=str
config.read( 'settings.ini')

os.environ['CONNECTION_STRING'] = config['DATABASE']['CONNECTION_STRING']


