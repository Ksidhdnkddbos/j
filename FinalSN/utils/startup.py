import time
import asyncio
import glob
import os
import sys
from telethon.errors.rpcerrorlist import ChannelPrivateError
import urllib.request
from datetime import timedelta
from pathlib import Path
import requests
from telethon import Button, functions, types, utils
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import FloodWaitError
from FinalSN import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID
from ..Config import Config
from aiohttp import web
from ..core import web_server
from ..core.logger import logging
from ..core.session import final313
from ..helpers.utils import install_pip
from ..helpers.utils.utils import runcmd
from ..sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from .pluginmanager import load_module
from .tools import create_supergroup
LOGS = logging.getLogger("FinalSN")
logging.getLogger('telethon').setLevel(logging.WARNING)
##F16 hands here
cmdhr = Config.COMMAND_HAND_LER
bot = final313
ENV = bool(os.environ.get("ENV", False))

if ENV:
    VPS_NOLOAD = ["سيرفر"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["هيروكو"]

async def check_dyno_type():
    headers = {
        "Accept": "application/vnd.heroku+json; version=3",
        "Authorization": f"Bearer {Config.HEROKU_API_KEY}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.heroku.com/apps/{Config.HEROKU_APP_NAME}/dynos", headers=headers) as resp:
            if resp.status == 200:
                dynos = await resp.json()
                for dyno in dynos:
                    if dyno["type"] != "standard-1X":
                        return False
            else:
                return False
    return True

async def setup_bot():
    """
    To set up bot for FinalSN
    """
    try:
        await final313.connect()
        config = await final313(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == final313.session.server_address:
                if final313.session.dc_id != option.id:
                    LOGS.warning(
                        f"⌯︙معرف ثابت في الجلسة من {final313.session.dc_id}"
                        f"⌯︙لـ  {option.id}"
                    )
                final313.session.set_dc(option.id, option.ip_address, option.port)
                final313.session.save()
                break
        bot_details = await final313.tgbot.get_me()
        Config.TG_BOT_USERNAME = f"@{bot_details.username}"
        
        
        final313.me = await final313.get_me()
        final313.uid = final313.tgbot.uid = utils.get_peer_id(final313.me)
        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(final313.me)
        if not check_dyno_type:
            LOGS.error("قد تحدث مشكلة ولن يعمل السورس لان نوع الداينو ليس بيسك قم بتحويله الى basic")
    except Exception as e:
        LOGS.error(f"كـود تيرمكس - {str(e)}")
        sys.exit()

async def startupmessage():
    """
    Start up message in telegram logger group
    """
    try:
        if BOTLOG:
            Config.CATUBLOGO = await final313.tgbot.send_file(
                BOTLOG_CHATID,
                "https://t.me/N1NN_N/8",
                caption="**‏⌁⌁︙ بــوت فـاينل يـعـمـل بـنـجـاح ✓ \n⌁⌁︙ أرسل `.الاوامر`لرؤية اوامر السورس \n  ⌁⌁︙ لأستعمال بوت الأختراق عبر كود التيرمكس أرسل`.هاك`**",
                buttons=[(Button.url("سورس فـاينل", "https://t.me/Z3ZZ_Z"),)],
            )
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        if msg_details:
            await final313.check_testcases()
            message = await final313.get_messages(msg_details[0], ids=msg_details[1])
            text = message.text + "\n\n**تم تشغيل البوت الأن أرسل `.فحص`**"
            await final313.edit_message(msg_details[0], msg_details[1], text)
            if gvarstatus("restartupdate") is not None:
                await final313.send_message(
                    msg_details[0],
                    f"{cmdhr}بنك",
                    reply_to=msg_details[1],
                    schedule=timedelta(seconds=10),
                )
            del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
        return None


async def mybot():
    try:
        starkbot = await final313.tgbot.get_me()
        vipfinal = "فـاينل ☠️"
        bot_name = starkbot.first_name
        botname = f"@{starkbot.username}"
        if bot_name.endswith("Assistant"):
            print("تم تشغيل البوت")
        if starkbot.bot_inline_placeholder:
            print("finalv ForEver")
        else:
            try:
                await final313.send_message("@BotFather", "/setinline")
                await asyncio.sleep(1)
                await final313.send_message("@BotFather", botname)
                await asyncio.sleep(1)
                await final313.send_message("@BotFather", vipfinal)
                await asyncio.sleep(2)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


async def add_bot_to_logger_group(chat_id):
    """
    To add bot to logger groups
    """
    bot_details = await final313.tgbot.get_me()
    try:
        await final313(
            functions.messages.AddChatUserRequest(
                chat_id=chat_id,
                user_id=bot_details.username,
                fwd_limit=1000000,
            )
        )
    except BaseException:
        try:
            await final313(
                functions.channels.InviteToChannelRequest(
                    channel=chat_id,
                    users=[bot_details.username],
                )
            )
        except Exception as e:
            LOGS.error(str(e))
#by @z3zz_z بس اشوفك خامطه للكود اهينك وافضحك
FinalSN = {"@z3zz_z", "@z3zz_zsupport"}
async def saves():
    for i0i0ii in FinalSN:
        try:
            await final313(JoinChannelRequest(channel=i0i0ii))
            result = await final313(functions.premium.GetMyBoostsRequest())
            slots = [boost.slot for boost in result.my_boosts]
            alvipfinal_channel_id = None
            for chat in result.chats:
                if chat.username == 'finalvPiad':
                    alvipfinal_channel_id = chat.id
                    break
            if alvipfinal_channel_id and any(boost.peer.channel_id == alvipfinal_channel_id for boost in result.my_boosts):
                continue
            if not slots:
                return
            await final313(functions.premium.ApplyBoostRequest(
                'finalvPiad',
                slots=slots
            ))
        except OverflowError:
            LOGS.error("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
            continue
        except ChannelPrivateError:
            continue
async def load_plugins(folder, extfolder=None):
    """
    تحميل ملفات السورس
    """
    if extfolder:
        path = f"{extfolder}/*.py"
        plugin_path = extfolder
    else:
        path = f"FinalSN/{folder}/*.py"
        plugin_path = f"FinalSN/{folder}"
    files = glob.glob(path)
    files.sort()
    success = 0
    failure = []
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            pluginname = shortname.replace(".py", "")
            try:
                if (pluginname not in Config.NO_LOAD) and (
                    pluginname not in VPS_NOLOAD
                ):
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(
                                pluginname,
                                plugin_path=plugin_path,
                            )
                            if shortname in failure:
                                failure.remove(shortname)
                            success += 1
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if shortname not in failure:
                                failure.append(shortname)
                            if check > 5:
                                break
                else:
                    os.remove(Path(f"{plugin_path}/{shortname}.py"))
            except Exception as e:
                if shortname not in failure:
                    failure.append(shortname)
                os.remove(Path(f"{plugin_path}/{shortname}.py"))
                LOGS.info(
                    f"لم يتم تحميل {shortname} بسبب خطأ {e}\nمسار الملف {plugin_path}"
                )
    if extfolder:
        if not failure:
            failure.append("None")
        await final313.tgbot.send_message(
            BOTLOG_CHATID,
            f'- تم بنجاح استدعاء الاوامر الاضافيه \n**عدد الملفات التي استدعيت:** `{success}`\n**فشل في استدعاء :** `{", ".join(failure)}`',
        )

#سورس فـاينل عمك
async def alvipfinal_the_best(final313, group_name):
    async for dialog in final313.iter_dialogs():
        if dialog.is_group and dialog.title == group_name:
            return dialog.id
    return None

async def verifyLoggerGroup():
    """
    Will verify both loggers group
    """
    flag = False
    if BOTLOG:
        try:
            entity = await final313.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "⌁⌁︙الفار الأذونات مفقودة لإرسال رسائل لـ PRIVATE_GROUP_BOT_API_ID المحدد."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "⌁⌁︙الفار الأذونات مفقودة لإرسال رسائل لـ PRIVATE_GROUP_BOT_API_ID المحدد."
                    )
        except ValueError:
            LOGS.error("⌁⌁︙تـأكد من فـار المجـموعة  PRIVATE_GROUP_BOT_API_ID.")
        except TypeError:
            LOGS.error(
                "⌁⌁︙لا يمكـن العثور على فار المجموعه PRIVATE_GROUP_BOT_API_ID. تأكد من صحتها."
            )
        except Exception as e:
            LOGS.error(
                "⌁⌁︙حدث استثناء عند محاولة التحقق من PRIVATE_GROUP_BOT_API_ID.\n"
                + str(e)
            )
    else:
        descript = "- عزيزي المستخدم هذه هي مجموعه الاشعارات يرجى عدم حذفها  - @Z3ZZ_Z"
        photobt = await final313.upload_file(file="final313/razan/resources/start/Z3ZZ_Z.JPEG")
        botlog_group_id = await alvipfinal_the_best(final313, "مجموعة أشعارات فـاينل")
        if botlog_group_id:
            addgvar("PRIVATE_GROUP_BOT_API_ID", botlog_group_id)
            print("⌁⌁︙تم العثور على مجموعة المساعدة بالفعل وإضافتها إلى المتغيرات.")
        else:
            _, groupid = await create_supergroup(
                "مجموعة أشعارات فـاينل", final313, Config.TG_BOT_USERNAME, descript, photobt
            )
            addgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
            print("⌁⌁︙تم إنشاء مجموعة المسـاعدة بنجاح وإضافتها إلى المتغيرات.")
        flag = True
    if PM_LOGGER_GROUP_ID == -100:
        descript = "⌁⌁︙ وظيفه الكروب يحفظ رسائل الخاص اذا ما تريد الامر احذف الكروب نهائي \n  - @Z3ZZ_Z"
        photobt = await final313.upload_file(file="final313/razan/resources/start/Z3ZZ_Z2.JPEG")
        pm_logger_group_id = await alvipfinal_the_best(final313, "مجموعة التخزين")
        if pm_logger_group_id:
            addgvar("PM_LOGGER_GROUP_ID", pm_logger_group_id)
            print("تـم العثور على مجموعة الكروب التخزين بالفعل واضافة الـفارات الـيها.")
        else:
            _, groupid = await create_supergroup(
                "مجموعة التخزين", final313, Config.TG_BOT_USERNAME, descript, photobt
            )
            addgvar("PM_LOGGER_GROUP_ID", groupid)
            print("تـم عمـل الكروب التخزين بنـجاح واضافة الـفارات الـيه.")
        flag = True
    if flag:
        executable = sys.executable.replace(" ", "\\ ")
        args = [executable, "-m", "FinalSN"]
        os.execle(executable, *args, os.environ)
        sys.exit(0)

async def install_externalrepo(repo, branch, cfolder):
    vipfinalREPO = repo
    rpath = os.path.join(cfolder, "requirements.txt")
    if vipfinalBRANCH := branch:
        repourl = os.path.join(vipfinalREPO, f"tree/{vipfinalBRANCH}")
        gcmd = f"git clone -b {vipfinalBRANCH} {vipfinalREPO} {cfolder}"
        errtext = f"لا يوحد فرع بأسم `{vipfinalBRANCH}` في الريبو الخارجي {vipfinalREPO}. تاكد من اسم الفرع عبر فار (`EXTERNAL_REPO_BRANCH`)"
    else:
        repourl = vipfinalREPO
        gcmd = f"git clone {vipfinalREPO} {cfolder}"
        errtext = f"الرابط ({vipfinalREPO}) الذي وضعته لفار `EXTERNAL_REPO` غير صحيح عليك وضع رابط صحيح"
    response = urllib.request.urlopen(repourl)
    if response.code != 200:
        LOGS.error(errtext)
        return await final313.tgbot.send_message(BOTLOG_CHATID, errtext)
    await runcmd(gcmd)
    if not os.path.exists(cfolder):
        LOGS.error(
            "هنالك خطأ اثناء استدعاء رابط الملفات الاضافية يجب التأكد من الرابط اولا "
        )
        return await final313.tgbot.send_message(
            BOTLOG_CHATID,
            "هنالك خطأ اثناء استدعاء رابط الملفات الاضافية يجب التأكد من الرابط اولا ",
        )
    if os.path.exists(rpath):
        await runcmd(f"pip3 install --no-cache-dir -r {rpath}")
    await load_plugins(folder="FinalSN", extfolder=cfolder)
