# Real Estate Bot 🏠

## Overview
Real Estate Bot is a Telegram application that helps users search for available properties and add their own properties easily. The bot provides an interactive interface with multiple options to meet different users' needs in the real estate world.

## Features ✨
- **Search Properties 🏘️:** Filter available properties based on multiple criteria such as type, price, location, and more.
- **Add Your Own Property 🏡:** Add details of your property to appear in the list of available properties for potential buyers or renters.
- **Contact Support Team 💬:** The bot offers an option to contact the support team for any inquiries or issues.

## Requirements 📋
- A Telegram account
- A bot token from [BotFather](https://core.telegram.org/bots#botfather)
- A configured SQLite database

## How to Run 🚀
1. **Clone the repository:**
    ```bash
    git clone https://github.com/softwarehouse55/akarat
    ```
2. **Install the requirements:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Initialize the database:**
    Create the `real_estate.db` database and ensure the required table exists:
    ```bash
    python create_db.py
    ```
4. **Add the token:**
    Create a file named `token.txt` and put your bot token inside it.
5. **Run the bot:**
    ```bash
    python bot.py
    ```

## Using the Bot 🤖
- When the bot starts, you will be presented with an interface containing three options:
  - **Search Properties 🏘️**
  - **Add Your Own Property 🏡**
  - **Contact Our Team 💬**
- Follow the instructions provided for each option to complete the desired action.

## Contribution 💡
We welcome all contributions to improve the bot. You can open a new issue or submit a pull request on [GitHub](https://github.com/softwarehouse55/real-estate-bot).

## Contact Us 📞
If you have any inquiries or need assistance, you can contact us via Telegram at: [@softwarehouse55](https://t.me/softwarehouse55)

## License 📄
This project is licensed under the [MIT License](LICENSE).

---

We are always looking to improve your experience in searching for and managing properties. Thank you for using Real Estate Bot! 🌟

---

*Note: Make sure to replace "softwarehouse55" with your actual GitHub username in the links.*