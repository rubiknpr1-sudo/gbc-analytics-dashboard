"""
Telegram-уведомления о крупных заказах (> 50 000 ₸)
Данные из Supabase → Telegram Bot API
"""

import urllib.request
import json

SUPABASE_URL = "https://mrxlzcfjlgjasntamxqa.supabase.co"
SUPABASE_KEY = "sb_publishable_j7flrOZfIi7CVlZXZ0Z-_w_eq2kwkJp"
BOT_TOKEN = "8551974158:AAFOferAxCfOwewYaMd8S2mwV7iNT6l7n0k"
CHAT_ID = "293052285"

def fetch_orders():
    """Получить заказы > 50000 из Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/orders?total_amount=gt.50000&select=*&order=total_amount.desc"
    req = urllib.request.Request(url, headers={
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    })
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())

def send_telegram(text):
    """Отправить сообщение в Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = json.dumps({
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())

def main():
    orders = fetch_orders()

    if not orders:
        print("Нет заказов > 50 000 ₸")
        return

    # Сводка
    total = sum(o["total_amount"] for o in orders)

    msg = f"🚨 <b>Крупные заказы (свыше 50 000 ₸)</b>\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"📊 Найдено: <b>{len(orders)}</b> заказов\n"
    msg += f"💰 На сумму: <b>{int(total):,} ₸</b>\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━━\n\n"

    for i, o in enumerate(orders[:10], 1):
        amount = int(o["total_amount"])
        items = o.get("items", [])
        product = items[0]["productName"] if items else "—"
        # Укорачиваем название товара
        if len(product) > 30:
            product = product[:30] + "…"

        msg += f"<b>#{i}</b> {o['first_name']} {o['last_name']} — {o['city']}\n"
        msg += f"   {product} → <b>{amount:,} ₸</b>\n"

    msg += f"🔗 <a href='https://gbc-analytics-dashboard-opal.vercel.app'>Открыть дашборд</a>"

    result = send_telegram(msg)

    if result.get("ok"):
        print(f"✓ Уведомление отправлено! {len(orders)} заказов > 50 000 ₸")
    else:
        print(f"✗ Ошибка: {result}")

if __name__ == "__main__":
    main()
