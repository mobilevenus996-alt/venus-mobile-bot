#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Venus Mobile Bot - ربات تلگرامی راهنمای شبکه‌های اجتماعی
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# تنظیم لاگ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========== توکن ربات ==========
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # توکن خود را اینجا بگذارید


# ========== متن‌های راهنما ==========

INSTAGRAM_CONTENT = """
📸 *راهنمای ساخت محتوا برای اینستاگرام*

━━━━━━━━━━━━━━━━━━

🔹 *انواع محتوا:*
• پست تصویری (Feed Post)
• ریلز (Reels) - ویدیوی ۱۵ ثانیه تا ۹۰ ثانیه
• استوری (Story) - ۲۴ ساعته
• IGTV - ویدیوهای بلند
• Live - پخش زنده

🔹 *نکات مهم برای پست:*
• تصویر با کیفیت بالا (حداقل ۱۰۸۰x۱۰۸۰)
• کپشن جذاب با هشتگ مناسب (۵ تا ۱۵ هشتگ)
• در ساعات اوج فعالیت پست بده (۹-۱۱ صبح / ۷-۹ شب)
• از CTA (دعوت به اقدام) استفاده کن

🔹 *برای ریلز:*
• موزیک ترند استفاده کن
• ۳ ثانیه اول باید جذاب باشه
• زیرنویس اضافه کن
• عمودی بفرست (۹:۱۶)

🔹 *ابزارهای مفید:*
• Canva - طراحی گرافیک
• CapCut - ویرایش ویدیو
• Later / Buffer - زمان‌بندی پست

✅ *نکته طلایی:* Consistency مهم‌ترین فاکتوره. حداقل ۳ بار در هفته پست بده!
"""

WHATSAPP_CONTENT = """
💬 *راهنمای ساخت محتوا برای واتساپ*

━━━━━━━━━━━━━━━━━━

🔹 *واتساپ بیزینس (WhatsApp Business):*
• حساب تجاری رایگان بساز
• پروفایل کامل با آدرس و ساعت کاری
• پیام خوش‌آمدگویی خودکار تنظیم کن
• پیام غیاب تنظیم کن

🔹 *انواع محتوا در واتساپ:*
• پیام متنی + ایموجی
• تصویر و ویدیو
• وویس نوت (صوتی)
• کاتالوگ محصولات
• استوری واتساپ (Status)

🔹 *گروه‌ها و کانال‌ها:*
• گروه: حداکثر ۱۰۲۴ عضو (تعاملی)
• کانال: بدون محدودیت عضو (یک‌طرفه)
• برای بیزینس از کانال استفاده کن

🔹 *نکات مهم:*
• پیام‌های کوتاه و واضح بفرست
• از Bold (*متن*) و Italic (_متن_) استفاده کن
• لینک‌ها را کوتاه کن (bit.ly)
• Broadcast List برای پیام انبوه استفاده کن

🔹 *WhatsApp API:*
• برای کسب‌وکارهای بزرگ
• امکان ارسال پیام خودکار
• نیاز به تایید Meta داره

✅ *نکته:* واتساپ بیزینس رایگانه! همین الان دانلود کن.
"""

APPSTORE_CONTENT = """
🍎 *راهنمای ورود به App Store (اپل)*

━━━━━━━━━━━━━━━━━━

🔹 *مرحله ۱: ساخت Apple ID*
۱. به appleid.apple.com برو
۲. روی "Create Your Apple ID" کلیک کن
۳. اطلاعات رو پر کن (نام، ایمیل، رمز)
۴. ایمیل رو تایید کن
۵. شماره موبایل برای تایید دو مرحله‌ای

🔹 *مرحله ۲: ورود به App Store*
۱. گوشی آیفون یا آیپد باز کن
۲. App Store رو باز کن
۳. پایین صفحه روی آیکون خودت کلیک کن
۴. "Sign In" رو بزن
۵. Apple ID و رمز رو وارد کن

🔹 *مشکل رایج - منطقه جغرافیایی:*
• بعضی اپ‌ها فقط در کشورهای خاص هستن
• برای تغییر Region:
  → Settings > [نامت] > Media & Purchases
  → View Account > Country/Region
  → Change Country or Region

🔹 *ساخت Apple ID بدون کارت:*
۱. App Store رو باز کن
۲. یه اپ رایگان انتخاب کن
۳. Get > Create New Apple ID
۴. در قسمت پرداخت "None" انتخاب کن ✅

🔹 *خرید از App Store:*
• اپل گیفت کارت
• کارت بین‌المللی
• خرید از اکانت‌های معتبر

⚠️ *مهم:* Apple ID رو با کسی شیر نکن!
"""

GENERAL_GUIDE = """
📱 *راهنمای کلی شبکه‌های اجتماعی*

━━━━━━━━━━━━━━━━━━

🔹 *مقایسه پلتفرم‌ها:*

| پلتفرم | بهترین محتوا | مخاطب |
|--------|-------------|--------|
| اینستاگرام | تصویر + ریلز | ۱۸-۳۵ سال |
| واتساپ | پیام + گروه | همه سنین |
| تلگرام | کانال + فایل | ۲۰-۴۰ سال |
| یوتیوب | ویدیوی بلند | همه سنین |
| لینکدین | محتوای حرفه‌ای | کسب‌وکار |

🔹 *اصول طلایی محتوا:*
✅ ارزش بده (آموزش، سرگرمی، انگیزه)
✅ منظم پست بده
✅ با مخاطب تعامل داشته باش
✅ از تصاویر باکیفیت استفاده کن
✅ استوری‌تلینگ کن

🔹 *ابزارهای ضروری:*
🎨 Canva - طراحی رایگان
✂️ CapCut - ویرایش ویدیو
📊 Meta Business Suite - آنالیز
📅 Buffer / Later - زمان‌بندی
🔗 Linktree - لینک در بیو

🔹 *اشتباهات رایج:*
❌ کپی محتوا از دیگران
❌ خرید فالوور
❌ پست نامنظم
❌ نادیده گرفتن کامنت‌ها
❌ هشتگ بی‌ربط

💡 *نکته مهم:* اول یه پلتفرم رو خوب یاد بگیر، بعد گسترش بده!
"""


# ========== کیبورد اصلی ==========

def main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📸 اینستاگرام", callback_data="instagram"),
            InlineKeyboardButton("💬 واتساپ", callback_data="whatsapp"),
        ],
        [
            InlineKeyboardButton("🍎 App Store", callback_data="appstore"),
            InlineKeyboardButton("📱 راهنمای کلی", callback_data="general"),
        ],
        [
            InlineKeyboardButton("❓ سوال دارم", callback_data="question"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def back_keyboard():
    keyboard = [[InlineKeyboardButton("🔙 بازگشت به منو", callback_data="back")]]
    return InlineKeyboardMarkup(keyboard)


# ========== هندلرها ==========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع ربات"""
    user = update.effective_user
    welcome_text = f"""
سلام {user.first_name} عزیز! 👋

به *Venus Mobile Bot* خوش اومدی 🌟

این ربات بهت کمک می‌کنه تو:
📸 اینستاگرام محتوای جذاب بسازی
💬 واتساپ بیزینس راه بندازی  
🍎 به App Store وارد بشی
📱 شبکه‌های اجتماعی رو حرفه‌ای مدیریت کنی

یه گزینه انتخاب کن 👇
"""
    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور کمک"""
    help_text = """
🆘 *راهنمای استفاده از ربات*

دستورات:
/start - شروع مجدد
/help - این پیام
/instagram - راهنمای اینستاگرام
/whatsapp - راهنمای واتساپ
/appstore - راهنمای App Store

یا از منوی زیر استفاده کن 👇
"""
    await update.message.reply_text(
        help_text,
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """هندلر دکمه‌ها"""
    query = update.callback_query
    await query.answer()

    if query.data == "instagram":
        await query.edit_message_text(
            INSTAGRAM_CONTENT,
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )

    elif query.data == "whatsapp":
        await query.edit_message_text(
            WHATSAPP_CONTENT,
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )

    elif query.data == "appstore":
        await query.edit_message_text(
            APPSTORE_CONTENT,
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )

    elif query.data == "general":
        await query.edit_message_text(
            GENERAL_GUIDE,
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )

    elif query.data == "question":
        await query.edit_message_text(
            "❓ *سوالت رو بنویس*\n\nسوالت رو مستقیم برام بفرست، جواب می‌دم! 👇",
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )
        context.user_data["waiting_question"] = True

    elif query.data == "back":
        welcome_text = """
🏠 *منوی اصلی*

یه گزینه انتخاب کن 👇
"""
        await query.edit_message_text(
            welcome_text,
            parse_mode="Markdown",
            reply_markup=main_keyboard()
        )
        context.user_data["waiting_question"] = False


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """هندلر پیام‌های متنی"""
    text = update.message.text.lower()

    # اگر کاربر سوال داره
    if context.user_data.get("waiting_question"):
        response = f"""
✅ سوالت دریافت شد!

📌 *سوال:* {update.message.text}

🤖 در حال حاضر ربات در حالت راهنما هست.
برای سوالات تخصصی‌تر با ادمین در تماس باش.

از منوی زیر می‌تونی راهنماها رو ببینی 👇
"""
        context.user_data["waiting_question"] = False
        await update.message.reply_text(
            response,
            parse_mode="Markdown",
            reply_markup=main_keyboard()
        )
        return

    # تشخیص کلیدواژه
    if "اینستاگرام" in text or "instagram" in text:
        await update.message.reply_text(
            INSTAGRAM_CONTENT,
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )
    elif "واتساپ" in text or "whatsapp" in text:
        await update.message.reply_text(
            WHATSAPP_CONTENT,
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )
    elif "اپ استور" in text or "app store" in text or "اپل" in text:
        await update.message.reply_text(
            APPSTORE_CONTENT,
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )
    else:
        await update.message.reply_text(
            "از منوی زیر گزینه مورد نظرت رو انتخاب کن 👇",
            reply_markup=main_keyboard()
        )


# ========== دستورات مستقیم ==========

async def instagram_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(INSTAGRAM_CONTENT, parse_mode="Markdown", reply_markup=back_keyboard())

async def whatsapp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WHATSAPP_CONTENT, parse_mode="Markdown", reply_markup=back_keyboard())

async def appstore_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(APPSTORE_CONTENT, parse_mode="Markdown", reply_markup=back_keyboard())


# ========== اجرای ربات ==========

def main():
    """اجرای اصلی"""
    print("🤖 Venus Mobile Bot در حال اجراست...")

    app = Application.builder().token(BOT_TOKEN).build()

    # هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("instagram", instagram_command))
    app.add_handler(CommandHandler("whatsapp", whatsapp_command))
    app.add_handler(CommandHandler("appstore", appstore_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("✅ ربات آماده‌ست! Ctrl+C برای خروج")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
