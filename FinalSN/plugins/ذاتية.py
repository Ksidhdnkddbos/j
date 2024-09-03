from FinalSN import final313
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
import os
import datetime
from telethon import events
from FinalSN import *
#ها يالفاشل شعدك داخل هنا 🫣 اعتمد ع نفسك لتخلي سورس فـاينل مصدر طشت سورسك
finalv_Asbo3 = {
    'Monday': 'الاثنين',
    'Tuesday': 'الثلاثاء',
    'Wednesday': 'الأربعاء',
    'Thursday': 'الخميس',
    'Friday': 'الجمعة',
    'Saturday': 'السبت',
    'Sunday': 'الأحد'
}

@final313.on(admin_cmd(pattern="(جلب الصورة|جلب الصوره|ذاتيه|ذاتية)"))
async def dato(event):
    if not event.is_reply:
        return await event.edit("..")
    i0i0ii = await event.get_reply_message()
    pic = await i0i0ii.download_media()
    await bot.send_file(
        "me",
        pic,
        caption=f"""
- تـم حفظ الصـورة بنجـاح ✓ 
- غير مبري الذمه اذا استخدمت الامر للابتزاز
- CH: @Z3ZZ_Z
- Dev: @i0i0ii
  """,
    )
    await event.delete()
#By @z3zz_z For You 🌹
@final313.on(admin_cmd(pattern="(الذاتية تشغيل|ذاتية تشغيل)"))
async def reda(event):
    if gvarstatus ("savepicforme"):
        return await edit_delete(event, "**⌁⌁︙حفظ الذاتيات مفعل وليس بحاجة للتفعيل مجدداً **")
    else:
        addgvar("savepicforme", "reda")
        await edit_delete(event, "**⌁⌁︙تم تفعيل ميزة حفظ الذاتيات بنجاح ✓**")
 
@final313.on(admin_cmd(pattern="(الذاتية تعطيل|ذاتية تعطيل)"))
async def F16_Is_Here(event):
    if gvarstatus ("savepicforme"):
        delgvar("savepicforme")
        return await edit_delete(event, "**⌁⌁︙تم تعطيل حفظت الذاتيات بنجاح ✓**")
    else:
        await edit_delete(event, "**⌁⌁︙انت لم تفعل حفظ الذاتيات لتعطيلها!**")

def vipfinal_unread_media(message):
    return message.media_unread and (message.photo or message.video)

async def ffinal(event, caption):
    media = await event.download_media()
    sender = await event.get_sender()
    sender_id = event.sender_id
    i0i0ii_date = event.date.strftime("%Y-%m-%d")
    i0i0ii_day = finalv_Asbo3[event.date.strftime("%A")]
    await bot.send_file(
        "me",
        media,
        caption=caption.format(sender.first_name, sender_id, i0i0ii_date, i0i0ii_day),
        parse_mode="markdown"
    )
    os.remove(media)

@final313.on(events.NewMessage(func=lambda e: e.is_private and vipfinal_unread_media(e) and e.sender_id != bot.uid))
async def F16(event):
    if gvarstatus("savepicforme"):
        caption = """**
           ♡  غير مبري الذمة اذا استعملته للأبتزاز  ♡
♡ تم حفظ الذاتية بنجاح ✓
♡ تم الصنع : @Z3ZZ_Z
♡ أسم المرسل : [{0}](tg://user?id={1})
♡  تاريخ الذاتية : `{2}`
♡  أرسلت في يوم `{3}`
       ♡    ALJOKER    ♡
        **"""
        await ffinal(event, caption)