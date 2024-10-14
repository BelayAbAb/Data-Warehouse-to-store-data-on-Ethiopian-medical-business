import logging
from telethon import TelegramClient
import csv
import os
import json

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

# Function to save last processed message IDs
def save_last_processed_ids(channel_username, last_ids):
    with open(f"{channel_username}_last_ids.json", 'w') as f:
        json.dump({'last_ids': last_ids}, f)
        logging.info(f"Saved last processed IDs for {channel_username}: {last_ids}.")

# Function to scrape all messages from a channel
async def scrape_channel(client, channel_username, writer, media_dir, collect_images=True):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title
        
        # Load the last processed message IDs
        last_ids = get_last_processed_ids(channel_username)
        
        message_count = 0
        processed_ids = []

        # Start retrieving messages
        async for message in client.iter_messages(entity):
            if message.id in last_ids:
                continue
            
            media_path = None
            if message.media and collect_images:
                filename = f"{channel_username}_{message.id}"
                if hasattr(message.media, 'document'):
                    mime_type = message.media.document.mime_type.split('/')[-1]
                    filename += f".{mime_type}"
                else:
                    filename += ".jpg"  # Default to jpg for images without document
                media_path = os.path.join(media_dir, filename)
                await client.download_media(message.media, media_path)
                logging.info(f"Downloaded media for message ID {message.id}.")
            
            # Write message data to CSV
            writer.writerow([
                channel_title,
                channel_username,
                message.id,
                message.message or '',  # Ensure message is not null
                message.date,
                media_path or ''  # Ensure media path is not null
            ])
            logging.info(f"Processed message ID {message.id} from {channel_username}.")
            
            processed_ids.append(message.id)
            message_count += 1

        save_last_processed_ids(channel_username, last_ids + processed_ids)

        if message_count == 0:
            logging.info(f"No new messages found for {channel_username}.")

    except Exception as e:
        logging.error(f"Error while scraping {channel_username}: {e}")

# Function to get last processed message IDs
def get_last_processed_ids(channel_username):
    try:
        with open(f"{channel_username}_last_ids.json", 'r') as f:
            return json.load(f).get('last_ids', [])
    except FileNotFoundError:
        logging.warning(f"No last IDs file found for {channel_username}. Starting from an empty list.")
        return []

# Initialize the client once with a session file
client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    try:
        await client.start(phone)
        logging.info("Client started successfully.")
        
        media_dir = 'photos'
        os.makedirs(media_dir, exist_ok=True)

        # Store scraped data in a CSV file
        with open('scraped_data.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the header only if the file is empty
            if os.stat('scraped_data.csv').st_size == 0:
                writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])
            
            # Define channels to scrape
            channels = [
                'DoctorsET',
                'Chemed Telegram Channel',
                'lobelia4cosmetics',
                'yetenaweg',
                'EAHCI',
                # Add any additional channels you find on et.tgstat.com/medicine here
            ]
            
            for channel in channels:
                await scrape_channel(client, channel, writer, media_dir, collect_images=True)
                logging.info(f"Scraped data from {channel}.")

    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
