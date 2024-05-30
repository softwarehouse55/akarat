import logging
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackQuery
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Connect to the database
conn = sqlite3.connect("real_estate.db")
c = conn.cursor()

# Columns for filtering properties
columns = [
    "type", "transaction_type", "location", "floor", "bedrooms", "direction", "view", 
    "license", "amenities", "maintenance", "expected_delivery_date", "area", "price", 
    "payment_flexibility", "contact_phone", "notes", "finishing", "rating", "transaction_status"
]

# Column descriptions and proposed values for each property
column_descriptions = {
    "type": "نوع العقار",
    "transaction_type": "نوع المعاملة العقارية",
    "location": "الموقع",
    "floor": "الطابق",
    "bedrooms": "عدد الغرف",
    "direction": "الإتجاه",
    "view": "الإطلالة",
    "license": "الترخيص",
    "amenities": "المرافق",
    "maintenance": "الصيانة",
    "expected_delivery_date": "التاريخ المتوقع للتسليم",
    "area": "المساحة",
    "price": "السعر",
    "payment_flexibility": "المرونة في الدفع",
    "contact_phone": "هاتف الإتصال",
    "notes": "ملاحظات",
    "finishing": "التجهيزات",
    "rating": "التقييم",
    "transaction_status": "حالة المعاملة"
}

proposed_values = {
    "type": ["شقة 🏢", "فيلا 🏡", "منزل 🏠", "أرض 🏞️", "شاليه 🏖️", "شقة طلابيةمشتركة 🏠🏢", "مزرعة 🚜"],
    "transaction_type": ["بيع 💰", "إيجار 🏠", "أسهم 🎯", "إيجار مفروش 🛋️", "إستثمار 📆"],
    "location": [],
    "floor": ["أرضي ⬇️", "طابق أول 🔝", "طابق ثاني 🔝🔝", "طابق ثالث 🔝🔝🔝", "طابق رابع 🔝🔝🔝🔝", " طابق خامس وما فوق+ 🔝🔝🔝🔝🔝"],
    "bedrooms": ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣+"],
    "direction": ["شمال ⬆️", "جنوب ⬇️", "شرق ➡️", "غرب ⬅️"],
    "view": ["حديقة 🌳", "شارع 🛣️", "مدرسة 🏫", "ساحة 🏞️", "بناء مقابل 🏗️", "حقل زراعي 🌾"],
    "license": ["طابو 📜", "حكم محكمة ⚖️", "قرارا شطب 🚫", "رخصة بناء 🏗️", "عقد إيجار 📝", "تصريح بناء 🏢", "عقد بيع 💱"],
    "amenities": ["مسبح 🏊", "حديقة 🌳", "موقف سيارات 🅿️", "نادي صحي 💪", "حديقة خاصة 🏞️", "نظام أمان 🚨", "مصعد 🏗", "مطبخ مجهز 🍽️"],
    "maintenance": ["بحاجة دهان 🎨", "بحاجة إصلاحات معينة 🔧", "تحتاج تجديدات 🚧", "لا يحتاج صيانة 🚫", "تحتاج ترميمات 🏗️"],
    "expected_delivery_date": ["تسليم فوري 🚚", "تسليم عند إنتهاء العقد الحالي ⏳", "تسليم في خلال 6 أشهر 🗓️", "تسليم في خلال سنة 📅", "تسليم في خلال 3 سنوات ⌛", "تسليم في خلال 5 سنوات ⌛"],
    "area": [],
    "price": [],
    "payment_flexibility": ["كامل المبلغ 💰", "أقساط 📆", "شهري 📅", "نصف سنوي 🗓️", "سنوي 📅", "تمويل بنكي 🏦"],
    "contact_phone": [],
    "notes": ["ملاحظة عقارية ✍️", "تحذير ⚠️", "معلومة ℹ️", "سؤال ❓", "طلب 📢", "حجز مسبق 🎟️", "عرض خاص 🎁", "فرصة استثمارية 💼"],
    "finishing": ["سوبر لوكس 💎", "تشطيب عادي 🛠️", "نصف تشطيب 🏗️", "تحت التشطيب 🚧", "تشطيب فندقي 🏨", "تشطيب ممتاز 🌟", "تشطيب سوبر ديلوكس 🎖️"],
    "rating": ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
    "transaction_status": ["بالإنتظار", "مفتوحة", "منتهية"]
}



# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with three buttons."""
    # Create buttons for the start menu
    keyboard = [
        [
            InlineKeyboardButton("البحث عن عقار 🏘️", callback_data="search_properties"),
            InlineKeyboardButton("إضافة عقارك الخاص 🏡", callback_data="add_property"),
        ],
        [InlineKeyboardButton("التواصل مع فريقنا 💬", callback_data="contact_us")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = """أهلاً وسهلاً بك في بوت العقارات 🏠! نحن سعداء بزيارتك! 😊
يرجى اختيار أحد الخيارات التالية:"""
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup)

# Button handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button clicks and navigate based on the selected option."""
    query = update.callback_query
    await query.answer()

    logger.info(f"Button clicked with data: {query.data}")

    if query.data == "search_properties":
        # Initialize filters_dict
        context.user_data["filters_dict"] = {}
        # Start property search
        logger.info("Starting property search...")
        await search_properties(update, context, query, 0)  # Start filtering with the first column
    elif query.data == "add_property":
        # Initialize property details and step index
        context.user_data["property_details"] = {}
        context.user_data["property_step"] = 0
        await add_property_step(update, context)  # Start adding property details
    elif query.data == "contact_us":
        # Display contact information
        keyboard = [[InlineKeyboardButton("العودة إلى البداية", callback_data="start")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("للتواصل معي عبر التلجرام: @softwarehouse55", reply_markup=reply_markup)

    elif query.data == "start":
        # Go back to start menu
        await start(update, context)
    else:
        # Handle the input for property addition or search
        if "search_" in query.data:
            # Update filters_dict for searching
            property_step = context.user_data.get("current_column_index", 0) - 1
            current_column = columns[property_step]
            filters_dict = context.user_data["filters_dict"]
            filters_dict[current_column] = query.data.split("_", 1)[1]
            await search_properties(update, context, query, context.user_data["current_column_index"])
        else:
            # Handle the input for property addition
            property_step = context.user_data.get("property_step", 0)
            current_column = columns[property_step - 1]
            context.user_data["property_details"][current_column] = query.data
            await add_property_step(update, context)

# Search properties handler
async def search_properties(update: Update, context: ContextTypes.DEFAULT_TYPE, query: CallbackQuery, column_index: int) -> None:
    """Filter properties based on the chosen column and value."""
    logger.info(f"search_properties called with column_index: {column_index}")

    filters_dict = context.user_data["filters_dict"]

    if column_index >= len(columns):
        await query.edit_message_text(text="لا يوجد المزيد من الأعمدة لتصفية.")
        return

    current_column = columns[column_index]
    query_text = "SELECT COUNT(*) FROM properties WHERE transaction_status = 'بالإنتظار'"
    query_params = []

    for col, val in filters_dict.items():
        query_text += f" AND {col} = ?"
        query_params.append(val)

    logger.info(f"Executing SQL: {query_text} with params: {query_params}")
    c.execute(query_text, query_params)
    open_properties_count = c.fetchone()[0]

    logger.info(f"Open properties count: {open_properties_count}")

    if open_properties_count == 1:
        query_text = "SELECT * FROM properties WHERE transaction_status = 'بالإنتظار'"
        query_params = []

        for col, val in filters_dict.items():
            query_text += f" AND {col} = ?"
            query_params.append(val)

        logger.info(f"Executing SQL: {query_text} with params: {query_params}")
        c.execute(query_text, query_params)
        property_details = c.fetchone()
        if property_details:
            keyboard = [[InlineKeyboardButton("العودة إلى البداية", callback_data="start")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                text=f"""تفاصيل العقار المتاح:
المرجع: {property_details[0]}
نوع العقار: {property_details[1]}
نوع المعاملة العقارية: {property_details[2]}
الموقع: {property_details[3]}
الطابق: {property_details[4]}
عدد الغرف: {property_details[5]}
الإتجاه: {property_details[6]}
الإطلالة: {property_details[7]}
الترخيص: {property_details[8]}
المرافق: {property_details[9]}
الصيانة: {property_details[10]}
التاريخ المتوقع للتسليم: {property_details[11]}
المساحة: {property_details[12]}
السعر: {property_details[13]}
المرونة في الدفع: {property_details[14]}
هاتف الإتصال: {property_details[15]}
ملاحظات: {property_details[16]}
التجهيزات: {property_details[17]}
التقييم: {property_details[18]}
حالة المعاملة: {property_details[19]}""",
                reply_markup=reply_markup
            )
        else:
            await query.edit_message_text(text="لا توجد تفاصيل متاحة لهذا العقار.")
    else:
        query_text = f"SELECT DISTINCT {current_column} FROM properties WHERE transaction_status = 'بالإنتظار'"
        query_params = []

        for col, val in filters_dict.items():
            query_text += f" AND {col} = ?"
            query_params.append(val)

        logger.info(f"Executing SQL: {query_text} with params: {query_params}")
        c.execute(query_text, query_params)
        unique_values = c.fetchall()

        if unique_values:
            keyboard = []
            for value in unique_values:
                keyboard.append([InlineKeyboardButton(value[0], callback_data=f"search_{value[0]}")])
            keyboard.append([InlineKeyboardButton("إلغاء", callback_data="start")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                text=f"اختر {column_descriptions[current_column]}:",
                reply_markup=reply_markup
            )
            context.user_data["current_column_index"] = column_index + 1
        else:
            await query.edit_message_text(text="لا توجد قيم فريدة لهذا العمود.")


# Add property handler
async def add_property_step(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Guide the user through the steps of adding a property."""
    step = context.user_data.get("property_step", 0)
    property_details = context.user_data.get("property_details", {})

    if step < len(columns) - 1:
        current_column = columns[step]
        if update.message:
            if step > 0:
                property_details[columns[step - 1]] = update.message.text
            keyboard = []
            for value in proposed_values[current_column]:
                row = [InlineKeyboardButton(value, callback_data=value)]
                keyboard.append(row)
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(f"يرجى اختيار {column_descriptions[current_column]}:", reply_markup=reply_markup)
        elif update.callback_query:
            property_details[columns[step - 1]] = update.callback_query.data
            keyboard = []
            for value in proposed_values[current_column]:
                row = [InlineKeyboardButton(value, callback_data=value)]
                keyboard.append(row)
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.callback_query.message.reply_text(f"يرجى اختيار {column_descriptions[current_column]}:", reply_markup=reply_markup)
        context.user_data["property_step"] += 1
    else:
        property_details[columns[step - 1]] = update.message.text if update.message else update.callback_query.data
        query_text = f"INSERT INTO properties (id, {', '.join(columns)}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        query_params = [
            f"REF+{c.execute('SELECT COUNT(*) FROM properties').fetchone()[0] + 1}",
            property_details.get("type"),
            property_details.get("transaction_type"),
            property_details.get("location"),
            property_details.get("floor"),
            property_details.get("bedrooms"),
            property_details.get("direction"),
            property_details.get("view"),
            property_details.get("license"),
            property_details.get("amenities"),
            property_details.get("maintenance"),
            property_details.get("expected_delivery_date"),
            property_details.get("area"),
            property_details.get("price"),
            property_details.get("payment_flexibility"),
            property_details.get("contact_phone"),
            property_details.get("notes"),
            property_details.get("finishing"),
            property_details.get("rating"),
            "بالإنتظار"
        ]

        c.execute(query_text, query_params)
        conn.commit()

        keyboard = [[InlineKeyboardButton("العودة إلى البداية", callback_data="start")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text("تمت إضافة العقار بنجاح!", reply_markup=reply_markup)
        elif update.callback_query:
            await update.callback_query.message.reply_text("تمت إضافة العقار بنجاح!", reply_markup=reply_markup)
        context.user_data["property_step"] = 0
        context.user_data["property_details"] = {}



# Main function to start the bot
def main() -> None:
    """Start the bot."""
    with open("token.txt") as f:
        token = f.read().strip()
        
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_property_step))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
