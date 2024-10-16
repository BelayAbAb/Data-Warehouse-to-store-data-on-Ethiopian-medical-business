import logging
from telethon import TelegramClient
import csv
import os
import json
import pandas as pd

# Set up logging
logging.basicConfig(
    filename='scraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Telegram API credentials
api_id = 26737733
api_hash = 'f590cc7e473a4e1c9ea4f7bc59163016'
phone = '+251940250405'

# Function to get last processed message ID
def get_last_processed_id(channel_username):
    try:
        with open(f"{channel_username}_last_id.json", 'r') as f:
            return json.load(f).get('last_id', 0)
    except FileNotFoundError:
        logging.warning(f"No last ID file found for {channel_username}. Starting from 0.")
        return 0

# Function to save last processed message ID
def save_last_processed_id(channel_username, last_id):
    with open(f"{channel_username}_last_id.json", 'w') as f:
        json.dump({'last_id': last_id}, f)
        logging.info(f"Saved last processed ID {last_id} for {channel_username}.")

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, writer, media_dir):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title
        
        last_id = get_last_processed_id(channel_username)
        
        message_count = 0
        async for message in client.iter_messages(entity):
            if message.id <= last_id:
                continue
            
            media_path = None
            if message.media:
                filename = f"{channel_username}_{message.id}"
                if hasattr(message.media, 'document'):
                    mime_type = message.media.document.mime_type.split('/')[-1]
                    filename += f".{mime_type}"
                else:
                    filename += ".jpg"  # Default to jpg for images without document
                media_path = os.path.join(media_dir, filename)
                await client.download_media(message.media, media_path)
                logging.info(f"Downloaded media for message ID {message.id}.")
            
            writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])
            logging.info(f"Processed message ID {message.id} from {channel_username}.")
            
            last_id = message.id
            message_count += 1
            
            # Stop after scraping 20 messages
            if message_count >= 20:
                break

        save_last_processed_id(channel_username, last_id)

        if message_count == 0:
            logging.info(f"No new messages found for {channel_username}.")

    except Exception as e:
        logging.error(f"Error while scraping {channel_username}: {e}")

# Initialize the client once with a session file
client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    try:
        await client.start(phone)
        logging.info("Client started successfully.")
        
        media_dir = 'photos'
        os.makedirs(media_dir, exist_ok=True)

        # Store scraped data in a CSV file
        csv_file = 'scraped_data.csv'
        with open(csv_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])
            
            # Define channels to scrape
            channels = [
                'DoctorsET',
                'Chemed Telegram Channel',
                'lobelia4cosmetics',
                'yetenaweg',
                'EAHCI',
            ]
            
            for channel in channels:
                await scrape_channel(client, channel, writer, media_dir)
                logging.info(f"Scraped data from {channel}.")

        # Clean the scraped data
        clean_data(csv_file)

    except Exception as e:
        logging.error(f"Error in main function: {e}")

def clean_data(csv_file):
    try:
        # Load data into a DataFrame
        df = pd.read_csv(csv_file)

        # Remove duplicates
        df.drop_duplicates(subset=['ID'], keep='first', inplace=True)

        # Handle missing values (example: fill with empty string)
        df.fillna('', inplace=True)

        # Standardize formats (example: converting dates to a standard format)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')

        # Data validation (example: check if 'ID' is numeric)
        if not df['ID'].apply(lambda x: str(x).isnumeric()).all():
            logging.warning("Some IDs are not numeric.")

        # Store cleaned data
        cleaned_csv_file = 'cleaned_data.csv'
        df.to_csv(cleaned_csv_file, index=False)
        logging.info(f"Cleaned data stored in {cleaned_csv_file}.")

    except Exception as e:
        logging.error(f"Error during data cleaning: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
