import time
import random

# Function to add random delays
def random_delay(min_seconds=1, max_seconds=3):
    time.sleep(random.uniform(min_seconds, max_seconds))

# Random scrolling function
def random_scroll(driver, min_scroll=100, max_scroll=400, scroll_times=10, min_wait=0.5, max_wait=2):
    for _ in range(scroll_times):
        scroll_amount = random.randint(min_scroll, max_scroll)  # Random scroll pixels
        scroll_direction = random.choice([-1, 1])  # Up (-1) or Down (1)
        
        driver.execute_script(f"window.scrollBy(0, {scroll_amount * scroll_direction});")
        
        wait_time = random.uniform(min_wait, max_wait)  # Random wait time
        time.sleep(wait_time)