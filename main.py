import os
import json
import telebot
import requests
from telebot import types
import time

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_ORDER_WEBHOOK")

if not TOKEN:
    print("ERROR: TELEGRAM_BOT_TOKEN environment variable not set!")
    print("Please add your Telegram bot token as an environment variable.")
    exit(1)

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

peptides = {
    "HGH 191AA (Somatropin)": {"sizes": {"6iu*10vials": 44, "10iu*10vials": 66, "12iu*10vials": 69, "15iu*10vials": 93}},
    "MT-1": {"sizes": {"10mg*10vials": 57}},
    "MT-2 (Melanotan 2 Acetate)": {"sizes": {"10mg*10vials": 57}},
    "PT-141": {"sizes": {"10mg*10vials": 75}},
    "Gonadorelin Acetate": {"sizes": {"2mg*10vials": 40}},
    "DSIP": {"sizes": {"5mg*10vials": 50, "15mg*10vials": 138}},
    "Selank": {"sizes": {"5mg*10vials": 50, "11mg*10vials": 80}},
    "Oxytocin Acetate": {"sizes": {"2mg*10vials": 56}},
    "Epithalon": {"sizes": {"10mg*10vials": 51, "50mg*10vials": 172}},
    "BPC 157": {"sizes": {"5mg*10vials": 51, "10mg*10vials": 82}},
    "ACE-031": {"sizes": {"1mg*10vials": 334}},
    "AICAR": {"sizes": {"50mg*10vials": 75}},
    "Semax": {"sizes": {"5mg*10vials": 52, "11mg*10vials": 75}},
    "Semaglutide": {"sizes": {"5mg*10vials": 46, "10mg*10vials": 63, "15mg*10vials": 85, "20mg*10vials": 108, "30mg*10vials":126}},
    "SS-31": {"sizes": {"10mg*10vials": 115, "50mg*10vials": 458}},
    "Tirzepatide": {"sizes": {
        "5mg*10vials": 51, "10mg*10vials": 69, "15mg*10vials": 92, "20mg*10vials": 110,
        "30mg*10vials": 144, "40mg*10vials": 172, "45mg*10vials": 201, "50mg*10vials": 226, "60mg*10vials": 265
    }},
    "GHRP-2 Acetate": {"sizes": {"5mg*10vials": 40, "10mg*10vials": 63}},
    "GHRP-6 Acetate": {"sizes": {"5mg*10vials": 40, "10mg*10vials": 63}},
    "CJC-1295": {"variants": {
        "Without DAC": {"sizes": {"5mg*10vials": 98, "10mg*10vials": 161}},
        "With DAC": {"sizes": {"5mg*10vials": 184}}
    }},
    "TB500 (Thymosin B4 Acetate)": {"sizes": {"5mg*10vials": 92, "10mg*10vials": 173}},
    "MGF": {"sizes": {"2mg*10vials": 51}},
    "PEG MGF": {"sizes": {"2mg*10vials": 103}},
    "Sermorelin Acetate": {"sizes": {"10mg*10vials": 138, "5mg*10vials": 87}},
    "HCG": {"sizes": {"10000IU*10vials": 179, "5000IU*10vials": 98}},
    "AOD9604": {"sizes": {"5mg*10vials": 131}},
    "Follistatin": {"sizes": {"1mg*10vials": 346}},
    "IGF-1 LR3": {"sizes": {"0.1mg*10vials": 48, "1mg*10vials": 248}},
    "IGF-DES": {"sizes": {"2mg*10vials": 70}},
    "Tesamorelin": {"sizes": {"5mg*10vials": 126, "10mg*10vials": 242}},
    "Ipamorelin": {"sizes": {"5mg*10vials": 49, "10mg*10vials": 87}},
    "GHK-CU": {"sizes": {"50mg*10vials": 40, "100mg*10vials": 57}},
    "KissPeptin-10": {"sizes": {"5mg*10vials": 70, "10mg*10vials": 122}},
    "Thymalin": {"sizes": {"10mg*10vials": 75}},
    "Thymosin Alpha-1": {"sizes": {"5mg*10vials": 103, "10mg*10vials": 190}},
    "MOTS-c": {"sizes": {"10mg*10vials": 80, "40mg*10vials": 236}},
    "FOX04": {"sizes": {"10mg*10vials": 346}},
    "LL37": {"sizes": {"5mg*10vials": 110}},
    "Retatrutide": {"sizes": {"5mg*10vials": 75, "10mg*10vials": 121, "15mg*10vials": 172, "20mg*10vials":199, "30mg*10vials":293, "40mg*10vials":397, "50mg*10vials":496}},
    "Melatonin": {"sizes": {"10mg*10vials": 75}},
    "HGH Fragment 176-191": {"sizes": {"2mg*10vials":57, "5mg*10vials":115}},
    "Dermorphin": {"sizes": {"5mg*10vials":61}},
    "GLP-1": {"sizes": {"5mg*10vials":126}},
    "Glutathione": {"sizes": {"1500mg*10vials":92}},
    "Insulin (3ml)": {"sizes": {"1vial":329}},
    "Bacteriostatic Water": {"sizes": {"3ml/10vials":11, "10ml/10vials":17}},
    "Botulinum toxin 100iu": {"sizes": {"1vial":162}},
    "5-amino-1mq": {"sizes": {"5mg*10vials":57}},
    "HMG 75 IU": {"sizes": {"75 IU *10 vials":76}},
    "EPO 5000 IU": {"sizes": {"5000 IU *10 vials":161}},
    "Cerebrolysin": {"sizes": {"60mg *6 vials":35}},
    "Cagrilintide": {"sizes": {"5mg *10 vials":168, "10mg*10vials":278}},
    "Ara-290": {"sizes": {"10mg*10vials":75}},
    "Snap-8": {"sizes": {"10mg*10vials":52}},
    "Mazdutide": {"sizes": {"10mg*10vials":242}},
    "NAD": {"sizes": {"100mg*10vials":52, "500mg*10vials":91}},
    "Alprostadil": {"sizes": {"20mcg*5vials":161}},
    "GLOW (BBG70)": {"sizes": {"70mg*10vials":248}},
    "KLOW": {"sizes": {"80mg*10vials":297}},
    "Survodutide": {"sizes": {"10mg*10vials":369}},
    "Pinealon": {"sizes": {"5mg*10vials":52, "10mg*10vials":75, "20mg*10vials":115}},
    "KPV": {"sizes": {"5mg*10vials":48, "10mg*10vials":67}},
    "SLU-PP-332": {"sizes": {"5mg*10vials":157}},
    "LIPO-C": {"variants": {
        "without B12": {"sizes": {"10ml*10vials":87}},
        "with B12": {"sizes": {"10ml*10vials":87}}
    }},
    "B12": {"sizes": {"10ml*10vials":46}},
    "Lemon Bottle": {"sizes": {"10ml*10vials":87}},
    "PNC27": {"variants": {
        "5mg": {"sizes": {"5mg*10vials":121}},
        "10mg": {"sizes": {"10mg*10vials":208}}
    }},
    "VIP": {"sizes": {"5mg*10vials":105, "10mg*10vials":190}},
}

additions_map = {
    "BPC 157": [
        {"name": "BPC5 + TB5 (BB10) 10mg*10vials", "price": 126},
        {"name": "BPC10 + TB10 (BB20) 20mg*10vials", "price": 231},
        {"name": "GLOW (BPC10 + GHK-CU50 + TB10) (BBG70) 70mg*10vials", "price": 248},
    ],
    "CJC-1295|Without DAC": [
        {"name": "+ IPA (CP10) 5mg", "price": 126}
    ],
    "Cagrilintide": [
        {"name": "Cagrilintide + Semaglutide 5mg (CS5)", "price": 149},
        {"name": "Cagrilintide + Semaglutide 10mg (CS10)", "price": 265},
    ],
    "GHK-CU": [
        {"name": "KLOW (CU50+TB10+BC10+KPV10) 80mg*10vials", "price": 297},
    ],
}

sessions = {}

STATE_START = "START"
STATE_WAIT_PRODUCT = "WAIT_PRODUCT"
STATE_WAIT_VARIANT = "WAIT_VARIANT"
STATE_WAIT_SIZE = "WAIT_SIZE"
STATE_WAIT_ADDITION = "WAIT_ADDITION"
STATE_WAIT_CONTINUE = "WAIT_CONTINUE"

def start_session(chat_id):
    sessions[chat_id] = {"state": STATE_WAIT_PRODUCT, "cart": [], "current": {}}
    return sessions[chat_id]

def is_variant_product(product):
    return "variants" in peptides[product]

def get_sizes(product, variant=None):
    product_data = peptides[product]
    if variant:
        return product_data["variants"][variant]["sizes"]
    else:
        return product_data["sizes"]

def get_product_full_name(product, variant=None):
    if variant:
        return f"{product} ({variant})"
    return product

def get_additions_key(product, variant=None):
    if variant:
        return f"{product}|{variant}"
    return product

def list_products_keyboard():
    names = list(peptides.keys())
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    row = []
    for i, n in enumerate(names):
        row.append(types.KeyboardButton(n))
        if len(row) >= 2:
            markup.row(*row)
            row = []
    if row:
        markup.row(*row)
    markup.row(types.KeyboardButton("Checkout"), types.KeyboardButton("Cancel"))
    return markup

def variant_keyboard_for(product):
    variants = list(peptides[product]["variants"].keys())
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for v in variants:
        markup.row(types.KeyboardButton(v))
    markup.row(types.KeyboardButton("Back"), types.KeyboardButton("Cancel"))
    return markup

def sizes_keyboard_for(product, variant=None):
    product_data = peptides[product]
    if variant:
        sizes = list(product_data["variants"][variant]["sizes"].keys())
    else:
        sizes = list(product_data["sizes"].keys())
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    row = []
    for s in sizes:
        row.append(types.KeyboardButton(s))
        if len(row) >= 2:
            markup.row(*row)
            row = []
    if row:
        markup.row(*row)
    markup.row(types.KeyboardButton("Back"), types.KeyboardButton("Cancel"))
    return markup

def continue_kb():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.row("Yes", "No")
    return markup

def format_cart(cart):
    lines = []
    total = 0
    for item in cart:
        product = item["product"]
        variant = item.get("variant")
        name = get_product_full_name(product, variant)
        size = item.get("size", "")
        addition = item.get("addition")
        price = item["price"]
        total += price
        line = f"{name} {size} — ${price}"
        if addition:
            line += f" + {addition['name']}"
        lines.append(line)
    lines.append(f"\nTotal: ${total}")
    return "\n".join(lines), total

def send_order_to_discord(user_info, cart_text, total):
    if not DISCORD_WEBHOOK_URL:
        print("Discord webhook URL not configured, skipping Discord notification.")
        return
    try:
        payload = {
            "content": f"🛒 **NEW ORDER**\n\n👤 **Customer:** {user_info}\n\n📦 **Order:**\n```\n{cart_text}\n```\n💰 **Total Amount:** ${total}"
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 204:
            print(f"Order notification sent to Discord successfully")
        else:
            print(f"Discord webhook returned status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error sending order to Discord: {e}")

@bot.message_handler(commands=["start", "restart"])
def cmd_start(message):
    print(f"Received /start command from chat_id: {message.chat.id}")
    chat_id = message.chat.id
    start_session(chat_id)
    reply = "Welcome! Choose a peptide to add to your cart. Tap Checkout when done."
    try:
        bot.send_message(chat_id, reply, reply_markup=list_products_keyboard())
        print(f"Sent welcome message to {chat_id}")
    except Exception as e:
        print(f"Error sending message: {e}")

@bot.message_handler(commands=["cart"])
def cmd_cart(message):
    chat_id = message.chat.id
    sess = sessions.get(chat_id)
    if not sess or not sess["cart"]:
        bot.send_message(chat_id, "Your cart is empty. Use /start to begin.", reply_markup=list_products_keyboard())
        return
    text, total = format_cart(sess["cart"])
    bot.send_message(chat_id, f"Your cart:\n\n{text}")

@bot.message_handler(func=lambda m: True)
def all_messages(message):
    chat_id = message.chat.id
    text = message.text.strip()
    sess = sessions.get(chat_id)
    if not sess:
        sess = start_session(chat_id)

    state = sess["state"]

    if text.lower() in ["cancel","/cancel"]:
        sessions.pop(chat_id, None)
        bot.send_message(chat_id, "Order cancelled. Use /start to start over.", reply_markup=types.ReplyKeyboardRemove())
        return

    if text == "Checkout":
        cart = sess["cart"]
        if not cart:
            bot.send_message(chat_id, "Cart is empty. Please add items.", reply_markup=list_products_keyboard())
            return
        cart_text, total = format_cart(cart)
        bot.send_message(chat_id, f"Checkout — here is your order:\n\n{cart_text}\n\nType 'Confirm' to place the order or 'Cancel' to abort.")
        sess["state"] = STATE_START
        return

    if text.lower() == "confirm":
        cart = sess.get("cart", [])
        if not cart:
            bot.send_message(chat_id, "Nothing to confirm. Cart empty.")
            return
        cart_text, total = format_cart(cart)

        user = message.from_user
        if user.username:
            user_info = f"@{user.username}"
        else:
            user_info = f"User ID: {user.id}"

        send_order_to_discord(user_info, cart_text, total)

        bot.send_message(chat_id, f"✅ Order confirmed!\n\nFinal total: ${total}\n\nThank you! You'll receive a message from our team soon.", reply_markup=types.ReplyKeyboardRemove())
        sessions.pop(chat_id, None)
        return

    if state == STATE_WAIT_PRODUCT:
        if text in peptides:
            sess["current"] = {"product": text}
            if is_variant_product(text):
                sess["state"] = STATE_WAIT_VARIANT
                bot.send_message(chat_id, f"You chose <b>{text}</b>. Pick a variant:", reply_markup=variant_keyboard_for(text))
            else:
                sess["state"] = STATE_WAIT_SIZE
                bot.send_message(chat_id, f"You chose <b>{text}</b>. Now pick a vial size:", reply_markup=sizes_keyboard_for(text))
            return
        else:
            bot.send_message(chat_id, "Please choose a product from the keyboard, or type a product name exactly. Use Checkout to finish.", reply_markup=list_products_keyboard())
            return

    if state == STATE_WAIT_VARIANT:
        current = sess.get("current", {})
        product = current.get("product")
        if not product:
            sess["state"] = STATE_WAIT_PRODUCT
            bot.send_message(chat_id, "Something went wrong — please pick a product again.", reply_markup=list_products_keyboard())
            return
        if text == "Back":
            sess["state"] = STATE_WAIT_PRODUCT
            bot.send_message(chat_id, "Back to products:", reply_markup=list_products_keyboard())
            return
        variants = list(peptides[product]["variants"].keys())
        if text in variants:
            sess["current"]["variant"] = text
            sess["state"] = STATE_WAIT_SIZE
            bot.send_message(chat_id, f"You chose <b>{get_product_full_name(product, text)}</b>. Now pick a vial size:", reply_markup=sizes_keyboard_for(product, text))
            return
        else:
            bot.send_message(chat_id, "Please choose a variant from the keyboard.", reply_markup=variant_keyboard_for(product))
            return

    if state == STATE_WAIT_SIZE:
        current = sess.get("current", {})
        product = current.get("product")
        variant = current.get("variant")
        if not product:
            sess["state"] = STATE_WAIT_PRODUCT
            bot.send_message(chat_id, "Something went wrong — please pick a product again.", reply_markup=list_products_keyboard())
            return
        if text == "Back":
            if variant:
                sess["state"] = STATE_WAIT_VARIANT
                sess["current"].pop("variant", None)
                bot.send_message(chat_id, "Back to variant selection:", reply_markup=variant_keyboard_for(product))
            else:
                sess["state"] = STATE_WAIT_PRODUCT
                bot.send_message(chat_id, "Back to products:", reply_markup=list_products_keyboard())
            return
        sizes = get_sizes(product, variant)
        if text in sizes:
            chosen_price = sizes[text]
            sess["current"].update({"size": text, "price": chosen_price})
            additions_key = get_additions_key(product, variant)
            if additions_key in additions_map and additions_map[additions_key]:
                sess["state"] = STATE_WAIT_ADDITION
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                for a in additions_map[additions_key]:
                    markup.row(types.KeyboardButton(a["name"]))
                markup.row(types.KeyboardButton("No, thanks"))
                bot.send_message(chat_id, f"Would you like any of these additions for <b>{get_product_full_name(product, variant)}</b>?", reply_markup=markup)
                return
            else:
                full_name = get_product_full_name(product, variant)
                item = {"product": product, "variant": variant, "size": text, "price": chosen_price}
                sess["cart"].append(item)
                sess["state"] = STATE_WAIT_CONTINUE
                bot.send_message(chat_id, f"✅ Added: {full_name} {text} — ${chosen_price}\n\nContinue shopping?", reply_markup=continue_kb())
                return
        else:
            bot.send_message(chat_id, "Please choose a valid vial size from the keyboard.", reply_markup=sizes_keyboard_for(product, variant))
            return

    if state == STATE_WAIT_ADDITION:
        current = sess.get("current", {})
        product = current.get("product")
        variant = current.get("variant")
        chosen_size = current.get("size")
        base_price = current.get("price", 0)
        additions_key = get_additions_key(product, variant)
        available = additions_map.get(additions_key, [])
        if text.lower() in ["no","no, thanks","no thanks","no,thanks"]:
            full_name = get_product_full_name(product, variant)
            item = {"product": product, "variant": variant, "size": chosen_size, "price": base_price}
            sess["cart"].append(item)
            sess["state"] = STATE_WAIT_CONTINUE
            bot.send_message(chat_id, f"✅ Added: {full_name} {chosen_size} — ${base_price}\n\nContinue shopping?", reply_markup=continue_kb())
            return
        matched = None
        for a in available:
            if text == a["name"]:
                matched = a
                break
        if matched:
            item = {"product": product, "variant": variant, "size": chosen_size, "price": matched["price"], "addition": matched}
            sess["cart"].append(item)
            sess["state"] = STATE_WAIT_CONTINUE
            bot.send_message(chat_id, f"✅ Added combo: {matched['name']} — ${matched['price']}\n\nContinue shopping?", reply_markup=continue_kb())
            return
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            for a in available:
                markup.row(types.KeyboardButton(a["name"]))
            markup.row(types.KeyboardButton("No, thanks"))
            bot.send_message(chat_id, "Please pick one of the additions or 'No, thanks'.", reply_markup=markup)
            return

    if state == STATE_WAIT_CONTINUE:
        if text.lower() in ["yes","y"]:
            sess["state"] = STATE_WAIT_PRODUCT
            sess["current"] = {}
            bot.send_message(chat_id, "Ok — pick another peptide:", reply_markup=list_products_keyboard())
            return
        elif text.lower() in ["no","n"]:
            text_cart, total = format_cart(sess["cart"])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.row("Confirm", "Cancel")
            bot.send_message(chat_id, f"Order summary:\n\n{text_cart}\n\nType Confirm to finalize or Cancel to abort.", reply_markup=markup)
            sess["state"] = STATE_START
            return
        else:
            bot.send_message(chat_id, "Please reply Yes or No.", reply_markup=continue_kb())
            return

    bot.send_message(chat_id, "I didn't understand that. Use the keyboard or type /start to begin.", reply_markup=list_products_keyboard())

if __name__ == "__main__":
    print("=" * 50)
    print("Starting Telegram Peptide Order Bot (Polling Mode)")
    print("=" * 50)
    print(f"Bot token configured: {'Yes' if TOKEN else 'No'}")
    print(f"Discord webhook configured: {'Yes' if DISCORD_WEBHOOK_URL else 'No'}")
    print("Bot is now running in polling mode...")
    print("Press Ctrl+C to stop the bot")
    print("=" * 50)

    try:
        bot.remove_webhook()
        print("Removed any existing webhooks")
    except Exception as e:
        print(f"Note: Could not remove webhook: {e}")

    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Error in polling: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
