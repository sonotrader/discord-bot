import discord
from discord.ext import commands, tasks
from datetime import datetime
import pytz
import os

# ===== الإعدادات - عدّل القيم هنا =====
TOKEN      = os.environ.get("DISCORD_TOKEN")
# السيرفر الأول
CHANNEL_ID  = 1513501351307378810
ROLE_ID     = 1513487411500290099

# السيرفر الثاني
CHANNEL_ID2 = 1512868995563524256
ROLE_ID2    = 1511784648563228702
TIMEZONE   = "Asia/Riyadh"
# =======================================

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tz  = pytz.timezone(TIMEZONE)


async def send_to_all(embed, with_mention=True):
    targets = [
        (CHANNEL_ID,  ROLE_ID),
        (CHANNEL_ID2, ROLE_ID2),
    ]
    for ch_id, role_id in targets:
        channel = bot.get_channel(ch_id)
        if not channel:
            continue
        role    = channel.guild.get_role(role_id)
        mention = role.mention if role else "@member"
        await channel.send(content=mention if with_mention else None, embed=embed)


@tasks.loop(minutes=1)
async def check_reminders():
    now     = datetime.now(tz)
    weekday = now.weekday()   # 0=Mon 1=Tue 2=Wed 3=Thu 4=Fri 5=Sat 6=Sun

    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        return

    # ── 1. Party — يومي الساعة 8:00 م ─────────────────────────────
    if now.hour == 20 and now.minute == 0:
        embed = discord.Embed(
            title="🎉 Party Time!",
            description=(
                "The **Party** event is starting now!\n"
                "Gather up and let's go! 🕹️"
            ),
            color=discord.Color.gold()
        )
        embed.set_footer(text="📅 Daily Event • 8:00 PM")
        await send_to_all(embed)

    # ── 2. Breaking Army — الأربعاء والسبت ─────────────────────────
    #    تذكير قبل البداية الساعة 4:45 م
    if weekday in (2, 5) and now.hour == 16 and now.minute == 45:
        embed = discord.Embed(
            title="⚔️ Breaking Army — Starting Soon!",
            description=(
                "**Breaking Army** kicks off in **15 minutes**!\n"
                "Get ready and join the battle! 💪"
            ),
            color=discord.Color.red()
        )
        embed.add_field(name="🕔 Start", value="5:00 PM", inline=True)
        embed.add_field(name="🕖 End",   value="7:00 PM", inline=True)
        embed.set_footer(text="📅 Wednesday & Saturday")
        await send_to_all(embed)

    #    إعلان البداية الساعة 5:00 م
    if weekday in (2, 5) and now.hour == 17 and now.minute == 0:
        embed = discord.Embed(
            title="⚔️ Breaking Army — Let's GO!",
            description=(
                "**Breaking Army** has started!\n"
                "Don't be late — join now! 🔥"
            ),
            color=discord.Color.dark_red()
        )
        embed.set_footer(text="Ends at 7:00 PM")
        await send_to_all(embed)

    #    إعلان النهاية الساعة 7:00 م
    if weekday in (2, 5) and now.hour == 19 and now.minute == 0:
        embed = discord.Embed(
            title="⚔️ Breaking Army — Event Ended",
            description="**Breaking Army** has ended. Great effort everyone! 🏆",
            color=discord.Color.greyple()
        )
        embed.set_footer(text="📅 Wednesday & Saturday")
        await send_to_all(embed)

    # ── 5. GVG Guild War — السبت والأحد ────────────────────────────
    #    تذكير قبل البداية الساعة 9:00 م
    if weekday in (5, 6) and now.hour == 21 and now.minute == 0:
        embed = discord.Embed(
            title="🏰 GVG Guild War — Starting in 15 Minutes!",
            description=(
                "⚠️ **Guild War (GVG) begins in 15 minutes!**\n\n"
                "📌 Make sure to **follow the instructions** sent previously in the server!\n"
                "Your coordination and discipline are key to victory! 🗡️🛡️"
            ),
            color=discord.Color.dark_gold()
        )
        embed.add_field(name="🕘 Start", value="9:15 PM",  inline=True)
        embed.add_field(name="🕛 End",   value="12:00 AM", inline=True)
        embed.set_footer(text="📅 Saturday & Sunday")
        await send_to_all(embed)

    #    إعلان البداية الساعة 9:15 م
    if weekday in (5, 6) and now.hour == 21 and now.minute == 15:
        embed = discord.Embed(
            title="🏰 GVG Guild War — STARTING NOW! ⚔️",
            description=(
                "🚨 **Guild War has begun!**\n\n"
                "📋 **Follow the instructions** shared in the server — no improvisation!\n"
                "Stay focused, stay coordinated, and fight for the guild! 💪🔥"
            ),
            color=discord.Color.brand_red()
        )
        embed.set_footer(text="Ends at 12:00 AM • Sat & Sun")
        await send_to_all(embed)

    #    إعلان النهاية الساعة 12:00 ص
    if weekday in (5, 6) and now.hour == 0 and now.minute == 0:
        embed = discord.Embed(
            title="🏰 GVG Guild War — Ended",
            description=(
                "**Guild War is over!** Great fight everyone! 🏆\n"
                "Rest up and get ready for the next battle! 💤"
            ),
            color=discord.Color.greyple()
        )
        embed.set_footer(text="📅 Saturday & Sunday")
        await send_to_all(embed)

    # ── 3. Showdown — الخميس والأحد ────────────────────────────────
    #    تذكير قبل البداية الساعة 4:45 م
    if weekday in (3, 6) and now.hour == 16 and now.minute == 45:
        embed = discord.Embed(
            title="🏆 Showdown — Starting Soon!",
            description=(
                "**Showdown** begins in **15 minutes**!\n"
                "Prepare yourself and get in position! ⚡"
            ),
            color=discord.Color.purple()
        )
        embed.add_field(name="🕔 Start", value="5:00 PM", inline=True)
        embed.add_field(name="🕖 End",   value="7:00 PM", inline=True)
        embed.set_footer(text="📅 Thursday & Sunday")
        await send_to_all(embed)

    #    إعلان البداية الساعة 5:00 م
    if weekday in (3, 6) and now.hour == 17 and now.minute == 0:
        embed = discord.Embed(
            title="🏆 Showdown — Starting Now!",
            description=(
                "**Showdown** has begun!\n"
                "Give it your all — good luck! 🎯"
            ),
            color=discord.Color.dark_purple()
        )
        embed.set_footer(text="Ends at 7:00 PM")
        await send_to_all(embed)

    #    إعلان النهاية الساعة 7:00 م
    if weekday in (3, 6) and now.hour == 19 and now.minute == 0:
        embed = discord.Embed(
            title="🏆 Showdown — Event Ended",
            description="**Showdown** is over. Well played everyone! 🥇",
            color=discord.Color.greyple()
        )
        embed.set_footer(text="📅 Thursday & Sunday")
        await send_to_all(embed)

    # ── 4. Daily Tasks Reminder — يومي الساعة 8:00 م (مع Party) ───
    if now.hour == 20 and now.minute == 0:
        embed = discord.Embed(
            title="📋 Daily Tasks Reminder",
            description=(
                "Hey everyone! Don't forget to **complete your daily tasks** in the guild! ✅\n\n"
                "Need help with a task? **Reach out to us** and we'll be happy to assist you! 🤝\n\n"
                "*Stay active, stay strong — together we grow!* 💪"
            ),
            color=discord.Color.green()
        )
        embed.set_footer(text="📅 Daily Reminder")
        await send_to_all(embed, with_mention=False)   # بدون منشن عشان ما يتكرر مع Party


# ── عند تشغيل البوت ────────────────────────────────────────────────

@bot.event
async def on_ready():
    print(f"✅ Bot is online: {bot.user}")
    check_reminders.start()


# ── أمر: عرض جدول اليوم ────────────────────────────────────────────

@bot.command(name="schedule")
async def schedule(ctx):
    now     = datetime.now(tz)
    weekday = now.weekday()
    days    = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    embed = discord.Embed(
        title=f"📅 Today's Schedule — {days[weekday]}",
        color=discord.Color.blue()
    )
    embed.add_field(name="🎉 Party",               value="Every day  •  8:00 PM",             inline=False)
    embed.add_field(name="📋 Daily Tasks Reminder", value="Every day  •  8:00 PM",            inline=False)
    embed.add_field(name="⚔️ Breaking Army",      value="Wed & Sat  •  5:00 PM → 7:00 PM",   inline=False)
    embed.add_field(name="🏆 Showdown",           value="Thu & Sun  •  5:00 PM → 7:00 PM",   inline=False)
    embed.add_field(name="🏰 GVG Guild War",      value="Sat & Sun  •  9:15 PM → 12:00 AM",  inline=False)
    embed.set_footer(text="All times are Saudi Arabia time (GMT+3)")
    await ctx.send(embed=embed)


bot.run(TOKEN)
