from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
import time
import urllib.parse
from utils import get_base_domain, find_social_links
from pocketbase import send_to_pocketbase
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BLACKLISTED_DOMAINS = {"google.com", "opentable.com", "treatwell.de"}
BLACKLISTED_KEYWORDS = {"book"}

def setup_driver():
    """Sets up the Chrome WebDriver with options and stealth settings."""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run headless if you don't need a GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Apply Selenium Stealth
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    
    return driver

def scrape_google_maps(search_query):
    """Scrapes Google Maps for business links based on the search query."""
    driver = setup_driver()
    try:
        encoded_query = urllib.parse.quote_plus(search_query)
        url = f"https://www.google.com/maps/search/{encoded_query}"
        logging.info(f"Navigating to URL: {url}")
        driver.get(url)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="feed"]')))
        scrollable_div = driver.find_element(By.CSS_SELECTOR, '[role="feed"]')
        previous_height = driver.execute_script('return arguments[0].scrollHeight', scrollable_div)

        while True:
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
            time.sleep(2)
            new_height = driver.execute_script('return arguments[0].scrollHeight', scrollable_div)
            if new_height == previous_height:
                break
            previous_height = new_height

        business_links = driver.find_elements(By.CSS_SELECTOR, '[role="feed"] > div > div > a')
        links = [link.get_attribute('href') for link in business_links if link.get_attribute('href')]

        for link in links:
            try:
                driver.get(link)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                title = driver.find_element(By.TAG_NAME, 'h1').text.strip()
                if not title:
                    continue

                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                website = next((a['href'] for a in soup.find_all('a', href=True)
                                if not any(domain in a['href'] for domain in BLACKLISTED_DOMAINS)), None)

                if not website or any(keyword in website for keyword in BLACKLISTED_KEYWORDS):
                    continue

                base_domain = get_base_domain(website)
                social_links = find_social_links(base_domain)

                if social_links.get('instagram') or social_links.get('facebook'):
                    send_to_pocketbase(title, base_domain, social_links.get('instagram'), social_links.get('facebook'))
            except Exception as e:
                logging.error(f"Error processing link {link}: {e}")

    except Exception as e:
        logging.error(f"Error processing query {search_query}: {e}")
    finally:
        driver.quit()

def main():
    search_queries = {
        "query1": "nagel studio in baden-württemberg",
        "query2": "nagel studio in bayern",
        "query3": "nagel studio in berlin",
        "query4": "nagel studio in brandenburg",
        "query5": "nagel studio in hessen",
        "query6": "nagel studio in mecklenburg-vorpommern",
        "query7": "nagel studio in niedersachsen",
        "query8": "nagel studio in nordrhein-westfalen",
        "query9": "nagel studio in rheinland-pfalz",
        "query10": "nagel studio in saarland",
        "query11": "nagel studio in sachsen",
        "query12": "nagel studio in sachsen-anhalt",
        "query13": "nagel studio in schleswig-holstein",
        "query14": "nagel studio in thüringen",
        "query15": "nagel studio in bremen",
        "query16": "nagel studio in hamburg",
        "query17": "nagel studio in aalen",
        "query18": "nagel studio in abensberg",
        "query19": "nagel studio in achern",
        "query20": "nagel studio in adelsdorf",
        "query21": "nagel studio in angermünde",
        "query22": "nagel studio in augsburg",
        "query23": "nagel studio in bad belzig",
        "query24": "nagel studio in bad doberan",
        "query25": "nagel studio in bad freienwalde",
        "query26": "nagel studio in bad homburg",
        "query27": "nagel studio in bad nauheim",
        "query28": "nagel studio in bad salzuflen",
        "query29": "nagel studio in bad soden am taunus",
        "query30": "nagel studio in bad wildbad",
        "query31": "nagel studio in bielefeld",
        "query32": "nagel studio in bonn",
        "query33": "nagel studio in braunschweig",
        "query34": "nagel studio in bremerhaven",
        "query35": "nagel studio in chemnitz",
        "query36": "nagel studio in cottbus",
        "query37": "nagel studio in dortmund",
        "query38": "nagel studio in dresden",
        "query39": "nagel studio in düsseldorf",
        "query40": "nagel studio in essen",
        "query41": "nagel studio in erfurt",
        "query42": "nagel studio in essen",
        "query43": "nagel studio in friedrichshain-kreuzberg",
        "query44": "nagel studio in freiburg im breisgau",
        "query45": "nagel studio in gießen",
        "query46": "nagel studio in göttingen",
        "query47": "nagel studio in görlitz",
        "query48": "nagel studio in habach",
        "query49": "nagel studio in halle (saale)",
        "query50": "nagel studio in hamburg",
        "query51": "nagel studio in hansestadt lübeck",
        "query52": "nagel studio in heidelberg",
        "query53": "nagel studio in heisenberg",
        "query54": "nagel studio in herford",
        "query55": "nagel studio in hohnstein",
        "query56": "nagel studio in jena",
        "query57": "nagel studio in kambs",
        "query58": "nagel studio in karlsruhe",
        "query59": "nagel studio in köln",
        "query60": "nagel studio in landshut",
        "query61": "nagel studio in leipzig",
        "query62": "nagel studio in lübeck",
        "query63": "nagel studio in mainz",
        "query64": "nagel studio in mannheim",
        "query65": "nagel studio in mönchengladbach",
        "query66": "nagel studio in münchen",
        "query67": "nagel studio in nürnberg",
        "query68": "nagel studio in oberhausen",
        "query69": "nagel studio in offenburg",
        "query70": "nagel studio in paderborn",
        "query71": "nagel studio in potsdam",
        "query72": "nagel studio in regensburg",
        "query73": "nagel studio in remscheid",
        "query74": "nagel studio in rostock",
        "query75": "nagel studio in saarbrücken",
        "query76": "nagel studio in stuttgart",
        "query77": "nagel studio in tübingen",
        "query78": "nagel studio in ulm",
        "query79": "nagel studio in wesel",
        "query80": "nagel studio in wiesbaden",
        "query81": "nagel studio in wuppertal",
        "query82": "nagel studio in würzburg",
        "query83": "nagel studio in zella-mehlis",
        "query84": "nagel studio in zittau",
        "query85": "nagel studio in zwickau",
        # Note: The list can be expanded or refined as necessary.
    }

    for query_name, search_query in search_queries.items():
        logging.info(f"Processing {query_name}: {search_query}")
        scrape_google_maps(search_query)

if __name__ == "__main__":
    main()
