# -*- coding: utf-8 -*-
"""TZ FX BOT — centralized Persian / English UI strings.

Business logic stays in bot.py. Call t(lang, key, **kwargs).
Default language is Persian (fa). English is a first-class catalog, not a fallback.
"""
from __future__ import print_function

FA = {
    "lang.name": u"فارسی",
    "lang.other": u"English",
    "brand.foot": u"آموزشی است · مشاوره مالی نیست",
    "brand.disclaimer": u"آموزشی است · حد ضرر اجباری · حداکثر ۱٪ · سود تضمینی نیست.",
    "head.home": u"خانه",
    "head.join": u"عضویت",
    "head.sub": u"اشتراک",
    "head.learn": u"آموزش",
    "head.crypto": u"کریپتو بتا",
    "head.desk": u"میز",
    "head.paper": u"پیپر",
    "head.connect": u"اتصال",
    "head.wr": u"وین‌ریت واقعی",
    "head.coach": u"مربی",
    "head.support": u"پشتیبانی",
    "head.signal": u"سیگنال",
    "btn.miniapp": u"🎮 مینی‌اپ",
    "btn.eur": u"💶 یورو",
    "btn.gbp": u"💷 پوند",
    "btn.xau": u"🥇 طلا",
    "btn.crypto": u"₿ کریپتو",
    "btn.all3": u"📡 هر ۳ نماد",
    "btn.coach": u"🎙️ مربی",
    "btn.learn": u"🎓 آموزش",
    "btn.wr": u"📊 وین‌ریت",
    "btn.sub": u"💎 اشتراک",
    "btn.support": u"🛟 پشتیبانی",
    "btn.connect": u"🔗 اتصال",
    "btn.paper": u"🤖 پیپر",
    "btn.home": u"🏠 خانه",
    "btn.hear": u"🔊 بشنو",
    "btn.lang": u"🌐 English",
    "btn.join_ch": u"📣 عضویت کانال TZ FX",
    "btn.joined": u"✅ عضو شدم",
    "btn.free_ch": u"📣 کانال رایگان",
    "btn.desk": u"🧰 میز",
    "btn.radar": u"🛰️ رادار",
    "btn.session": u"🕒 سشن",
    "btn.journal": u"📒 ژورنال",
    "btn.paper_on": u"▶️ روشن",
    "btn.paper_off": u"⏸ خاموش",
    "btn.paper_reset": u"↺ ریست ۱۰٬۰۰۰",
    "btn.hot": u"🔥 داغ‌ترین",
    "btn.find_coin": u"🔎 اسم کوین را بفرست",
    "btn.crypto_radar": u"🛰️ رادار محبوب",
    "btn.crypto_brief": u"🌍 حال کوین",
    "btn.crypto_core": u"📡 سیگنال محبوب‌ها",
    "btn.crypto_ch": u"📣 کانال TZ Crypto",
    "btn.lvl1": u"🟢 سطح ۱ — مبتدی از صفر",
    "btn.lvl2": u"🔵 سطح ۲ — ICT پایه",
    "btn.lvl3": u"🟣 سطح ۳ — ICT پیشرفته",
    "btn.lvl4": u"🟡 سطح ۴ — اجرا و ذهن",
    "btn.lvl5": u"🔗 سطح ۵ — API و اتصال",
    "btn.ask_all": u"💬 از مربی بپرس (کل دوره)",
    "btn.ask_level": u"💬 سوال از مربی همین سطح",
    "btn.ask_lesson": u"💬 سوالت را بپرس — مربی همین درس",
    "btn.hear_lesson": u"🔊 این درس را بشنو",
    "btn.catalog": u"📚 فهرست",
    "btn.prev": u"⬅️ قبلی",
    "btn.next": u"بعدی ➡️",
    "btn.same_level": u"📚 همین سطح",
    "btn.go_connect": u"🔗 رفتن به اتصال",
    "btn.refresh": u"🔄 بروزرسانی",
    "btn.open_pos": u"📡 معاملات باز",
    "txt.start": u"%s تهران\nفارکس: یورو · پوند · طلا\nکریپتو بتا: هر کوین USDT — اسم را بفرست\n\nسیگنال الکی نیست. حد ضرر اجباری.\nکانال رایگان @TZ_FX_CH",
    "txt.help": u"/signal سیگنال\n/crypto کوین\n/connect اتصال\n/paper پیپر\n/learn آموزش\n/wr وین‌ریت\n/lang زبان\n\nویس بفرست — مربی جواب می‌دهد.",
    "txt.join": u"اول کانال رایگان را عضو شو، بعد «عضو شدم» را بزن.\nسیگنال کامل با اشتراک است.",
    "txt.paywall_active": u"اشتراک فعال تا %s · حدود %s روز مانده",
    "txt.paywall_none": u"اشتراک نداری",
    "txt.paywall_body": u"سیگنال کامل، چارت، مربی و VIP فقط با اشتراک.\nپلن → واریز کارت → عکس رسید همین‌جا.\nلینک VIP بعد از تایید.",
    "txt.me_on": u"فعال تا %s · %s روز\nVIP: %s\nپاک کردن حافظه مربی: /forget",
    "txt.me_off": u"فعال نیست. برای سیگنال کامل اشتراک بگیر.",
    "txt.crypto": u"%s کوین اسپات USDT.\nاسم را بفرست یا از داغ‌ترین انتخاب کن.\nهندسه همان ICT است — بتا، قول سود نیست.\nکانال: %s",
    "txt.desk": u"رادار · سشن · ژورنال · پیپر · اتصال",
    "txt.connect": u"دمو است. سفارش به حساب واقعی نمی‌رود.\nصرافی: <b>%s</b> · کلید %s\nMT5: %s\nریسک ۱٪ · حد ضرر اجباری",
    "txt.connect_ready": u"اتصال آماده است. صرافی را بزن، بعد کلید.",
    "txt.edu_intro": u"ICT ۲۰۲۲ از صفر تا اجرا.\nدرس را باز کن. API و اتصال در سطح ۵.",
    "txt.gate_join": u"اول کانال را عضو شو",
    "txt.gate_pay": u"اشتراک لازم است",
    "txt.coach_hello": u"🎙️ سلام %s، مربی خودتم.\nنماد محبوب: <b>%s</b>%s\n\nبنویس یا ویس بفرست — جواب متن و ویس است.",
    "txt.coach_hello_speak": u"سلام %s. مربی خودتی. بنویس یا ویس بفرست.",
    "txt.coach_mem": u"\nحرف‌های قبلی‌ات یادم هست — مال خودت است، با بقیه قاطی نمی‌شود.",
    "txt.coach_busy": u"الان مربی شلوغ است. کمی بعد دوباره بپرس.",
    "txt.coach_empty": u"پیام خالی است",
    "txt.coach_wait": u"یک لحظه صبر کن",
    "txt.coach_quota": u"سهم چت این ساعت پر شد",
    "txt.forget": u"🧹 حافظه مربی مخصوص تو پاک شد.\nاز این به بعد از صفر می‌شناسیمت — مال بقیه دست نمی‌خورد.",
    "txt.watch_on": u"👀 خبررسان روشن شد. ستاپ کامل ICT ۲۰۲۲ را همین‌جا می‌فرستم.",
    "txt.watch_off": u"👀 خبررسان خاموش شد.",
    "txt.lang_set_fa": u"زبان: فارسی",
    "txt.lang_set_en": u"Language: English",
    "txt.wait": u"صبر",
    "txt.buy": u"بخر",
    "txt.sell": u"بفروش",
    "txt.no_signal": u"ستاپ ICT ۲۰۲۲ هنوز کامل نشده — تعقیب نکن.",
    "txt.paper_demo": u"آزمایشی است · پول واقعی نیست · ریسک ۱٪ · حد ضرر اجباری",
    "txt.paper_on": u"روشن",
    "txt.paper_off": u"خاموش",
    "txt.wr_line": u"از حد سود و حد ضرر واقعی. درصد الکی نمی‌نویسم.",
    "txt.wr_empty": u"هنوز سیگنال بسته‌شده‌ای تو دفتر جدید نیست.",
    "txt.all_coins": u"همه",
    "txt.fx_closed": u"فارکس بسته است",
    "txt.fx_open": u"فارکس باز است",
    "cmd.start": u"خانه",
    "cmd.signal": u"سیگنال",
    "cmd.crypto": u"کریپتو",
    "cmd.connect": u"اتصال صرافی/بروکر",
    "cmd.paper": u"پیپر",
    "cmd.learn": u"آموزش",
    "cmd.wr": u"وین‌ریت",
    "cmd.help": u"راهنما",
    "cmd.lang": u"زبان / Language",
    "cmd.desk": u"میز",
    "cmd.support": u"پشتیبانی",
    "ai.sys": (
        u"تو مربی TZ FX هستی. مرد فارسی‌زبان، گرم، رک، کوتاه مثل ویس. "
        u"کنار همین یک شاگرد نشسته‌ای. ربات‌بازی نکن. "
        u"دو میز: ۱) فارکس ICT منتورشیپ ۲۰۲۲ — فقط EURUSD، GBPUSD، XAUUSD. "
        u"شنبه و یکشنبه فارکس بسته است؛ صادق بگو. پنجره سیگنال کانال فارکس ۸:۳۰–۲۰:۳۰ تهران. "
        u"۲) کریپتو بتا — هر کوین اسپات USDT. همان هندسه: Judas سوئیپ → MSS → FVG → ورود داخل شکاف، حد ضرر پشت ویک. "
        u"کریپتو ۲۴/۷ است و بتا؛ قول ICT مایکل روی کوین نده. "
        u"سیگنال الکی نساز. قیمت از خودت درنیار. فقط اگر در «داده بازار» آمده همان را بگو. "
        u"بدون حد ضرر ورود نده. امتیاز زیر ۴ یا خلاف روزانه = صبر. "
        u"قول سود و درصد دقت الکی ممنوع. حافظه فقط همین شاگرد. "
        u"جمله کوتاه، قابل ویس، بدون جدول و ستاره."
    ),
}

EN = {
    "lang.name": u"English",
    "lang.other": u"فارسی",
    "brand.foot": u"Educational · not financial advice",
    "brand.disclaimer": u"Educational · stop loss required · max 1% risk · no guaranteed profit.",
    "head.home": u"Home",
    "head.join": u"Join",
    "head.sub": u"Subscription",
    "head.learn": u"Education",
    "head.crypto": u"Crypto beta",
    "head.desk": u"Desk",
    "head.paper": u"Paper",
    "head.connect": u"Connect",
    "head.wr": u"Real win-rate",
    "head.coach": u"Mentor",
    "head.support": u"Support",
    "head.signal": u"Signal",
    "btn.miniapp": u"🎮 Mini App",
    "btn.eur": u"💶 EUR",
    "btn.gbp": u"💷 GBP",
    "btn.xau": u"🥇 Gold",
    "btn.crypto": u"₿ Crypto",
    "btn.all3": u"📡 All 3 FX",
    "btn.coach": u"🎙️ Mentor",
    "btn.learn": u"🎓 Learn",
    "btn.wr": u"📊 Win-rate",
    "btn.sub": u"💎 Subscribe",
    "btn.support": u"🛟 Support",
    "btn.connect": u"🔗 Connect",
    "btn.paper": u"🤖 Paper",
    "btn.home": u"🏠 Home",
    "btn.hear": u"🔊 Listen",
    "btn.lang": u"🌐 فارسی",
    "btn.join_ch": u"📣 Join TZ FX channel",
    "btn.joined": u"✅ I joined",
    "btn.free_ch": u"📣 Free channel",
    "btn.desk": u"🧰 Desk",
    "btn.radar": u"🛰️ Radar",
    "btn.session": u"🕒 Session",
    "btn.journal": u"📒 Journal",
    "btn.paper_on": u"▶️ On",
    "btn.paper_off": u"⏸ Off",
    "btn.paper_reset": u"↺ Reset 10,000",
    "btn.hot": u"🔥 Hottest",
    "btn.find_coin": u"🔎 Send a coin name",
    "btn.crypto_radar": u"🛰️ Core radar",
    "btn.crypto_brief": u"🌍 Coin brief",
    "btn.crypto_core": u"📡 Core signals",
    "btn.crypto_ch": u"📣 TZ Crypto channel",
    "btn.lvl1": u"🟢 Level 1 — Beginner",
    "btn.lvl2": u"🔵 Level 2 — ICT foundation",
    "btn.lvl3": u"🟣 Level 3 — Advanced ICT",
    "btn.lvl4": u"🟡 Level 4 — Execution & mind",
    "btn.lvl5": u"🔗 Level 5 — API & connect",
    "btn.ask_all": u"💬 Ask the mentor (full course)",
    "btn.ask_level": u"💬 Ask about this level",
    "btn.ask_lesson": u"💬 Ask about this lesson",
    "btn.hear_lesson": u"🔊 Hear this lesson",
    "btn.catalog": u"📚 Catalog",
    "btn.prev": u"⬅️ Prev",
    "btn.next": u"Next ➡️",
    "btn.same_level": u"📚 This level",
    "btn.go_connect": u"🔗 Open connect",
    "btn.refresh": u"🔄 Refresh",
    "btn.open_pos": u"📡 Open trades",
    "txt.start": u"%s Tehran\nForex: EUR · GBP · Gold\nCrypto beta: any USDT spot — send the name\n\nNo fabricated signals. Stop loss is mandatory.\nFree channel @TZ_FX_CH",
    "txt.help": u"/signal signals\n/crypto coins\n/connect venues\n/paper paper trading\n/learn lessons\n/wr win-rate\n/lang language\n\nSend a voice note — the mentor replies.",
    "txt.join": u"Join the free channel first, then tap “I joined”.\nFull signals require a subscription.",
    "txt.paywall_active": u"Active until %s · about %s days left",
    "txt.paywall_none": u"No active subscription",
    "txt.paywall_body": u"Full signals, charts, mentor and VIP need a subscription.\nPick a plan → card transfer → send the receipt photo here.\nVIP link after approval.",
    "txt.me_on": u"Active until %s · %s days\nVIP: %s\nClear mentor memory: /forget",
    "txt.me_off": u"Not active. Subscribe for full signals.",
    "txt.crypto": u"%s USDT spot coins.\nSend a name or pick hottest.\nSame ICT geometry — beta, no profit promise.\nChannel: %s",
    "txt.desk": u"Radar · session · journal · paper · connect",
    "txt.connect": u"Demo mode. No live orders are sent.\nExchange: <b>%s</b> · keys %s\nMT5: %s\n1%% risk · stop loss required",
    "txt.connect_ready": u"Connect is ready. Pick an exchange, then send keys.",
    "txt.edu_intro": u"ICT 2022 from zero to execution.\nOpen a lesson. API and connectivity are level 5.",
    "txt.gate_join": u"Join the channel first",
    "txt.gate_pay": u"Subscription required",
    "txt.coach_hello": u"🎙️ Hi %s — your TZ FX mentor.\nFavorite symbol: <b>%s</b>%s\n\nType or send a voice note — reply is text + voice.",
    "txt.coach_hello_speak": u"Hi %s. I am your mentor. Type or send a voice note.",
    "txt.coach_mem": u"\nI remember your earlier notes — they stay isolated to you.",
    "txt.coach_busy": u"Mentor is busy. Try again in a moment.",
    "txt.coach_empty": u"Empty message",
    "txt.coach_wait": u"Wait a second",
    "txt.coach_quota": u"Hourly chat quota is full",
    "txt.forget": u"🧹 Your mentor memory was cleared.\nI start from zero with you — other students are untouched.",
    "txt.watch_on": u"👀 Watcher on. I will DM complete ICT 2022 setups.",
    "txt.watch_off": u"👀 Watcher off.",
    "txt.lang_set_fa": u"زبان: فارسی",
    "txt.lang_set_en": u"Language: English",
    "txt.wait": u"WAIT",
    "txt.buy": u"BUY",
    "txt.sell": u"SELL",
    "txt.no_signal": u"ICT 2022 model is incomplete — do not chase.",
    "txt.paper_demo": u"Practice only · not real money · 1% risk · stop loss required",
    "txt.paper_on": u"On",
    "txt.paper_off": u"Off",
    "txt.wr_line": u"From real take-profit and stop-loss hits. No invented percentage.",
    "txt.wr_empty": u"No closed signals in the current engine book yet.",
    "txt.all_coins": u"all",
    "txt.fx_closed": u"Forex is closed",
    "txt.fx_open": u"Forex is open",
    "cmd.start": u"Home",
    "cmd.signal": u"Signals",
    "cmd.crypto": u"Crypto",
    "cmd.connect": u"Connect exchange/broker",
    "cmd.paper": u"Paper trading",
    "cmd.learn": u"Lessons",
    "cmd.wr": u"Win-rate",
    "cmd.help": u"Help",
    "cmd.lang": u"Language / زبان",
    "cmd.desk": u"Desk",
    "cmd.support": u"Support",
    "ai.sys": (
        "You are the TZ FX mentor. Warm, direct, short — like a voice note. "
        "You sit with this one student. Do not sound like a bot. "
        "Two desks: 1) Forex ICT Mentorship 2022 — EURUSD, GBPUSD, XAUUSD only. "
        "Saturday and Sunday forex is closed; say so honestly. Channel FX window 08:30–20:30 Tehran. "
        "2) Crypto beta — any USDT spot coin. Same geometry: Judas sweep → MSS → FVG → enter inside the gap, SL beyond the wick. "
        "Crypto is 24/7 and beta; do not claim Michael's ICT on coins. "
        "Never invent signals or prices. Use market data only if it is in the prompt. "
        "No entry without stop loss. Score under 4 or against daily bias = wait. "
        "No profit promises, no fake accuracy. Memory is this student only. "
        "Short sentences, speakable, no tables or asterisks."
    ),
}

EDU_TITLE_EN = {
    "edu_1": u"What is trading?",
    "edu_2": u"Pips, lots, spread, margin",
    "edu_3": u"MetaTrader from zero",
    "edu_4": u"Entry, stop loss, take profit",
    "edu_5": u"1% risk management",
    "edu_6": u"ICT Mentorship 2022",
    "edu_7": u"Liquidity BSL and SSL",
    "edu_8": u"Sweep and Judas Swing",
    "edu_9": u"Displacement",
    "edu_10": u"FVG — Fair Value Gap",
    "edu_11": u"Premium and discount",
    "edu_12": u"A complete ICT setup",
    "edu_13": u"OTE — golden zone",
    "edu_14": u"Order block and breaker",
    "edu_15": u"London and New York kill zones",
    "edu_16": u"Silver Bullet",
    "edu_17": u"HTF bias D1/H4/H1",
    "edu_18": u"Gold in ICT",
    "edu_19": u"When not to trade",
    "edu_20": u"Trading psychology",
    "edu_21": u"Managing a live position",
    "edu_22": u"Trade journal",
    "edu_23": u"Using TZ FX BOT",
    "edu_24": u"Pre-click checklist",
    "edu_25": u"Exchange API keys",
    "edu_26": u"Broker and bot connection",
}

EDU_EN = {
    "edu_1": (
        u"<b>Lesson 1 — What is trading?</b>\n"
        u"Level 1 · Beginner\n"
        u"────────────\n"
        u"Trading is buying or selling a symbol based on a directional view.\n"
        u"Forex desk: EUR, GBP, gold. Crypto beta is separate.\n\n"
        u"• <b>BUY</b> = expect higher prices.\n"
        u"• <b>SELL</b> = expect lower prices.\n\n"
        u"Every trade needs three numbers: entry, stop loss, take profit.\n"
        u"Without those three it is gambling, not trading.\n\n"
        u"We do not promise profit. We do not invent accuracy percentages."
    ),
    "edu_2": (
        u"<b>Lesson 2 — Pips, lots, spread, margin</b>\n"
        u"A pip is the unit of price movement. EUR/GBP: 0.0001. Gold here: about 0.1.\n"
        u"Lot is size. Start tiny (0.01) on small accounts.\n"
        u"Spread is the broker’s cost of entry.\n"
        u"Leverage does not enlarge skill — it kills mistakes faster.\n"
        u"Margin is collateral. Hit it and the broker force-closes you."
    ),
    "edu_3": (
        u"<b>Lesson 3 — MetaTrader from zero</b>\n"
        u"Open a demo account first. Find the symbol, set H1 or M15.\n"
        u"New order: volume, stop loss, take profit. No SL, no click.\n"
        u"The bot signals. Broker execution on Windows is the MT5 bridge. The bot server does not run MT5."
    ),
    "edu_4": (
        u"<b>Lesson 4 — Entry, SL, TP</b>\n"
        u"Entry is where the 2022 model completed — not wherever you feel like it.\n"
        u"Stop loss sits beyond the sweep wick.\n"
        u"Take profit is opposing internal liquidity.\n"
        u"No stop loss = no trade. Do not chase after the move."
    ),
    "edu_5": (
        u"<b>Lesson 5 — 1% risk</b>\n"
        u"Risk at most 1% of equity per trade.\n"
        u"Size from the distance between entry and stop loss, not from emotion.\n"
        u"Paper is practice. It is not real money."
    ),
    "edu_6": (
        u"<b>Lesson 6 — ICT Mentorship 2022</b>\n"
        u"One model only. Sequence: HTF draw → Judas sweep → MSS with displacement → "
        u"enter inside FVG/OTE → SL beyond the wick → TP internal liquidity.\n"
        u"If one link is missing, wait."
    ),
    "edu_7": (
        u"<b>Lesson 7 — BSL and SSL</b>\n"
        u"Buy-side liquidity sits above highs. Sell-side below lows.\n"
        u"The market hunts those stops, then often reverses.\n"
        u"Do not chase the hunt. Wait for the sweep, then join the real draw."
    ),
    "edu_8": (
        u"<b>Lesson 8 — Judas Swing</b>\n"
        u"A fake push beyond a session high/low to harvest stops.\n"
        u"After the sweep you still need MSS with a strong body. A wick alone is not a setup."
    ),
    "edu_9": (
        u"<b>Lesson 9 — Displacement</b>\n"
        u"Strong-bodied candles after the sweep. Without displacement, MSS is weak.\n"
        u"The bot does not fire a live signal without it."
    ),
    "edu_10": (
        u"<b>Lesson 10 — Fair Value Gap</b>\n"
        u"A three-candle imbalance. Enter only inside the gap.\n"
        u"If price runs through the gap, do not chase. Wait for the next model."
    ),
    "edu_11": (
        u"<b>Lesson 11 — Premium and discount</b>\n"
        u"Split the range. Above midpoint = premium. Below = discount.\n"
        u"Buy in discount with bullish HTF. Sell in premium with bearish HTF.\n"
        u"Buying premium is chasing."
    ),
    "edu_12": (
        u"<b>Lesson 12 — Complete ICT 2022 setup</b>\n"
        u"HTF bias, Judas sweep, MSS, FVG, entry inside the gap, SL beyond the wick, TP IRL.\n"
        u"Score under 4 = do not click. We do not invent signals."
    ),
    "edu_13": (
        u"<b>Lesson 13 — OTE</b>\n"
        u"Optimal Trade Entry is the 62–79% retrace of the displacement leg.\n"
        u"Stronger when it overlaps the FVG. Not required if the rest of the model is complete."
    ),
    "edu_14": (
        u"<b>Lesson 14 — Order block and breaker</b>\n"
        u"Order block: last opposing candle before displacement.\n"
        u"Breaker: a broken block that changes role.\n"
        u"Primary entry remains the FVG. Blocks are confirmation, not a reason to fade HTF."
    ),
    "edu_15": (
        u"<b>Lesson 15 — Kill zones</b>\n"
        u"London and New York are where liquidity is typically taken.\n"
        u"Outside those windows, wait. Clock is Tehran time.\n"
        u"Silver Bullet is a short window inside New York — not magic."
    ),
    "edu_16": (
        u"<b>Lesson 16 — Silver Bullet</b>\n"
        u"The same 2022 model inside a specific time window.\n"
        u"No sweep, no gap → the name changes nothing. Do not chase."
    ),
    "edu_17": (
        u"<b>Lesson 17 — HTF bias</b>\n"
        u"Daily, then H4, then H1.\n"
        u"Bullish daily → look for discount buys on M15. Against daily = wait."
    ),
    "edu_18": (
        u"<b>Lesson 18 — Gold</b>\n"
        u"Same 2022 model, wider swings. Do not set a stop so wide it eats 1%.\n"
        u"Gold spread is larger than EUR. Size down into heavy news, or stand aside."
    ),
    "edu_19": (
        u"<b>Lesson 19 — When not to trade</b>\n"
        u"Skip if: outside kill zone, against HTF, no sweep, no FVG, wide spread, news in one minute, or your gut is loud.\n"
        u"Not trading is a position."
    ),
    "edu_20": (
        u"<b>Lesson 20 — Psychology</b>\n"
        u"Do not revenge after a loss. Do not double size.\n"
        u"Two losses in a row: walk. The mentor is a checklist, not a gambling buddy."
    ),
    "edu_21": (
        u"<b>Lesson 21 — Managing the trade</b>\n"
        u"Do not drag the stop so the loser can live.\n"
        u"Move to breakeven only after first target if you must.\n"
        u"Do not turn a winner into a loser."
    ),
    "edu_22": (
        u"<b>Lesson 22 — Journal</b>\n"
        u"Write symbol, side, entry, SL, TP, why, result.\n"
        u"Without a journal you repeat the same error. Do not write fake percentages."
    ),
    "edu_23": (
        u"<b>Lesson 23 — TZ FX BOT</b>\n"
        u"ICT signals, charts, mentor, 26 lessons.\n"
        u"FX channel window 08:30–20:30 Tehran. In-bot DM is 24/7.\n"
        u"Saturday forex is closed. Crypto is beta and separate."
    ),
    "edu_24": (
        u"<b>Lesson 24 — Pre-click checklist</b>\n"
        u"HTF? Swept? MSS? Inside the gap? SL placed? 1%?\n"
        u"If two answers are no, do not click. Send it to the mentor."
    ),
    "edu_25": (
        u"<b>Lesson 25 — Exchange API keys</b>\n"
        u"Keys are yours. Send them in the bot; the message is deleted and never logged.\n"
        u"Demo first. Until you type LIVE, no real order is sent.\n"
        u"Bitget and BingX are on the connect screen. Never share keys."
    ),
    "edu_26": (
        u"<b>Lesson 26 — Broker connection</b>\n"
        u"MT5 runs on Windows, not on the bot server.\n"
        u"Download the bridge from Connect. Run it on the PC where MT5 is logged in.\n"
        u"Stop loss required. Paper is practice. Nothing is live until you type LIVE."
    ),
}

EDU_SPEAK_EN = {
    "edu_1": u"Lesson one. Trading is a directional bet with three mandatory numbers: entry, stop loss, take profit. Without those it is gambling. We do not promise profit.",
    "edu_2": u"Lesson two. Pips measure movement. Lots are size. Start at point zero one on small accounts. Leverage kills mistakes faster than it grows skill.",
    "edu_3": u"Lesson three. Open MetaTrader on demo. Every order needs volume, stop loss and take profit. The bot does not run MT5. The Windows bridge does.",
    "edu_4": u"Lesson four. Enter where the 2022 model completed. Stop beyond the sweep wick. Target opposing liquidity. Do not chase.",
    "edu_5": u"Lesson five. Risk one percent. Size from stop distance, not from feeling. Paper is not real money.",
    "edu_6": u"Lesson six. ICT Mentorship 2022 only. HTF, Judas sweep, MSS with displacement, enter inside the gap, stop beyond the wick.",
    "edu_7": u"Lesson seven. BSL above highs, SSL below lows. Let the hunt happen, then join the real draw.",
    "edu_8": u"Lesson eight. Judas is a fake push that harvests stops. You still need a strong-bodied market structure shift.",
    "edu_9": u"Lesson nine. Displacement is the strong body after the sweep. Without it the bot will not fire.",
    "edu_10": u"Lesson ten. Fair value gap is the imbalance. Enter only inside it. If price runs through, wait.",
    "edu_11": u"Lesson eleven. Discount is cheap, premium is expensive. Buy discount with bullish daily. Do not buy premium.",
    "edu_12": u"Lesson twelve. If any link is missing, it is not a setup. Score under four means do not click.",
    "edu_13": u"Lesson thirteen. OTE is the sixty-two to seventy-nine percent retrace. Stronger with the gap.",
    "edu_14": u"Lesson fourteen. Order block is confirmation. The gap remains the entry.",
    "edu_15": u"Lesson fifteen. London and New York kill zones, Tehran clock. Outside them, wait.",
    "edu_16": u"Lesson sixteen. Silver Bullet is a window, not magic. No sweep, no gap, no trade.",
    "edu_17": u"Lesson seventeen. Daily, then four-hour, then one-hour. Against daily, wait.",
    "edu_18": u"Lesson eighteen. Gold uses the same model. Do not let the stop eat your one percent.",
    "edu_19": u"Lesson nineteen. Skip wide spreads, news, missing sweeps, and a loud gut. Standing aside is a trade.",
    "edu_20": u"Lesson twenty. No revenge. No doubled size after a loss.",
    "edu_21": u"Lesson twenty-one. Do not drag the stop to keep a loser alive.",
    "edu_22": u"Lesson twenty-two. Journal every trade. Do not write fake percentages.",
    "edu_23": u"Lesson twenty-three. Channel forex window eight-thirty to twenty-thirty Tehran. Crypto is beta.",
    "edu_24": u"Lesson twenty-four. Checklist: HTF, sweep, MSS, gap, stop, one percent. Two nos, no click.",
    "edu_25": u"Lesson twenty-five. API keys are deleted after you send them. Demo until you type LIVE.",
    "edu_26": u"Lesson twenty-six. Run the MT5 bridge on Windows beside the terminal. Stop loss is mandatory.",
}

CATALOG = {"fa": FA, "en": EN}


def norm_lang(code):
    c = (code or "").lower()
    if c.startswith("en"):
        return "en"
    return "fa"


def t(lang, key, **kwargs):
    lang = norm_lang(lang)
    bag = CATALOG.get(lang) or FA
    s = bag.get(key)
    if s is None:
        s = FA.get(key) or key
    if kwargs:
        try:
            return s % kwargs
        except Exception:
            try:
                return s % tuple(kwargs.values())
            except Exception:
                return s
    return s


def edu_title(lang, key, fallback=""):
    if norm_lang(lang) == "en":
        return EDU_TITLE_EN.get(key) or fallback
    return fallback


def edu_html(lang, key, fallback=""):
    if norm_lang(lang) == "en":
        return EDU_EN.get(key) or fallback
    return fallback


def edu_speak(lang, key, fallback=""):
    if norm_lang(lang) == "en":
        return EDU_SPEAK_EN.get(key) or fallback
    return fallback


def ai_sys(lang):
    return t(lang, "ai.sys")
