import sys
import contextlib
import FinalSN
from FinalSN import BOTLOG_CHATID, HEROKU_APP, PM_LOGGER_GROUP_ID
from .Config import Config
from .core.logger import logging
from .core.session import final313
from .utils import (
    add_bot_to_logger_group,
    install_externalrepo,
    load_plugins,
    setup_bot,
    mybot,
    startupmessage,
    verifyLoggerGroup,
    saves,
)

LOGS = logging.getLogger("FinalSN")
imam_ali = """
_____________________   ______________                    
___  ____/___  _/__  | / /__    |__  /                    
__  /_    __  / __   |/ /__  /| |_  /                     
_  __/   __/ /  _  /|  / _  ___ |  /___                   
/_/      /___/  /_/ |_/  /_/  |_/_____/                   
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
_____  ________________________________________________   
__  / / /_  ___/__  ____/__  __ \__  __ )_  __ \__  __/   
_  / / /_____ \__  __/  __  /_/ /_  __  |  / / /_  /      
/ /_/ / ____/ /_  /___  _  _, _/_  /_/ // /_/ /_  /       
\____/  /____/ /_____/  /_/ |_| /_____/ \____/ /_/        
                                                          ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""
print(FinalSN.__copyright__)
print("Licensed under the terms of the " + FinalSN.__license__)
print(imam_ali)
cmdhr = Config.COMMAND_HAND_LER

try:
    LOGS.info("جارِ بدء بوت فـاينل ✓")
    final313.loop.run_until_complete(setup_bot())
    LOGS.info("تم اكتمال تنصيب البوت ✓")
except Exception as e:
    LOGS.error(f"{str(e)}")
    sys.exit()

try:
    LOGS.info("يتم تفعيل وضع الانلاين")
    final313.loop.run_until_complete(mybot())
    LOGS.info("تم تفعيل وضع الانلاين بنجاح ✓")
except Exception as jep:
    LOGS.error(f"- {jep}")
    sys.exit()    

async def startup_process():
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    print("⌁⌁︙بـوت فـاينل يعـمل بـنجاح ")
    print(
        f"تم تشغيل الانلاين تلقائياً ارسل {cmdhr}الاوامر لـرؤيـة اوامر السورس\
        \nللمسـاعدة تواصـل  https://t.me/z3zz_zSupport"
    )
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    await verifyLoggerGroup()
    await saves()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    return

async def externalrepo():
    if Config.VCMODE:
        await install_externalrepo("https://github.com/z3zz_ziq/JepVc", "jepvc", "z3zz_zvc")

final313.loop.run_until_complete(externalrepo())
final313.loop.run_until_complete(startup_process())

if len(sys.argv) in {1, 3, 4}:
    with contextlib.suppress(ConnectionError):
        final313.run_until_disconnected()
else:
    final313.disconnect()
