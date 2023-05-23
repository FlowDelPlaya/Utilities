import os
import time
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def download_images(url, output_folder, width, height):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.find_all('a', class_='fileThumb')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    downloaded_count = 0
    skipped_count = 0

    for img in images:
        img_url = 'https:' + img['href']
        img_response = requests.get(img_url)
        img_data = BytesIO(img_response.content)

        if img_url.lower().endswith('.webm'):
            print(f"Skipped {img_url} due to unsupported format")
            skipped_count += 1
            continue

        try:
            with Image.open(img_data) as image:
                if image.size == (width, height):
                    file_name = os.path.join(output_folder, img_url.split('/')[-1])
                    with open(file_name, 'wb') as f:
                        f.write(img_response.content)
                    print(f"Downloaded {img_url}")
                    downloaded_count += 1
                else:
                    print(f"Skipped {img_url} due to size mismatch")
                    skipped_count += 1
        except Exception as e:
            print(f"Error processing {img_url}: {e}")
        time.sleep(1)

    return downloaded_count, skipped_count

if __name__ == '__main__':
    board = 'wg'
    output_folder = os.path.join(os.getcwd(), 'my_images')

    width, height = 2560, 1440

    total_downloaded_count = 0
    total_skipped_count = 0

    # For the first page, the url should be https://boards.4chan.org/{board}/
    url = f'https://boards.4chan.org/{board}/'
    print(f"Scraping page {url}")
    downloaded_count, skipped_count = download_images(url, output_folder, width, height)
    total_downloaded_count += downloaded_count
    total_skipped_count += skipped_count
    print(f"Downloaded {downloaded_count} images, skipped {skipped_count} images from page {url}")

    # For pages from 2 onwards, the url should be https://boards.4chan.org/{board}/{page}
    page = 2
    while True:
        url = f'https://boards.4chan.org/{board}/{page}'
        print(f"Scraping page {url}")
        downloaded_count, skipped_count = download_images(url, output_folder, width, height)
        total_downloaded_count += downloaded_count
        total_skipped_count += skipped_count
        print(f"Downloaded {downloaded_count} images, skipped {skipped_count} images from page {url}")

        # Stop when no images were downloaded or skipped on the current page
        if downloaded_count == 0 and skipped_count == 0:
            break

        page += 1
        time.sleep(1)

    print(f"Finished scraping. Downloaded a total of {total_downloaded_count} images, skipped {total_skipped_count} images.")

