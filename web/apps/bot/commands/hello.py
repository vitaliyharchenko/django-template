from .. import commands

def hello():
   message = 'Привет, друг!\nЯ новый чат-бот.'
   return message, ''

hello_command = commands.Command()

hello_command.keys = ['привет', 'hello', 'дратути', 'здравствуй', 'здравствуйте']
hello_command.description = 'Поприветствую тебя'
hello_command.process = hello