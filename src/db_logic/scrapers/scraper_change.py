import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

urls = [
    "https://www.change.org/t/abortion-access-en-us?source_location=homepage",
#    "https://www.change.org/t/health-and-well-being-en-us?source_location=topic_page",
#    "https://www.change.org/t/public-health-en-us?source_location=topic_page",
#    "https://www.change.org/t/government-and-politics-en-us?source_location=topic_page",
#    "https://www.change.org/t/public-safety-2?source_location=topic_page",
#    "https://www.change.org/t/criminal-justice-en-US?source_location=topic_page",
#    "https://www.change.org/t/student-issues-en-us?source_location=topic_page",
#    "https://www.change.org/t/free-speech-en-us?source_location=homepage",
#    "https://www.change.org/t/entertainment-media-en-us?source_location=topic_page",
#    "https://www.change.org/t/technology-9?source_location=topic_page",
#    "https://www.change.org/t/video-games-online-gaming-en-us?source_location=topic_page",
#    "https://www.change.org/t/consumer-rights-en-us?source_location=topic_page",
#    "https://www.change.org/t/environmental-issues-en-us?source_location=topic_page",
#    "https://www.change.org/t/animal-rights-and-conservation-en-us?source_location=topic_page",
#    "https://www.change.org/t/business-and-economy-en-us?source_location=topic_page"
]

def fetch_initiative_change(url: str):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=options)) as driver:
        driver.get(url)
        driver.implicitly_wait(10)
        
        initiatives = []

        try:
            # Get all elements with the specified class
            objective_divs = driver.find_elements(By.CLASS_NAME, "corgi-1vlmmoi")

            for div in objective_divs:
                title = div.text.strip()

                # Find the closest parent or sibling anchor tag
                parent = div.find_element(By.XPATH, "./ancestor::a")
                url = parent.get_attribute("href") if parent else None

                # Only add entries with a valid URL and text
                if title and url:
                    initiatives.append({
                        "title": title,
                        "url": url
                    })
            return initiatives
        except Exception as e:
            print(f"Error extracting initiatives: {e}")
            return []




def fetch_descriptions_for_initiatives(initiatives: dict):
    """
    Fetch descriptions for each initiative in the dictionary and update it.
    """
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)

    try:
        for initiative in initiatives.values():
            driver.get(initiative["url"])
            time.sleep(1)  # Ensure the page fully loads

            try:
                description_element = driver.find_element(By.CLASS_NAME, "e19irtt30.corgi-1qn3huw")
                description_text = description_element.text.strip()
                initiative["description"] = description_text
            except Exception as e:
                print(f"Error fetching description from {initiative['url']}: {e}")
                initiative["description"] = "No description found"

    finally:
        driver.quit()


res = []

for url in urls:
    res += fetch_initiative_change(url)


unique_initiatives = {initiative['url']: initiative for initiative in res}
fetch_descriptions_for_initiatives(unique_initiatives)

res = list(unique_initiatives.values())

for initiative in res:
    print(initiative)
print(f"Total unique initiatives found: {len(res)}")