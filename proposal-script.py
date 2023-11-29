import time
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

def write_in_file(list_of_dicts):
    json_file_path = "list_of_dicts.json"

    # Write the list of dictionaries to a JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(list_of_dicts, json_file)

# Create a Chrome web driver with the service
driver = webdriver.Chrome()

# The URL of the Nouns DAO proposal page
url = 'https://nouns.wtf/vote#candidates'

# Use the web driver to open the page
driver.get(url)

# Wait for the page to load (you may need to adjust the time)
time.sleep(10)
driver.implicitly_wait(10)

result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[2]/div[2]")))
#attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', result)
#print(attrs)
#print(result.get_attribute('innerHTML'))

div_inner_html = result.get_attribute('innerHTML')

soup = BeautifulSoup(div_inner_html, "html.parser")

# Extract specific elements (e.g., all <li> elements)
list_items = soup.find_all("a")
all_links = []
i=0
for item in list_items:
    innerSoup = BeautifulSoup(str(item), "html.parser")
    href = innerSoup.a['href']
    href = "https://nouns.wtf" + href
    #all_links.append(href)
    driver.get(href)
    dic = {}
    # Wait for the page to load (you may need to adjust the time)
    time.sleep(20)
    driver.implicitly_wait(20)
    header = "/html[1]/body[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/h1[1]"
    try: 
        result = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, header)))
        print("Title: "+result.get_attribute('innerHTML'))
        dic['Title'] = result.get_attribute('innerHTML')
    except Exception as e:
        continue

    body = "/html[1]/body[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]"
    result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, body)))
    #print("Body: "+result.get_attribute('innerHTML'))
    # Parse the HTML content
    soup = BeautifulSoup(result.get_attribute('innerHTML'), 'html.parser')

    # Extract the text content
    text_content = soup.get_text(separator='\n', strip=True)

    # Print the result
    #print(text_content)

    dic['Description'] = text_content

    result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]/div[1]/button[1]/p[1]")))
    #print("For: "+result.get_attribute('innerHTML'))
    for_votes = int(result.get_attribute('innerHTML').split()[0])

    dic['num_for_votes'] = for_votes
    for_list = []
    for k in range(for_votes):
        xpath_forprop = "/html[1]/body[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]/div[1]/div[1]/div["+str(k+1)+"]/div[1]/div[1]/p[1]"
        result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_forprop)))
        #print("For: "+result.get_attribute('innerHTML'))
        for_list.append(result.get_attribute('innerHTML'))
    dic['for_votes'] = for_list

    result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]/div[2]/button[1]/p[1]")))
    #print("Against: "+result.get_attribute('innerHTML'))
    against_votes = int(result.get_attribute('innerHTML').split()[0])

    dic['num_against_votes'] = against_votes

    against_list = []
    for k in range(against_votes):
        xpath_forprop = "/html[1]/body[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]/div[2]/div[1]/div["+str(k+1)+"]/div[1]/div[1]/p[1]"
        result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_forprop)))
        #print("Aginst: "+result.get_attribute('innerHTML'))
        against_list.append(result.get_attribute('innerHTML'))
    dic['against_votes'] = against_list
    all_links.append(dic)
    i+=1

#print(all_links)
write_in_file(all_links)