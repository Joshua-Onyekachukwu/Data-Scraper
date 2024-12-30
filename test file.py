import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import threading
import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

# Set up logging
logging.basicConfig(filename="scraper.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Function to get random User-Agent
def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/59.0",
        # Add more user agents here
    ]
    return random.choice(user_agents)


# Function to scrape a page using requests (for static pages)
def scrape_page(url):
    try:
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            logging.info(f"Successfully scraped: {url}")
            return response.text
        else:
            logging.error(f"Failed to scrape {url}: Status Code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping {url}: {e}")
        return None


# Function to scrape a page using Selenium (for dynamic content)
def scrape_with_selenium(url):
    try:
        options = Options()
        options.headless = True  # Runs the browser in the background
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(2)  # Wait for the page to load
        page_source = driver.page_source
        driver.quit()  # Close the browser once done
        logging.info(f"Successfully scraped with Selenium: {url}")
        return page_source
    except Exception as e:
        logging.error(f"Error with Selenium scraping for {url}: {e}")
        return None


# Function to search for keywords in the scraped content
def search_keywords(content, keywords):
    keyword_results = {}
    for keyword in keywords:
        keyword_results[keyword] = content.lower().count(keyword.lower())
    return keyword_results


# Function to scrape and search for keywords across multiple pages
def scrape_and_search():
    url_list = entry_urls.get().split(',')
    keywords = entry_keywords.get().split(',')
    total_pages = len(url_list)
    progress['maximum'] = total_pages
    progress['value'] = 0
    result_text.set('Scraping in progress...')

    results = []

    for url in url_list:
        progress['value'] += 1
        window.update_idletasks()

        content = scrape_page(url)  # Use requests or Selenium based on page type
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            page_text = soup.get_text()  # Get all the text on the page
            keyword_results = search_keywords(page_text, keywords)
            results.append({'url': url, 'keywords': keyword_results})

        # Random sleep interval to avoid detection
        time.sleep(random.uniform(1, 3))

    progress['value'] = total_pages
    window.update_idletasks()

    # Display the result
    result_str = '\n'.join(
        [f"URL: {res['url']}\n" + '\n'.join([f"{key}: {value}" for key, value in res['keywords'].items()]) for res in
         results])
    result_text.set(result_str if result_str else "No results found.")

    logging.info("Scraping completed.")
    save_button.config(state="normal")


# Function to save the results to a file
def save_results():
    results = result_text.get()
    with open("scraping_results.txt", "w") as file:
        file.write(results)
    messagebox.showinfo("Save Results", "Results have been saved to 'scraping_results.txt'")


# Function to handle the multi-threaded scraping
def start_scraping_thread():
    threading.Thread(target=scrape_and_search).start()


# Set up the GUI window
window = tk.Tk()
window.title("Web Scraper with Keyword Search")
window.geometry("600x500")

# Label for URL input
label_urls = tk.Label(window, text="Enter URLs (separate by commas):")
label_urls.grid(row=0, column=0, padx=10, pady=5)

# Entry for URLs
entry_urls = tk.Entry(window, width=50)
entry_urls.grid(row=0, column=1, padx=10, pady=5)

# Label for keywords input
label_keywords = tk.Label(window, text="Enter Keywords (separate by commas):")
label_keywords.grid(row=1, column=0, padx=10, pady=5)

# Entry for keywords
entry_keywords = tk.Entry(window, width=50)
entry_keywords.grid(row=1, column=1, padx=10, pady=5)

# Button to start scraping
button_scrape = tk.Button(window, text="Start Scraping", command=start_scraping_thread)
button_scrape.grid(row=2, column=0, columnspan=2, pady=20)

# Progress bar
progress = ttk.Progressbar(window, orient="horizontal", length=400, mode="indeterminate")
progress.grid(row=3, column=0, columnspan=2, pady=10)

# Label to show the result
result_text = tk.StringVar()
label_result = tk.Label(window, textvariable=result_text, wraplength=550)
label_result.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

# Button to save the results to a file
save_button = tk.Button(window, text="Save Results to Txt", state="disabled", command=save_results)
save_button.grid(row=5, column=0, columnspan=2, pady=20)

# Start the GUI event loop
window.mainloop()
