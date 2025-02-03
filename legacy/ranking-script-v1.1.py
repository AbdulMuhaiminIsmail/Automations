from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
import time
import random

# Function to simulate human-like typing
def human_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3)) 

# Function to simulate human-like mouse movements
def human_mouse_move(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element(element).pause(random.uniform(0.5, 1.5)).perform()

# Function to add random delays
def random_delay(min_seconds=1, max_seconds=3):
    time.sleep(random.uniform(min_seconds, max_seconds))

# Function to check rank of a website wrt some keyword
def search_and_check_rank(keyword, region, target_url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-infobars")  # Disable infobars
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--disable-popup-blocking")  # Disable popups
    chrome_options.add_argument("--disable-notifications")  # Disable notifications
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Rotate user agents to avoid detection
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    ]
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

    # Initialize the WebDriver with stealth options
    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    try:
        # Navigate to Valentin.app website
        search_query = keyword.replace(" ", "+")
        print("Navigating to google search page with US proxy and 100 results...")
        driver.get(f"https://www.google.com/search?q={search_query}&hl=en&gl=US&ie=utf-8&oe=utf-8&pws=0&uule=a+cm9sZToxCnByb2R1Y2VyOjEyCnByb3ZlbmFuY2U6Ngp0aW1lc3RhbXA6MTczODM0MTQ5NzU4NjAwMApsYXRsbmd7CmxhdGl0dWRlX2U3OjM3MDkwMjQwMApsb25naXR1ZGVfZTc6LTk1NzEyODkxMAp9CnJhZGl1czo5MzAwMA%3D%3D&num=100")
        print("Page loaded successfully.")

        # # Wait for the search input to load
        # try:
        #     WebDriverWait(driver, 20).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, "#search-input"))
        #     )
        #     print("Valentin search input found.")
        # except TimeoutException:
        #     print("Error: Search input not found. The valentin page may not have loaded correctly.")
        #     return -1

        # # Enter the keyword
        # keyword_input = driver.find_element(By.CSS_SELECTOR, "#search-input")
        # keyword_input.clear()
        # keyword_input.send_keys(keyword)
        # # human_mouse_move(driver, keyword_input)  # Simulate mouse movement
        # # human_type(keyword_input, keyword)  # Simulate human typing
        # # random_delay(1, 2)  # Random delay after typing
        # print(f"Entered keyword: {keyword}")

        # # Enter the region
        # region_input = driver.find_element(By.CSS_SELECTOR, "#regions")
        # region_input.clear()
        # region_input.send_keys(region)
        # # human_mouse_move(driver, region_input)  # Simulate mouse movement
        # # human_type(region_input, region)  # Simulate human typing
        # # random_delay(1, 2)  # Random delay after typing
        # print(f"Entered region: {region}")

        # # Click the search button with human-like behavior
        # search_button = driver.find_element(By.CSS_SELECTOR, "#button-search")
        # # human_mouse_move(driver, search_button)  # Simulate mouse movement
        # # random_delay(1, 2)  # Random delay before clicking
        # search_button.click()
        # print("Clicked search button.")

        # Wait for the results to load
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.TAG_NAME, "cite"))
            )
            print("First page's search results successfully loaded.")
        except TimeoutException:
            print("Error: First page's search results did not load in time.")
            return -1
        
        # Get all search result links
        links = []
        results = driver.find_elements(By.TAG_NAME, "cite")
        for result in results:
            link = result.text
            if link and link.startswith("http"):
                links.append(link)

        # Save links in file
        with open("links.txt", "w") as f:
            for link in links:
                f.write(link + "\n")

        
        # Find all search result links
        rank = 1
        for link in links:
            if target_url in link:
                break
            rank += 1

        return rank
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return -1
    finally:
        driver.quit()
        print("Browser closed.")
        
#----------------------------------------------------------------------

# Example usage
keyword="tire machine parts"
region="United States - English"
target_url="https://coatscompany.com"

rank = search_and_check_rank(
    keyword=keyword,
    region=region,
    target_url=target_url    
)

if rank != -1:
    print(f"{target_url} ranks at #{rank} when {keyword} is searched.")
else:
    print(f"{target_url} does not rank among top 100 results when {keyword} is searched.")