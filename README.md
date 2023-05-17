## Telegram Stock News Project
This script gets information about a stock from alphavantage's API and checks if
the price variation from yesterday in comparison to the day before reaches a minimum value.
If it does, it gets the top 3 news articles from the news API and then sends their headlines,
descriptions and the price variation from a Telegram bot to a user.  
The environment variables are loaded by the dotenv module from a local .env file.