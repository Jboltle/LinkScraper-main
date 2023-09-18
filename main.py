import os
import re
import time
import logging
import subprocess
import requests
import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# Configure logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    root = tk.Tk()  # Create the main application window
    root.withdraw()  # Hide the root window
    input_file_path, output_file_path, cleaned_data_file_path = get_input_paths(root)

    # Read and process input data
    entries = read_and_process_input(input_file_path)

    # Initialize web scraping components
    driver = initialize_web_scraping()

    # Scrape and save links
    scrape_and_save_links(driver, entries, output_file_path)

    # Clean data and save
    cleaned_data_str = clean_data(output_file_path)
    save_cleaned_data(cleaned_data_str, cleaned_data_file_path)

    root.destroy()  # Close the GUI window

def get_input_paths(root):
    input_file_path = filedialog.askopenfilename(title="Select Input File")
    if not os.path.isfile(input_file_path):
        messagebox.showerror("Error", "Input file not found.")
        exit()

    output_file_path = filedialog.asksaveasfilename(title="Save Output File")
    cleaned_data_file_path = filedialog.asksaveasfilename(title="Save Cleaned Data File")

    return input_file_path, output_file_path, cleaned_data_file_path

# Configure lo
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    input_file_path, output_file_path, cleaned_data_file_path = get_input_paths()

    # Read and process input data
    entries = read_and_process_input(input_file_path)

    # Initialize web scraping components
    driver = initialize_web_scraping()

    # Scrape and save links
    scrape_and_save_links(driver, entries)

    # Clean data and save
    cleaned_data_str = clean_data(output_file_path)
    save_cleaned_data(cleaned_data_str, cleaned_data_file_path)

def get_input_paths():
    input_file_path = input("Enter the path to the input file: ").strip()
    output_file_path = input("Enter the path to the output file: ").strip()
    cleaned_data_file_path = input("Enter the path to save cleaned data: ").strip()

    if not os.path.isfile(input_file_path):
        raise FileNotFoundError(f"Input file not found: {input_file_path}")

    return input_file_path, output_file_path, cleaned_data_file_path

def read_and_process_input(input_file_path):
    with open(input_file_path, 'r') as input_file:
        data = input_file.read()

    entries = re.findall(r'^(.+?):\s+(https?://\S+)', data, flags=re.MULTILINE)
    return entries

def initialize_web_scraping():
    profile_path = input("Enter the path to the browser profile directory: ").strip()
    brave_path = input("Enter the path to the browser executable file: ").strip()
    driver_path = input("Enter the path to the Chrome driver executable: ").strip()



    chrome_options = Options()
    chrome_options.binary_location = brave_path
    chrome_options.add_argument('--user-data-dir=' + profile_path)

    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)
def check_and_update_chromedriver():
    latest_version = get_latest_chromedriver_version()
    if latest_version:
        installed_version = get_installed_chromedriver_version()
        if latest_version != installed_version:
            print(f"Updating ChromeDriver from version {installed_version} to {latest_version}...")
            update_chromedriver(latest_version)
        else:
            print(f"ChromeDriver is up to date (version {installed_version}).")

def get_latest_chromedriver_version():
    try:
        response = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE')
        if response.status_code == 200:
            return response.text.strip()
        else:
            print(f"Failed to fetch the latest ChromeDriver version. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error while fetching ChromeDriver version: {str(e)}")
    return None

def get_installed_chromedriver_version():
    # Replace with the actual path to your installed ChromeDriver executable
    chromedriver_path = input("Enter the path to the Chrome driver executable: ").strip()
    try:
        process = subprocess.Popen([chromedriver_path, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = process.communicate()
        installed_version = re.search(r'ChromeDriver (\d+\.\d+\.\d+)', output.decode('utf-8'))
        if installed_version:
            return installed_version.group(1)
    except Exception as e:
        print(f"Error while getting installed ChromeDriver version: {str(e)}")
    return None

def update_chromedriver(version):
    # Replace with the actual path where you want to save the new ChromeDriver executable
    chromedriver_path = input("Enter the path to the Chrome driver executable: ").strip()
    chromedriver_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip"  # Replace with your platform
    try:
        response = requests.get(chromedriver_url)
        if response.status_code == 200:
            with open(chromedriver_path, 'wb') as file:
                file.write(response.content)
                print(f"ChromeDriver {version} downloaded and saved to {chromedriver_path}")
        else:
            print(f"Failed to download ChromeDriver. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error while downloading ChromeDriver: {str(e)}")

def scrape_and_save_links(driver, entries):
    output_file_path = input("Enter the path to the output file: ").strip()
    desktop_path = os.path.expanduser("~/Desktop")

    try:
        with open(output_file_path, 'a') as mega_file:
            for name, url in entries:
                try:
                    # Scrape the mega.nz links from the webpage
                    links = scrape_links(driver, url)

                    # Print the links to check if the scraping process is working
                    logger.info(f"{name}")
                    for link in links:
                        logger.info(link)

                    # Write the links to the output file
                    for link in links:
                        mega_file.write(f"{name}: {link}\n")

                    # Wait for 3 seconds before scraping the next webpage
                    time.sleep(3)
                except Exception as e:
                    logger.error(f"An error occurred while scraping {url}: {e}")

        logger.info(f"Links have been written to {output_file_path}")
    except Exception as e:
        logger.error(f"An error occurred while opening or writing to {output_file_path}: {e}")

def scrape_links(driver, url):
    # Navigate to the webpage
    driver.get(url)

    # Wait for 3 seconds before scraping the webpage content
    time.sleep(3)

    # Parse the webpage content using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the elements that contain the information you want to scrape
    # For example, to scrape all the links on the webpage that contain "mega.nz":
    links = soup.find_all('a', href=lambda href: href and 'mega.nz' in href)

    # Extract the href attributes from the links and return them as a list
    return [link.get('href') for link in links]

def clean_data(output_file_path):
    with open(output_file_path, "r") as f:
        output_data = f.read()

    cleaned_data_str = ""
    for line in output_data.strip().split('\n'):
        name, link = line.strip().split(': ')
        name = name.strip().title()
        link = link.strip()
        cleaned_data_str += f"{name}: {link}\n"

    return cleaned_data_str

def save_cleaned_data(cleaned_data_str, cleaned_data_file_path):
    with open(cleaned_data_file_path, 'w') as f:
        f.write(cleaned_data_str)

if __name__ == "__main__":
    main()
