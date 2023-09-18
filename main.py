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
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("File Paths Input")
        
        self.input_file_label = tk.Label(root, text="Input File:")
        self.input_file_label.pack()
        self.input_file_path_var = tk.StringVar()
        self.input_file_path = tk.Entry(root, textvariable=self.input_file_path_var)
        self.input_file_path.pack()
        self.browse_input_button = tk.Button(root, text="Browse", command=self.browse_input)
        self.browse_input_button.pack()
        
        self.output_file_label = tk.Label(root, text="Output File:")
        self.output_file_label.pack()
        self.output_file_path_var = tk.StringVar()
        self.output_file_path = tk.Entry(root, textvariable=self.output_file_path_var)
        self.output_file_path.pack()
        self.browse_output_button = tk.Button(root, text="Browse", command=self.browse_output)
        self.browse_output_button.pack()
        
        self.cleaned_data_label = tk.Label(root, text="Cleaned Data File:")
        self.cleaned_data_label.pack()
        self.cleaned_data_path_var = tk.StringVar()
        self.cleaned_data_path = tk.Entry(root, textvariable=self.cleaned_data_path_var)
        self.cleaned_data_path.pack()
        self.browse_cleaned_data_button = tk.Button(root, text="Browse", command=self.browse_cleaned_data)
        self.browse_cleaned_data_button.pack()

        self.brave_profile_label = tk.Label(root, text="Brave Profile Directory:")
        self.brave_profile_label.pack()
        self.brave_profile_path_var = tk.StringVar()
        self.brave_profile_path = tk.Entry(root, textvariable=self.brave_profile_path_var)
        self.brave_profile_path.pack()
        self.browse_brave_profile_button = tk.Button(root, text="Browse", command=self.browse_brave_profile)
        self.browse_brave_profile_button.pack()

        self.brave_executable_label = tk.Label(root, text="Brave Executable File:")
        self.brave_executable_label.pack()
        self.brave_executable_path_var = tk.StringVar()
        self.brave_executable_path = tk.Entry(root, textvariable=self.brave_executable_path_var)
        self.brave_executable_path.pack()
        self.browse_brave_executable_button = tk.Button(root, text="Browse", command=self.browse_brave_executable)
        self.browse_brave_executable_button.pack()

        self.chrome_driver_label = tk.Label(root, text="Chrome Driver Executable:")
        self.chrome_driver_label.pack()
        self.chrome_driver_path_var = tk.StringVar()
        self.chrome_driver_path = tk.Entry(root, textvariable=self.chrome_driver_path_var)
        self.chrome_driver_path.pack()
        self.browse_chrome_driver_button = tk.Button(root, text="Browse", command=self.browse_chrome_driver)
        self.browse_chrome_driver_button.pack()

        self.submit_button = tk.Button(root, text="Submit", command=self.process_input)
        self.submit_button.pack()

        # Load the previously entered values
        self.load_saved_values()
    
    def browse_input(self):
        input_path = filedialog.askopenfilename(title="Select Input File")
        self.input_file_path_var.set(input_path)
    
    def browse_output(self):
        output_path = filedialog.asksaveasfilename(title="Save Output File")
        self.output_file_path_var.set(output_path)
    
    def browse_cleaned_data(self):
        cleaned_data_path = filedialog.asksaveasfilename(title="Save Cleaned Data File")
        self.cleaned_data_path_var.set(cleaned_data_path)
    
    def browse_brave_profile(self):
        brave_profile_path = filedialog.askdirectory(title="Select Brave Profile Directory")
        self.brave_profile_path_var.set(brave_profile_path)
    
    def browse_brave_executable(self):
        brave_executable_path = filedialog.askopenfilename(title="Select Brave Executable File")
        self.brave_executable_path_var.set(brave_executable_path)
    
    def browse_chrome_driver(self):
        chrome_driver_path = filedialog.askopenfilename(title="Select Chrome Driver Executable")
        self.chrome_driver_path_var.set(chrome_driver_path)
    
    def process_input(self):
        input_file_path = self.input_file_path_var.get()
        output_file_path = self.output_file_path_var.get()
        cleaned_data_file_path = self.cleaned_data_path_var.get()
        brave_profile_path = self.brave_profile_path_var.get()
        brave_executable_path = self.brave_executable_path_var.get()
        chrome_driver_path = self.chrome_driver_path_var.get()

        # Save the entered values for future use
        self.save_values(input_file_path, output_file_path, cleaned_data_file_path, brave_profile_path, brave_executable_path, chrome_driver_path)

        # Rest of your processing code here
        entries = self.read_and_process_input(input_file_path)

        # Initialize web scraping components based on the input from the GUI
        driver = self.initialize_web_scraping(brave_profile_path, brave_executable_path, chrome_driver_path)

        # Scrape and save links
        self.scrape_and_save_links(driver, entries, output_file_path)

    def load_saved_values(self):
        try:
            with open("saved_values.txt", "r") as file:
                lines = file.readlines()
                if len(lines) >= 6:
                    (input_path, output_path, cleaned_data_path, brave_profile_path, brave_executable_path, chrome_driver_path) = lines[:6]
                    self.input_file_path_var.set(input_path.strip())
                    self.output_file_path_var.set(output_path.strip())
                    self.cleaned_data_path_var.set(cleaned_data_path.strip())
                    self.brave_profile_path_var.set(brave_profile_path.strip())
                    self.brave_executable_path_var.set(brave_executable_path.strip())
                    self.chrome_driver_path_var.set(chrome_driver_path.strip())
        except FileNotFoundError:
            pass
    
    def save_values(self, input_path, output_path, cleaned_data_path, brave_profile_path, brave_executable_path, chrome_driver_path):
        with open("saved_values.txt", "w") as file:
            file.write(f"{input_path}\n")
            file.write(f"{output_path}\n")
            file.write(f"{cleaned_data_path}\n")
            file.write(f"{brave_profile_path}\n")
            file.write(f"{brave_executable_path}\n")
            file.write(f"{chrome_driver_path}\n")
        # Read and process input data
        entries = self.read_and_process_input(input_path)

        # Initialize web scraping components based on the input from the GUI
        driver = self.initialize_web_scraping(brave_profile_path, brave_executable_path, chrome_driver_path)

        # Scrape and save links
        self.scrape_and_save_links(driver, entries, output_path)

    def read_and_process_input(self, input_file_path):
        with open(input_file_path, 'r') as input_file:
            data = input_file.read()

        entries = re.findall(r'^(.+?):\s+(https?://\S+)', data, flags=re.MULTILINE)
        return entries

    def initialize_web_scraping(self, profile_path, brave_path, driver_path):
        chrome_options = Options()
        chrome_options.binary_location = brave_path
        chrome_options.add_argument('--user-data-dir=' + profile_path)

        service = Service(driver_path)
        return webdriver.Chrome(service=service, options=chrome_options)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
