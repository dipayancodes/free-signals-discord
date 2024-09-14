import requests
from bs4 import BeautifulSoup
import json

# Screener URL for your filtered stocks
filtered_stocks_url = 'https://www.screener.in/screens/2033673/a/'  # Replace with your actual screen URL

# Discord Webhook URL
webhook_url = 'https://discord.com/api/webhooks/1284440879813234758/UIsn5HMs5fPbmuJYa48RsRcUMPVYAwzjk7Wkf9qXINoYMvbk49gaCWUU-TPIAF305rbg'
# Function to fetch stock data from Screener
def fetch_stocks():
    response = requests.get(filtered_stocks_url)
    if response.status_code != 200:
        print(f"Failed to fetch the page, status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    stock_table = soup.find('table')  # Modify this depending on Screener's page structure

    stocks = []
    if stock_table:
        for row in stock_table.find_all('tr')[1:]:  # Skip the header row
            cols = row.find_all('td')
            if len(cols) > 3:  # Ensure we have enough columns to avoid errors
                stock_info = {
                    'number': cols[0].text.strip(),
                    'name': cols[1].text.strip(),
                    'price': cols[2].text.strip(),
                    'market_cap': cols[4].text.strip(),
                    'pe_ratio': cols[3].text.strip()  # Add more fields as necessary
                }
                stocks.append(stock_info)
    else:
        print("Failed to find the stock table on the page.")
    
    return stocks

# Function to send the stock data to Discord
def send_to_discord(stocks):
    if not stocks:
        print("No stocks to send.")
        return

    message = """ @here 
    **__STOCK RECOMMENDATION__**\n\n"""
    for stock in stocks:
        message += f"**{stock['number']}** **__Name:__** **{stock['name']}** **__Price:__** **{stock['price']}** **__Market Cap:__** **{stock['market_cap']}** **__P/E Ratio:__** **{stock['pe_ratio']}** 🔥\n\n"

    data = {
        'content': message
    }

    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Message sent to Discord successfully!")
    else:
        print(f"Failed to send message, status code: {response.status_code}")

# Fetch the stock data and send it to Discord immediately
stocks = fetch_stocks()
if stocks:
    send_to_discord(stocks)




# import requests
# from bs4 import BeautifulSoup
# import json
# import os
# import time
# import schedule

# # Screener URL for your filtered stocks
# filtered_stocks_url = 'https://www.screener.in/screens/2033673/a/'  # Replace with your actual screen URL

# # Discord Webhook URL
# webhook_url = 'https://discord.com/api/webhooks/1284440879813234758/UIsn5HMs5fPbmuJYa48RsRcUMPVYAwzjk7Wkf9qXINoYMvbk49gaCWUU-TPIAF305rbg'  # Replace with your actual webhook

# # File to store previous stock data
# DATA_FILE = 'previous_stocks.json'

# # Function to fetch stock data from Screener
# def fetch_stocks():
#     response = requests.get(filtered_stocks_url)
#     if response.status_code != 200:
#         print(f"Failed to fetch the page, status code: {response.status_code}")
#         return None

#     soup = BeautifulSoup(response.content, 'html.parser')
#     stock_table = soup.find('table')  # Modify this depending on Screener's page structure

#     stocks = []
#     # Assuming that the first row is the header, so we skip it and start from the second row
#     if stock_table:
#         for row in stock_table.find_all('tr')[1:]:
#             cols = row.find_all('td')
#             if len(cols) > 3:  # Ensure we have enough columns to avoid errors
#                 stock_info = {
#                     'name': cols[0].text.strip(),
#                     'price': cols[1].text.strip(),
#                     'market_cap': cols[2].text.strip(),
#                     'pe_ratio': cols[3].text.strip()  # Add more fields as necessary
#                 }
#                 stocks.append(stock_info)
#     else:
#         print("Failed to find the stock table on the page.")
    
#     return stocks

# # Function to check if stocks have changed
# def check_for_changes():
#     # Fetch the current stock data
#     new_stocks = fetch_stocks()

#     if new_stocks is None or len(new_stocks) == 0:
#         print("No stocks found or could not fetch new stock data.")
#         return

#     # Load previous stock data if exists
#     if os.path.exists(DATA_FILE):
#         with open(DATA_FILE, 'r') as file:
#             previous_stocks = json.load(file)
#     else:
#         previous_stocks = []

#     # Compare new stocks with previous stocks
#     if new_stocks != previous_stocks:
#         print("Stocks have changed. Sending updates...")
#         send_to_discord(new_stocks)
#         # Save the new stock data to file
#         with open(DATA_FILE, 'w') as file:
#             json.dump(new_stocks, file)
#     else:
#         print("No changes in stocks.")

# # Function to send the updated stock data to Discord
# def send_to_discord(stocks):
#     message = "@everyone **Updated Stock Recommendations**\n\n"
#     for stock in stocks:
#         message += f"**{stock['name']}**\nPrice: {stock['price']}\nMarket Cap: {stock['market_cap']}\nP/E Ratio: {stock['pe_ratio']}\n\n"

#     data = {
#         'content': message
#     }

#     try:
#         response = requests.post(webhook_url, json=data)
#         if response.status_code == 204:
#             print("Message sent to Discord successfully!")
#         else:
#             print(f"Failed to send message, status code: {response.status_code}")
#     except Exception as e:
#         print(f"Error while sending message to Discord: {e}")

# # Schedule the job to run every hour or any interval you prefer
# schedule.every(1).hour.do(check_for_changes)

# # Run the scheduled tasks
# while True:
#     schedule.run_pending()
#     time.sleep(1)
