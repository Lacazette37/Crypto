import requests
from telegram import Update # type: ignore
from telegram.ext import Application, CommandHandler, ContextTypes

# CoinGecko API'den kripto para fiyatını almak için fonksiyon
def get_crypto_price(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=try"
    response = requests.get(url)
    data = response.json()
    return data[crypto_id]['try']

# /start komutunu işleyen fonksiyon
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Merhaba! Kripto para birimlerinin anlık fiyatlarını öğrenmek için /fiyat <kripto_adi> komutunu kullanın. Örneğin: /price bitcoin')

# /price komutunu işleyen fonksiyon
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        crypto_id = context.args[0].lower()  # Kullanıcının girdiği kripto adını al
        price = get_crypto_price(crypto_id)  # Fiyatı CoinGecko API'den al
        await update.message.reply_text(f'{crypto_id.upper()} fiyatı: ${price}')
    except IndexError:
        await update.message.reply_text('Lütfen bir kripto para birimi adı girin. Örneğin: /fiyat bitcoin')
    except KeyError:
        await update.message.reply_text('Geçersiz kripto para birimi adı.')

# Ana fonksiyon
def main():
    # Telegram bot token'ınızı buraya girin
    token = '7542415403:AAFv1MGS5Z0yZpaT7GzL_NGWnIaCUFryrxs'
    
    # Application oluştur
    application = Application.builder().token(token).build()
    
    # Komut işleyicilerini ekleyin
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("fiyat", price))
    
    # Botu başlatın
    application.run_polling()

if __name__ == '__main__':
    main()