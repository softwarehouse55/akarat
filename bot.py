import logging
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackQuery
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Connect to the database
conn = sqlite3.connect("real_estate.db")
c = conn.cursor()

# Columns for filtering properties
columns = [
    "type", "status", "location", "price", "area", "bedrooms", "bathrooms", 
    "description", "interior_design", "floor", "license", "amenities", 
    "payment_flexibility", "facilities", "rating", "finishing", "view", 
    "direction", "expected_delivery_date", "age", "maintenance", "images", 
    "current_owner", "views", "security", "nearby_services", 
    "transaction_status", "contact_phone", "notes"
]

# Filter dictionary and property details dictionary
filters_dict = {}

# Column descriptions and proposed values for each property
column_descriptions = {
    "type": "賳賵毓 丕賱毓賯丕乇",
    "status": "丕賱丨丕賱丞",
    "location": "丕賱賲賵賯毓",
    "price": "丕賱爻毓乇",
    "area": "丕賱賲爻丕丨丞",
    "bedrooms": "毓丿丿 丕賱睾乇賮",
    "bathrooms": "毓丿丿 丕賱丨賲丕賲丕鬲",
    "description": "丕賱賵氐賮",
    "interior_design": "丕賱鬲氐賲賷賲 丕賱丿丕禺賱賷",
    "floor": "丕賱胤丕亘賯",
    "license": "丕賱乇禺氐丞",
    "amenities": "賵爻丕卅賱 丕賱乇丕丨丞",
    "payment_flexibility": "賲乇賵賳丞 丕賱丿賮毓",
    "facilities": "丕賱賲乇丕賮賯",
    "rating": "丕賱鬲賯賷賷賲",
    "finishing": "丕賱鬲卮胤賷亘",
    "view": "丕賱廿胤賱丕賱丞",
    "direction": "丕賱丕鬲噩丕賴",
    "expected_delivery_date": "鬲丕乇賷禺 丕賱鬲爻賱賷賲 丕賱賲鬲賵賯毓",
    "age": "丕賱毓賲乇",
    "maintenance": "丨丕賱丞 丕賱氐賷丕賳丞",
    "images": "乇賵丕亘胤 丕賱氐賵乇",
    "current_owner": "丕賱賲丕賱賰 丕賱丨丕賱賷",
    "views": "毓丿丿 丕賱賲卮丕賴丿丕鬲",
    "security": "賲爻鬲賵賶 丕賱兀賲丕賳",
    "nearby_services": "丕賱禺丿賲丕鬲 丕賱賯乇賷亘丞",
    "transaction_status": "丨丕賱丞 丕賱氐賮賯丞",
    "contact_phone": "乇賯賲 丕賱丕鬲氐丕賱",
    "notes": "賲賱丕丨馗丕鬲"
}

proposed_values = {
    "type": ["卮賯丞", "賮賷賱丕", "賲賳夭賱", "兀乇囟"],
    "status": ["噩丿賷丿", "賲爻鬲毓賲賱"],
    "location": ["賲丿賷賳丞", "囟賵丕丨賷", "賯乇賷丞"],
    "price": ["100000", "200000", "300000", "400000"],
    "area": ["100", "200", "300", "400"],
    "bedrooms": ["1", "2", "3", "4", "5+"],
    "bathrooms": ["1", "2", "3", "4+"],
    "description": ["賲鬲賵爻胤", "噩賷丿", "賲賲鬲丕夭"],
    "interior_design": ["亘爻賷胤", "毓氐乇賷", "賰賱丕爻賷賰賷"],
    "floor": ["兀乇囟賷", "胤丕亘賯 兀賵賱", "胤丕亘賯 孬丕賳賷", "胤丕亘賯 孬丕賱孬+"],
    "license": ["賲乇禺氐", "睾賷乇 賲乇禺氐"],
    "amenities": ["賲爻亘丨", "丨丿賷賯丞", "賲賵賯賮 爻賷丕乇丕鬲"],
    "payment_flexibility": ["賰丕卮", "鬲賯爻賷胤"],
    "facilities": ["兀賲賳", "賲氐毓丿", "賲爻噩丿"],
    "rating": ["1", "2", "3", "4", "5"],
    "finishing": ["爻賵亘乇 賱賵賰爻", "鬲卮胤賷亘 毓丕丿賷"],
    "view": ["亘丨乇", "丨丿賷賯丞", "卮丕乇毓"],
    "direction": ["卮賲丕賱", "噩賳賵亘", "卮乇賯", "睾乇亘"],
    "expected_delivery_date": ["賯乇賷亘丕賸", "賮賷 丕賱賲爻鬲賯亘賱"],
    "age": ["噩丿賷丿", "賲爻鬲毓賲賱"],
    "maintenance": ["賲胤賱賵亘丞", "睾賷乇 賲胤賱賵亘丞"],
    "images": ["乇丕亘胤1", "乇丕亘胤2", "乇丕亘胤3"],
    "current_owner": ["丕賱賲丕賱賰", "丕賱賵賰賷賱"],
    "views": ["100", "200", "300", "400"],
    "security": ["賲賲鬲丕夭", "噩賷丿", "賲毓鬲丿賱"],
    "nearby_services": ["賲丿乇爻丞", "賲丨賱 鬲噩丕乇賷", "賲爻鬲卮賮賶"]
}

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with three buttons."""
    filters_dict.clear()
    
    # Create buttons for the start menu
    keyboard = [
        [
            InlineKeyboardButton("丕賱亘丨孬 毓賳 毓賯丕乇 馃彉锔�", callback_data="search_properties"),
            InlineKeyboardButton("廿囟丕賮丞 毓賯丕乇賰 丕賱禺丕氐 馃彙", callback_data="add_property"),
        ],
        [InlineKeyboardButton("丕賱鬲賵丕氐賱 賲毓 賮乇賷賯賳丕 馃挰", callback_data="contact_us")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = """兀賴賱丕賸 賵爻賴賱丕賸 亘賰 賮賷 亘賵鬲 丕賱毓賯丕乇丕鬲 馃彔! 賳丨賳 爻毓丿丕亍 亘夭賷丕乇鬲賰! 馃槉
賷乇噩賶 丕禺鬲賷丕乇 兀丨丿 丕賱禺賷丕乇丕鬲 丕賱鬲丕賱賷丞:"""
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup)


# Button handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button clicks and navigate based on the selected option."""
    query = update.callback_query
    await query.answer()

    if query.data == "search_properties":
        await search_properties(update, context, query, 0)  # Start filtering with the first column
    elif query.data == "add_property":
        context.user_data["property_details"] = {}
        context.user_data["property_step"] = 0
        await add_property_step(update, context)  # Removed the third argument 'query'
    elif query.data == "contact_us":
        await query.edit_message_text("賱賱鬲賵丕氐賱 賲毓賷 毓亘乇 丕賱鬲賱噩乇丕賲: @softwarehouse55")
    elif query.data == "start":
        await start(update, context)
    else:
        column_index = context.user_data.get("current_column_index", 0)
        column_name = columns[column_index - 1]
        filters_dict[column_name] = query.data
        await search_properties(update, context, query, column_index)



# Search properties handler
async def search_properties(update: Update, context: ContextTypes.DEFAULT_TYPE, query: CallbackQuery, column_index: int) -> None:
    """Filter properties based on the chosen column and value."""
    if column_index >= len(columns):
        await query.edit_message_text(text="賱丕 賷賵噩丿 丕賱賲夭賷丿 賲賳 丕賱兀毓賲丿丞 賱鬲氐賮賷丞.")
        return

    current_column = columns[column_index]
    query_text = "SELECT COUNT(*) FROM properties WHERE transaction_status = '賲賮鬲賵丨丞'"
    query_params = []

    for col, val in filters_dict.items():
        query_text += f" AND {col} = ?"
        query_params.append(val)

    c.execute(query_text, query_params)
    open_properties_count = c.fetchone()[0]

    if open_properties_count == 1:
        query_text = "SELECT * FROM properties WHERE transaction_status = '賲賮鬲賵丨丞'"
        query_params = []

        for col, val in filters_dict.items():
            query_text += f" AND {col} = ?"
            query_params.append(val)

        c.execute(query_text, query_params)
        property_details = c.fetchone()
        if property_details:
            keyboard = [[InlineKeyboardButton("丕賱毓賵丿丞 廿賱賶 丕賱亘丿丕賷丞", callback_data="start")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                text=f"""鬲賮丕氐賷賱 丕賱毓賯丕乇 丕賱賲鬲丕丨:
賳賵毓 丕賱毓賯丕乇: {property_details[1]}
丕賱丨丕賱丞: {property_details[2]}
丕賱爻毓乇: {property_details[3]}
丕賱賲賵賯毓: {property_details[4]}
丕賱賲爻丕丨丞: {property_details[5]}
丕賱睾乇賮: {property_details[6]}
丕賱丨賲丕賲丕鬲: {property_details[7]}
丕賱賵氐賮: {property_details[8]}
丕賱鬲氐賲賷賲 丕賱丿丕禺賱賷: {property_details[9]}
丕賱胤丕亘賯: {property_details[10]}
丕賱乇禺氐丞: {property_details[11]}
丕賱賲乇丕賮賯: {property_details[12]}
賲乇賵賳丞 丕賱丿賮毓: {property_details[13]}
賵爻丕卅賱 丕賱乇丕丨丞: {property_details[14]}
丕賱鬲賯賷賷賲: {property_details[15]}
丕賱鬲卮胤賷亘: {property_details[16]}
丕賱廿胤賱丕賱丞: {property_details[17]}
丕賱丕鬲噩丕賴: {property_details[18]}
鬲丕乇賷禺 丕賱鬲爻賱賷賲 丕賱賲鬲賵賯毓: {property_details[19]}
丕賱毓賲乇: {property_details[20]}
丕賱氐賷丕賳丞: {property_details[21]}
丕賱氐賵乇: {property_details[22]}
丕賱賲丕賱賰 丕賱丨丕賱賷: {property_details[23]}
丕賱賲卮丕賴丿丕鬲: {property_details[24]}
丕賱兀賲丕賳: {property_details[25]}
丕賱禺丿賲丕鬲 丕賱賯乇賷亘丞: {property_details[26]}
丨丕賱丞 丕賱氐賮賯丞: {property_details[27]}
乇賯賲 丕賱丕鬲氐丕賱: {property_details[28]}
賲賱丕丨馗丕鬲: {property_details[29]}""",
                reply_markup=reply_markup
            )
        else:
            await query.edit_message_text(text="賱丕 鬲賵噩丿 鬲賮丕氐賷賱 賲鬲丕丨丞 賱賴匕丕 丕賱毓賯丕乇.")
    else:
        query_text = f"SELECT DISTINCT {current_column} FROM properties WHERE transaction_status = '賲賮鬲賵丨丞'"
        query_params = []

        for col, val in filters_dict.items():
            query_text += f" AND {col} = ?"
            query_params.append(val)

        c.execute(query_text, query_params)
        unique_values = c.fetchall()

        if unique_values:
            keyboard = [
                [InlineKeyboardButton(value[0], callback_data=value[0]) for value in unique_values],
                [InlineKeyboardButton("丕賱毓賵丿丞 廿賱賶 丕賱亘丿丕賷丞", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                text=f"丕禺鬲乇 賯賷賲丞 賱賭 {current_column}:", reply_markup=reply_markup
            )
        else:
            await query.edit_message_text(text=f"賱丕 鬲賵噩丿 賯賷賲 賮乇賷丿丞 賱賭 {current_column}.")

    context.user_data["current_column_index"] = column_index + 1

# Add property step-by-step handler
async def add_property_step(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the step-by-step collection of new property details from the user."""
    step = context.user_data["property_step"]
    property_details = context.user_data["property_details"]
    
    prompts = [
        "賷乇噩賶 廿丿禺丕賱 賳賵毓 丕賱毓賯丕乇:",
        "賷乇噩賶 廿丿禺丕賱 丕賱丨丕賱丞:",
        "賷乇噩賶 廿丿禺丕賱 丕賱爻毓乇:",
        "賷乇噩賶 廿丿禺丕賱 丕賱賲賵賯毓:",
        "賷乇噩賶 廿丿禺丕賱 丕賱賲爻丕丨丞:",
        "賷乇噩賶 廿丿禺丕賱 毓丿丿 丕賱睾乇賮:",
        "賷乇噩賶 廿丿禺丕賱 毓丿丿 丕賱丨賲丕賲丕鬲:",
        "賷乇噩賶 廿丿禺丕賱 丕賱賵氐賮:",
        "賷乇噩賶 廿丿禺丕賱 丕賱鬲氐賲賷賲 丕賱丿丕禺賱賷:",
        "賷乇噩賶 廿丿禺丕賱 丕賱胤丕亘賯:",
        "賷乇噩賶 廿丿禺丕賱 丕賱乇禺氐丞:",
        "賷乇噩賶 廿丿禺丕賱 賵爻丕卅賱 丕賱乇丕丨丞:",
        "賷乇噩賶 廿丿禺丕賱 賲乇賵賳丞 丕賱丿賮毓:",
        "賷乇噩賶 廿丿禺丕賱 丕賱賲乇丕賮賯:",
        "賷乇噩賶 廿丿禺丕賱 丕賱鬲賯賷賷賲:",
        "賷乇噩賶 廿丿禺丕賱 丕賱鬲卮胤賷亘:",
        "賷乇噩賶 廿丿禺丕賱 丕賱廿胤賱丕賱丞:",
        "賷乇噩賶 廿丿禺丕賱 丕賱丕鬲噩丕賴:",
        "賷乇噩賶 廿丿禺丕賱 鬲丕乇賷禺 丕賱鬲爻賱賷賲 丕賱賲鬲賵賯毓:",
        "賷乇噩賶 廿丿禺丕賱 丕賱毓賲乇:",
        "賷乇噩賶 廿丿禺丕賱 丨丕賱丞 丕賱氐賷丕賳丞:",
        "賷乇噩賶 廿丿禺丕賱 乇賵丕亘胤 丕賱氐賵乇:",
        "賷乇噩賶 廿丿禺丕賱 丕賱賲丕賱賰 丕賱丨丕賱賷:",
        "賷乇噩賶 廿丿禺丕賱 毓丿丿 丕賱賲卮丕賴丿丕鬲:",
        "賷乇噩賶 廿丿禺丕賱 賲爻鬲賵賶 丕賱兀賲丕賳:",
        "賷乇噩賶 廿丿禺丕賱 丕賱禺丿賲丕鬲 丕賱賯乇賷亘丞:"
    ]

    if step < len(prompts):
        if update.message:
            # Save the user's input from the previous step
            if step > 0:
                property_details[columns[step-1]] = update.message.text

            await update.message.reply_text(prompts[step])
            context.user_data["property_step"] += 1
        elif update.callback_query:
            await update.callback_query.message.reply_text(prompts[step])
            context.user_data["property_step"] += 1
    else:
        # Final step: insert the property into the database
        property_details[columns[step-1]] = update.message.text if update.message else ""
        query_text = f"INSERT INTO properties (id, {', '.join(columns)}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        query_params = [
            f"REF+{c.execute('SELECT COUNT(*) FROM properties').fetchone()[0] + 1}",
            property_details.get("type"),
            property_details.get("status"),
            property_details.get("location"),
            property_details.get("price"),
            property_details.get("area"),
            property_details.get("bedrooms"),
            property_details.get("bathrooms"),
            property_details.get("description"),
            property_details.get("interior_design"),
            property_details.get("floor"),
            property_details.get("license"),
            property_details.get("amenities"),
            property_details.get("payment_flexibility"),
            property_details.get("facilities"),
            property_details.get("rating"),
            property_details.get("finishing"),
            property_details.get("view"),
            property_details.get("direction"),
            property_details.get("expected_delivery_date"),
            property_details.get("age"),
            property_details.get("maintenance"),
            property_details.get("images"),
            property_details.get("current_owner"),
            property_details.get("views"),
            property_details.get("security"),
            property_details.get("nearby_services"),
            "亘丕賱廿賳鬲馗丕乇",
            "賱丕 賷賵噩丿",
            "賱丕 賷賵噩丿"
        ]

        c.execute(query_text, query_params)
        conn.commit()

        keyboard = [[InlineKeyboardButton("丕賱毓賵丿丞 廿賱賶 丕賱亘丿丕賷丞", callback_data="start")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("鬲賲鬲 廿囟丕賮丞 丕賱毓賯丕乇 亘賳噩丕丨!", reply_markup=reply_markup)
        context.user_data["property_step"] = 0
        context.user_data["property_details"] = {}


# Main function to start the bot
def main() -> None:
    """Start the bot."""
    with open("token.txt") as f:
        token = f.read().strip()
        
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_property_step))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()