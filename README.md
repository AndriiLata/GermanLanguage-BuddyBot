# Petra - Find Your German Buddy

Telegram bot that helps connect users with different German levels to practice the language together.

![Screenshots of the bot chat](/petra_screens.png)

## Features

- **Matching Algorithm**: A robust matching function to connect users based on their language-level.
- **User-friendly Commands**: Easy-to-use commands to find a language partner.
- **Database**: Management of user data with a MySQL database.


### Prerequisites

- Python 3.x
- MySQL Database (local or hosted)
- Telegram Bot Token (Create your bot on Telegram and get the token)


## Project Structure

- **bot.py**: Contains all the commands to handle user input and interactions.
- **database.py**: Manages the MySQL database setup, and handles insertions, deletions, and searches for user data.
- **match.py**: Contains the matching function to connect users based on their german level.

## Usage

Once the bot is running, users can interact with it through the following commands:

- **/start**: Initialize the bot and checks if the profile already exists, if not - leads you through the steps to create a user profile.
- **Start Matching**: Starts the matching process and shows user profiles with the same language level
- **❤️**: Sends previous user your contact and a message that you liked him
- **👎**: Shows the next profile
- **Stop**: Returns user to the starting page
   

## Contact

If you have any questions or need help, feel free to open an issue or contact me.
