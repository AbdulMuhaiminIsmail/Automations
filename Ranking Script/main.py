import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc

def random_delay(min_seconds=7, max_seconds=12):
    """Sleep for a random time between min_seconds and max_seconds."""
    time.sleep(random.uniform(min_seconds, max_seconds))

def random_scroll(driver, min_scroll=100, max_scroll=400, scroll_times=1, min_wait=1, max_wait=2):
    """
    Perform a small random scroll pass to appear more human,
    but not so much that it looks robotic.
    """
    for _ in range(scroll_times):
        scroll_amount = random.randint(min_scroll, max_scroll)
        scroll_direction = random.choice([-1, 1])  
        driver.execute_script(f"window.scrollBy(0, {scroll_amount * scroll_direction});")
        time.sleep(random.uniform(min_wait, max_wait))
#----------------------------------------------------------------------------------

# Function to check rank of a website wrt array of keywords
def check_ranking(keywords, target_url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--lang=en-US")  # Set language to English
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--start-maximized")  # Start window maximized
    chrome_options.add_argument("--disable-dev-shm-usage")  # Disable /dev/shm usage
    chrome_options.add_argument("--disable-infobars")  # Disable infobars
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--disable-popup-blocking")  # Disable popups
    chrome_options.add_argument("--disable-notifications")  # Disable notifications
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation control
    # chrome_options.add_argument(r"--user-data-dir=C:\Users\ZEUS\AppData\Local\Google\Chrome\User Data\Default")  # STILL COMMENTED OUT

    # Rotate user agents to avoid detection
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    ]
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

    # Initialize the WebDriver with stealth options
    driver = uc.Chrome(service=Service(), options=chrome_options, keep_alive=True)

    # Logging to results.txt
    with open("results.txt", "a") as f:
        f.write("----------------------------------------------------------------------------------------------------------------------------------------------\n")
        f.write("                                                Link: " + target_url + "\n")

    for keyword in keywords:
        try:
            search_query = keyword.replace(" ", "+")
            google_url = f"https://www.google.com/search?q={search_query}&hl=en&gl=US&num=100"

            print(f"Navigating to: {google_url}")
            driver.get(google_url)
            print("Page loaded successfully.")

            # Wait for the results to load or up to 30 seconds
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "g"))
                )
                print("Search results successfully loaded.")
            except TimeoutException:
                print("Error: Search results did not load in time.")

            # Small random delay and small scroll pass
            random_delay()
            random_scroll(driver, scroll_times=1)

            # Fetch all search results
            results = driver.find_elements(By.CLASS_NAME, "g")

            # Extracting links and matching with target_url
            rank = 0
            for result in results:
                try:
                    link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                    rank += 1

                    if (rank > 100): break  # Stop checking after 100 results

                    if target_url in link:
                        with open("results.txt", "a") as f:
                            f.write(f"                                                    - Keyword: {keyword} (#{rank})\n")
                        with open("results.csv", "a") as f:
                            f.write(f"{keyword}, {rank}\n")
                        break
                except NoSuchElementException:
                    continue

            random_delay()
            random_scroll(driver, scroll_times=1)

            # If not found in top 100
            if rank > 100:
                with open("results.txt", "a") as f:
                    f.write(f"                                                    - Keyword: {keyword} (#{rank})\n")
                with open("results.csv", "a") as f:
                    f.write(f"{keyword}, N/A\n")

        except Exception as e:
            print(f"An error occurred: {e}")
            with open("results.txt", "a") as f:
                f.write(f"                                                    - Keyword: {keyword} (#Error)\n")
            with open("results.csv", "a") as f:
                f.write(f"{keyword}, Error\n")

        finally:
            # Another longer random delay before moving to next keyword
            random_delay()

    with open("results.txt", "a") as f:
        f.write("----------------------------------------------------------------------------------------------------------------------------------------------\n")
    
    print("Results saved in results.txt file.")
    print("Results saved in results.csv file.")

    driver.quit()

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
    target_url = "https://coatscompany.com"

    # Start timer
    start_time = time.time()

    # Get the rankings for the keywords
    check_ranking(keywords, target_url)

    # End timer
    end_time = time.time()
    minutes_elapsed = (end_time - start_time) / 60
    print(f"Rankings checked in {minutes_elapsed:.2f} minutes.")

if __name__ == "__main__":
    main()
