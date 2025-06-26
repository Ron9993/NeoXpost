
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot token and channel configuration
BOT_TOKEN = '8037037101:AAGUgIZSRRyGagqKlqt2VMlv8TSdiRBZtzI'
CHANNEL_ID = '@neoxchange88'  # Your channel ID
NEOXBOT_USERNAME = '@NeoXchange_bot'  # Your NeoXchange bot username
CRYPTO_SHOP_CHANNEL = '@cryptoaccess88'  # Your crypto accessories channel

# Multilingual content
MESSAGES = {
    'english': {
        'title': '🚀 Welcome to NeoXchange – Myanmar\'s Trusted Crypto ↔ MMK Converter',
        'intro': 'Looking to buy USDT or TRX in Myanmar with ease, speed, and full transparency?\nNeoXchange is your secure local crypto hub, offering real-time rates, fast admin verification, and full multilingual support.',
        'features': '''💸 What NeoXchange Offers You:
✅ Buy USDT or TRX directly with MMK (Kyat)
✅ Competitive daily exchange rates
✅ Secure proof upload and fast admin approval
✅ Receive your crypto within minutes after verification
✅ Full order tracking — know exactly what stage your order is at
✅ Available in English 🇬🇧, Burmese 🇲🇲, and Chinese 🇨🇳''',
        'tracking': '''📦 All orders are tracked by unique Order IDs, and status updates are shown clearly:
➖ Pending → Approved → Processing → Sent''',
        'support': '💬 Need help? Talk directly to support — no bots, no delays.',
        'footer': '📲 Start buying now via Telegram:\n📌 Built by locals — for locals.'
    },
    'burmese': {
        'title': '🌐 NeoXchange – မြန်မာနိုင်ငံအတွက် ယုံကြည်စိတ်ချရတဲ့ Crypto ဝယ်ယူမှုစနစ်',
        'intro': '🪙 USDT / TRX ကို MMK နဲ့ တိုက်ရိုက် ဝယ်လို့ရပါပြီ။\n🔒 ရှင်းလင်းမှု၊ စိတ်ချမှုနဲ့ မြန်ဆန်မှုကို အခြေခံထားတဲ့ ဝန်ဆောင်မှုဖြစ်ပါတယ်။',
        'features': '''💸 NeoXchange မှ ပေးအပ်သော ဝန်ဆောင်မှုများ:
✅ MMK (ကျပ်) နဲ့ USDT သို့မဟုတ် TRX တိုက်ရိုက်ဝယ်ယူပါ
✅ ယှဉ်ပြိုင်နိုင်သော နေ့စဉ်လဲလှယ်နှုန်းများ
✅ လုံခြုံသော သက်သေအထောက်အထားတင်ခြင်းနှင့် မြန်ဆန်သော အက်ဒမင်အတည်ပြုခြင်း
✅ အတည်ပြုပြီးနောက် မိနစ်အနည်းငယ်အတွင်း သင့်crypto ရယူပါ
✅ အပြည့်အစုံ အမိန့်ခြေရာခံခြင်း — သင့်အမိန့်သည် မည်သည့်အဆင့်တွင်ရှိသည်ကို အတိအကျသိရှိပါ
✅ အင်္ဂလိပ် 🇬🇧၊ မြန်မာ 🇲🇲၊ နှင့် တရုတ် 🇨🇳 တို့တွင် ရရှိနိုင်ပါသည်''',
        'tracking': '''📦 အမိန့်များအားလုံးကို ထူးခြားသော Order ID များဖြင့် ခြေရာခံထားပြီး အခြေအနေအပ်ဒိတ်များကို ရှင်းလင်းစွာပြသထားသည်:
➖ ဆိုင်းငံ့ → အတည်ပြု → လုပ်ဆောင်နေ → ပေးပို့ပြီး''',
        'support': '💬 အကူအညီလိုအပ်လား? ထောက်ပံ့မှုနှင့် တိုက်ရိုက်စကားပြော — ဘော့များမရှိ၊ နှောင့်နှေးမှုမရှိ။',
        'footer': '📲 Telegram မှတစ်ဆင့် ယခုပင်ဝယ်ယူခြင်းကို စတင်ပါ:\n📌 ဒေသခံများမှ တည်ဆောက် — ဒေသခံများအတွက်။'
    },
    'chinese': {
        'title': '🌐 NeoXchange – 缅甸用户首选的加密货币购买平台',
        'intro': '💵 通过缅币（MMK）快速购买 USDT 或 TRX\n🔒 透明、安全、快速的本地化服务。',
        'features': '''💸 NeoXchange 为您提供:
✅ 通过缅币（MMK）直接购买 USDT 或 TRX
✅ 具有竞争力的每日汇率
✅ 安全的凭证上传和快速管理员审批
✅ 验证后几分钟内收到您的加密货币
✅ 完整的订单跟踪 — 准确了解您的订单处于哪个阶段
✅ 支持英语 🇬🇧、缅甸语 🇲🇲 和中文 🇨🇳''',
        'tracking': '''📦 所有订单都通过唯一的订单ID进行跟踪，状态更新清晰显示:
➖ 待处理 → 已批准 → 处理中 → 已发送''',
        'support': '💬 需要帮助？直接与支持人员交谈 — 无机器人，无延迟。',
        'footer': '📲 现在通过Telegram开始购买:\n📌 由本地人建造 — 为本地人服务。'
    }
}

def get_inline_keyboard(current_lang='english'):
    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_english"),
            InlineKeyboardButton("🇲🇲 မြန်မာ", callback_data="lang_burmese"),
            InlineKeyboardButton("🇨🇳 中文", callback_data="lang_chinese")
        ],
        [
            InlineKeyboardButton("💰 Buy Crypto", url=f"https://t.me/{NEOXBOT_USERNAME}"),
            InlineKeyboardButton("🛒 Crypto Shop", url=f"https://t.me/{CRYPTO_SHOP_CHANNEL.replace('@', '')}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def format_message(lang='english'):
    msg = MESSAGES[lang]
    separator = "━━━━━━━━━━━━━━━━━━━"
    
    message = f"{msg['title']}\n\n"
    message += f"{msg['intro']}\n\n"
    message += f"{msg['features']}\n\n"
    message += f"{msg['tracking']}\n\n"
    message += f"{msg['support']}\n\n"
    message += f"{separator}\n"
    message += f"{msg['footer']}\n"
    message += f"➡️ @{NEOXBOT_USERNAME}"
    
    return message

async def start(update, context):
    """Handle the /start command"""
    message = format_message('english')
    keyboard = get_inline_keyboard('english')
    
    await update.message.reply_text(
        message,
        reply_markup=keyboard,
        parse_mode='HTML'
    )

async def post_to_channel(update, context):
    """Handle the /post command to send message to channel"""
    if not CHANNEL_ID:
        await update.message.reply_text("Channel ID not configured. Please set TELEGRAM_CHANNEL_ID in Secrets.")
        return
    
    message = format_message('english')
    keyboard = get_inline_keyboard('english')
    
    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        await update.message.reply_text("✅ Message posted to channel successfully!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error posting to channel: {str(e)}")

async def button_handler(update, context):
    """Handle inline button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('lang_'):
        lang = query.data.replace('lang_', '')
        message = format_message(lang)
        keyboard = get_inline_keyboard(lang)
        
        await query.edit_message_text(
            text=message,
            reply_markup=keyboard,
            parse_mode='HTML'
        )

async def help_command(update, context):
    """Show help information"""
    help_text = """
🤖 NeoXchange Bot Commands:

/start - Show the main NeoXchange message with language options
/post - Post the message to your configured channel
/help - Show this help message

📝 Setup Instructions:
1. Set TELEGRAM_BOT_TOKEN in Secrets
2. Set TELEGRAM_CHANNEL_ID in Secrets (e.g., @yourchannel)
3. Set CRYPTO_SHOP_CHANNEL in Secrets (optional, defaults to @cryptoshop)

🔧 Configuration:
- Edit NEOXBOT_USERNAME variable in the code to match your NeoXchange bot
- Customize messages in the MESSAGES dictionary
- Modify inline buttons in get_inline_keyboard function
    """
    await update.message.reply_text(help_text)

def main():
    """Start the bot"""
    if not BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not found in environment variables.")
        print("Please add your bot token to Secrets in Replit.")
        return
    
    print("🚀 Starting NeoXchange Telegram Bot...")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("post", post_to_channel))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Start the bot
    print("✅ Bot is running! Use /start to test the message.")
    print("✅ Use /post to send the message to your channel.")
    application.run_polling()

if __name__ == '__main__':
    main()
