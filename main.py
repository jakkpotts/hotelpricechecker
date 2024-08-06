import datetime
import random
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth

if __name__ == "__main__":

    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--remote-debugging-port=9222')
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')

    # Initialize the Chrome driver
    driver = uc.Chrome(
        headless=False,
        use_subprocess=True,
        options=chrome_options
    )

    # Apply stealth settings
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    # Generate dates for the URL
    today = datetime.datetime.today()
    two_days_later = today + datetime.timedelta(days=2)
    today_str = today.strftime("%m/%d/%Y")
    two_days_later_str = two_days_later.strftime("%m/%d/%Y")

    # Construct the URL with the dates
    url_template = "https://www.caesars.com/book/hotel-list?arrivalDate=__TODAY__&departureDate=__TWODAYSLATER__&dateSearchFormat=exact-dates&propCode=lvm"
    search_url = url_template.replace("__TODAY__", today_str).replace("__TWODAYSLATER__", two_days_later_str)
    print(search_url)

    # Navigate to the search URL
    driver.get(search_url)

    # Introduce random delay
    time.sleep(random.uniform(1, 6))
    # print(driver.page_source)

    # Get the page source after ensuring the JavaScript content has loaded
    html_string = driver.page_source

    # Print part of the page source for debugging
    # print("Page source:\n", html_string[:1000])  # Adjusted to show the beginning of the HTML

    # Parse the HTML
    soup = BeautifulSoup(html_string, 'html.parser')

    # Find all article elements
    articles = soup.find_all('article')

    # Iterate through articles and find h1 and h4 elements within each
    for article in articles:
        h1 = article.find('h1')
        h4 = article.find('h4')
        if h1 and h4:
            print(f"{h4.text.strip()} -- {h1.text.strip()}")

    driver.quit()
