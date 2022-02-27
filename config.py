import os

settings = {
    'token': os.getenv('TOKEN'),
    'bot': os.getenv('BOT'),
    'id': os.getenv('ID'),
    'prefix': os.getenv('PREFIX'),
    'version': os.getenv('VERSION')
}
MONGODB_LINK = os.getenv('MONGO_URL')
