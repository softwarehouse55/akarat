import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, Filters, Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Function to connect to the SQLite database
def connect_to_database():
    return sqlite3.connect("real_estate.db")

# Handler for the /start command
def start(update: Update, context: CallbackContext) -> None:
    # Define the columns of the database table
    context.user_data['columns'] = [
        'property_type', 'type', 'status', 'location', 'price', 'area', 'rooms',
        'bathrooms', 'description', 'add_date', 'seller_info', 'floor', 'amenities',
        'age', 'maintenance', 'images', 'current_owner', 'expected_delivery_date',
        'rating', 'views', 'finishing', 'view', 'orientation', 'security',
        'nearby_services', 'interior_layout', 'landscape', 'transportation',
        'permits', 'fixtures', 'payment_flexibility', 'legal_status', 'environmental_rating',
        'updates_renovations', 'construction_date'
    ]
    
    update.message.reply_text('Please choose an attribute to fill:')
    show_next_attribute(update, context)

# Function to display the next attribute to fill
def show_next_attribute(update: Update, context: CallbackContext) -> None:
    # Check if the current attribute index exists in the user data
    if 'current_attribute_index' not in context.user_data:
        context.user_data['current_attribute_index'] = 0
    
    # Check if there are more attributes to display
    if context.user_data['current_attribute_index'] < len(context.user_data['columns']):
        attribute = context.user_data['columns'][context.user_data['current_attribute_index']]
        context.user_data['current_attribute_index'] += 1
        keyboard = [
            [InlineKeyboardButton(attribute.replace('_', ' ').title(), callback_data=attribute)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose an attribute to fill:', reply_markup=reply_markup)
    else:
        save_data(update, context)

# Function to save the data to the database
def save_data(update: Update, context: CallbackContext) -> None:
    # Check if there is data to save
    if 'data' in context.user_data:
        data = context.user_data['data']
        conn = connect_to_database()
        cursor = conn.cursor()
        # Insert the data into the database
        cursor.execute("INSERT INTO properties VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(data.values()))
        conn.commit()
        conn.close()
        update.message.reply_text("Data saved successfully!")
        del context.user_data['data']
    else:
        update.message.reply_text("No data to save!")

# Handler for button clicks
def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    context.user_data['current_attribute'] = query.data
    query.edit_message_text(text=f"Please enter the value for {query.data.replace('_', ' ').title()}:")

# Handler for text messages
def message_handler(update: Update, context: CallbackContext) -> None:
    if 'current_attribute' in context.user_data:
        attribute = context.user_data['current_attribute']
        value = update.message.text
        
        if 'data' not in context.user_data:
            context.user_data['data'] = {}

        context.user_data['data'][attribute] = value

        show_next_attribute(update, context)
    else:
        update.message.reply_text("Please start by selecting an attribute.")

# Main function to start the bot
def main() -> None:
    updater = Updater('YOUR_TELEGRAM_BOT_TOKEN')
    dispatcher = updater.dispatcher

    # Add handlers for commands, button clicks, and text messages
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_click))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    # Start the bot
    updater.start_polling()
    updater.idle()

# Entry point of the program
if __name__ == '__main__':
    main()

