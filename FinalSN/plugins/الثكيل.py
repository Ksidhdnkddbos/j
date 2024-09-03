#ربي اشرح لي صدري
#تمت كتابة الكود من قبل السيد حسين @i0i0ii
#فريق فـاينل @z3zz_z
import asyncio
from telethon import events
from FinalSN import final313
sajad_enabled = False
alvipfinal_enabled = False
JOKER_ID = {}

@final313.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def mark_as_read(event):
    global alvipfinal_enabled, JOKER_ID
    sender_id = event.sender_id
    if alvipfinal_enabled and sender_id in JOKER_ID:
        vipfinal_time = JOKER_ID[sender_id]
        if vipfinal_time > 0:
            await asyncio.sleep(vipfinal_time)
        await event.mark_read()

@final313.on(events.NewMessage(outgoing=True, pattern=r'^\.التكبر تعطيل$'))
async def ffinal(event):
    global alvipfinal_enabled
    alvipfinal_enabled = False
    await event.edit('**⌁⌁︙ تم تعطيل امر التكبر بنجاح ✅**')

@final313.on(events.NewMessage(outgoing=True, pattern=r'^\.التكبر (\d+) (\d+)$'))
async def ffinal(event):
    global alvipfinal_enabled, JOKER_ID
    vipfinal_time = int(event.pattern_match.group(1))
    user_id = int(event.pattern_match.group(2)) 
    JOKER_ID[user_id] = vipfinal_time
    alvipfinal_enabled = True
    await event.edit(f'**⌁⌁︙ تم تفعيل امر التكبر بنجاح مع  {vipfinal_time} ثانية للمستخدم {user_id}**')

@final313.on(events.NewMessage(outgoing=True, pattern=r'^\.مود التكبر تعطيل$'))
async def ffinal(event):
    global sajad_enabled
    sajad_enabled = False
    await event.edit('**⌁⌁︙ تم تعطيل امر التكبر على الجميع بنجاح ✅**')
    
@final313.on(admin_cmd(pattern=f"مود التكبر (\d+)"))
async def ffinal(event):
    global sajad_enabled, sajad_time
    sajad_time = int(event.pattern_match.group(1))
    sajad_enabled = True
    await event.edit(f'**⌁⌁︙ تم تفعيل امر التكبر بنجاح مع  {sajad_time} ثانية**')

@final313.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def ffinal(event):
    global sajad_enabled, sajad_time
    if sajad_enabled:
        await asyncio.sleep(sajad_time)
        await event.mark_read()
