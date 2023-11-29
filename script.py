import time
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

# Create a Chrome web driver with the service
driver = webdriver.Chrome()

# The URL of the Nouns DAO proposal page
url = 'https://nouns.wtf/vote'

# Use the web driver to open the page
driver.get(url)

# Wait for the page to load (you may need to adjust the time)
time.sleep(10)
driver.implicitly_wait(10)

result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[2]")))
attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', result)
print(attrs)
#print(result.get_attribute('innerHTML'))

div_inner_html = result.get_attribute('innerHTML')

soup = BeautifulSoup(div_inner_html, "html.parser")

# Extract specific elements (e.g., all <li> elements)
list_items = soup.find_all("a")
proposals = {}
executed_proposals = []
i=0
for item in list_items:
    innerSoup = BeautifulSoup(str(item), "html.parser")
    proposal_title = innerSoup.find("span", class_="Proposals_proposalTitle__VkUVe").text
    proposal_status = innerSoup.find("div", class_="Proposals_proposalStatusWrapper__2axTx Proposals_votePillWrapper__SYS_O").text
    words = proposal_title.split()
    nounId, prop = words[0], ' '.join(words[1:])
    print(nounId)
    print(proposal_title)
    print(prop)
    dict = {
        "status": proposal_status,
        "proposal": prop
    }
    proposals[nounId] = dict
    if(proposal_status == 'Canceled'):
        new_dict = {
            "nounId": nounId,
            "status": proposal_status,
            "proposal": prop
        }
        executed_proposals.append(new_dict)
print(executed_proposals)
