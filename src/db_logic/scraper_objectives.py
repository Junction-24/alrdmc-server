from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def fetch_objective_from_url(url: str):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="130").install()), options=options)
    driver.get(url)
    driver.implicitly_wait(10)
    
    try:
        # Find the div containing the objectives
        objective_div = driver.find_element(By.ID, "initiativeDetails")
        
        # Extract the objective text
        objective_text = objective_div.text.strip()
        
        if objective_text:
            return objective_text
        else:
            print("Objective text not found")
            return " "
    except Exception as e:
        print(f"Error extracting objective: {e}")
        return " "
    finally:
        # Close the browser window
        driver.quit()

# Example of how to use the function:
# url = "https://eci.ec.europa.eu/035/public/?lg=en"
url = "https://eci.ec.europa.eu/047/public/?lg=en"
objective_text = fetch_objective_from_url(url)

if objective_text:
    print("Objective Text Extracted:")
    print(objective_text)
else:
    print("No objective text available.")
