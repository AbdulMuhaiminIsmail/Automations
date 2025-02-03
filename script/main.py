from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc

from google_sheets import update_sheet
from random_helpers import random_delay, random_scroll

import random
import time

# Function to check rank of a website wrt array of keywords
def check_ranking(keywords, target_url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox") # Bypass OS security model
    chrome_options.add_argument("--lang=en-US") # Set language to English
    chrome_options.add_argument("--disable-gpu") # Disable GPU acceleration
    chrome_options.add_argument("--start-maximized") # Start window maximized
    chrome_options.add_argument("--disable-dev-shm-usage") # Disable /dev/shm usage
    chrome_options.add_argument("--disable-infobars")  # Disable infobars
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--disable-popup-blocking")  # Disable popups
    chrome_options.add_argument("--disable-notifications")  # Disable notifications
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") # Disable automation control
    chrome_options.add_argument(r"--user-data-dir=C:\Users\ZEUS\AppData\Local\Google\Chrome\User Data\Default") # Set user data directory

    # Rotate user agents to avoid detection
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    ]
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

    # Initialize the WebDriver with stealth options
    driver = uc.Chrome(service=Service(), options=chrome_options, keep_alive=True)

    rankings = []

    with open("results.txt", "a") as f:
        f.write("----------------------------------------------------------------------------------------------------------------------------------------------\n")
        f.write("                                                Link: " + target_url + "\n")
    f.close()

    for keyword in keywords:
        try:
            search_query = keyword.replace(" ", "+")
            print("Navigating to google search page with US proxy")
            driver.get(f"https://www.google.com/search?q={search_query}&hl=en&gl=US&ie=utf-8&oe=utf-8&pws=0&uule=a+cm9sZToxCnByb2R1Y2VyOjEyCnByb3ZlbmFuY2U6Ngp0aW1lc3RhbXA6MTczODM0MTQ5NzU4NjAwMApsYXRsbmd7CmxhdGl0dWRlX2U3OjM3MDkwMjQwMApsb25naXR1ZGVfZTc6LTk1NzEyODkxMAp9CnJhZGl1czo5MzAwMA%3D%3D&num=100")
            print("Page loaded successfully.")

            # Wait for the results to load
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "g"))
                )
                print("Search results successfully loaded.")
            except TimeoutException:
                print("Error: Search results did not load in time.")

            random_delay(1, 2)
            random_scroll(driver, scroll_times=5)
            
            # Get all search result links
            links = []

            results = driver.find_elements(By.CLASS_NAME, "g")
     
            for result in results:
                try:
                    link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                    links.append(link)
                except NoSuchElementException:
                    continue

            random_delay(1, 3)
            random_scroll(driver, scroll_times=2)

            # Search for ranking in top 100 results
            rank = 1
            for link in links:
                if target_url in link:
                    with open("results.txt", "a") as f:
                        f.write("                                                    - Keyword: " + keyword + " (#" + str(rank) + ")\n")
                    f.close()
                    break
                rank += 1
            
            # Handle the case when target_url is not found in top 100 results
            if (rank > 100):
                with open("results.txt", "a") as f:
                    f.write("                                                    - Keyword: " + keyword + " (#" + str(rank) + ")\n")
                f.close()
        
        except Exception as e:
            print(f"An error occurred: {e}")
            rank = -1

        finally:
            rankings.append(rank)
            random_delay(3, 5)
            continue
    
    with open("results.txt", "a") as f:
        f.write("----------------------------------------------------------------------------------------------------------------------------------------------\n")
    f.close()
    print("Results saved in results.txt file.")

    driver.quit()
    return rankings
        
#----------------------------------------------------------------------

def main():
    # Keywords to check rankings for
    keywords = [
        "tire machine parts",
        "tire accessories",
        "tire machine accessories",
        "tire changer accessories",
        "tire machine parts & accessories",
        "auto lift accessories",
        "automotive lift accessories",
        "vehicle lift accessories",
        "Wheel Balancer Accessories",
        "wheel balancer parts",
        "wheel balancing machine accessories"
    ]

    # Target URL to check rankings for
    target_url="https://coatscompany.com"

    # Start timer
    start_time = time.time()

    # Get the rankings for the keywords
    rankings = check_ranking(keywords, target_url)

    # Update Google Sheet with the rankings
    update_sheet("Automated Ranking", rankings, "E2")

    # End timer
    end_time = time.time()

    print(f"Rankings checked and updated in Google Sheet in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()

    