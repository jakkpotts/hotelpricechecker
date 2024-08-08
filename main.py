import datetime
import random
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from bs4 import BeautifulSoup

# Chrome options
chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--remote-debugging-port=9222')
chrome_options.add_argument('--headless')  # Enable headless mode
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

# Initialize the Chrome driver
driver = uc.Chrome(
    headless=True,
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
# standard today as the arrival date and two days later as the departure date
today = datetime.datetime.today()
two_days_later = today + datetime.timedelta(days=2)
today_str = today.strftime("%m/%d/%Y")
two_days_later_str = two_days_later.strftime("%m/%d/%Y")

# Construct the URL with the dates
url_template = "https://www.caesars.com/book/hotel-list?arrivalDate=__TODAY__&departureDate=__TWODAYSLATER__&dateSearchFormat=exact-dates&propCode=lvm"
search_url = url_template.replace("__TODAY__", today_str).replace("__TWODAYSLATER__", two_days_later_str)

# Debug
print(search_url)

# Navigate to the search URL
driver.get(search_url)

# Introduce random delay for bot detection avoidance
# and to ensure the JavaScript content has loaded
time.sleep(random.uniform(1, 6))

html_string = driver.page_source

# Print page source for debugging
# print("Page source:\n", html_string)  # Adjusted to show the beginning of the HTML

# Parse the HTML, sleep
time.sleep(random.uniform(1, 3))
soup = BeautifulSoup(html_string, 'html.parser')

# Find all article elements
articles = soup.find_all('article')

# Debug
# print(f"Found {len(articles)} articles")

# Iterate through articles and find h1 and h4 elements within each
# Also store the results in a list of dictionaries
hotels = []
for article in articles:
    h1 = article.find('h1')
    h4 = article.find('h4')
    if h1 and h4:
        # Debug
        # print(f"{h4.text.strip()} -- {h1.text.strip()}")
        hotels.append({"hotel_name": h4.text.strip(), "room_price": h1.text.strip()})
    else:
        # Debug
        # print("h1 or h4 not found in article")
        pass
for hotel in hotels:
    print(hotel["hotel_name"], hotel["room_price"], sep=" -- ")

driver.quit()
