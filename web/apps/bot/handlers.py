from . import vkapi
import importlib, os


def get_answer(body):
   message = 'Привет, я новый бот! Не шли мне больше {}'.format(body)
   return message

def create_answer(data, token):
   from .commands import hello, info
   user_id = data['user_id']
   message = get_answer(data['body'].lower())
   vkapi.send_message(user_id, token, message)