import asyncio
from create_bot import application
from handlers import client
async def main()->None:
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.run_polling()
if __name__=="__main__":
    application.run_polling()