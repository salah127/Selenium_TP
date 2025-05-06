import argparse
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import tkinter as tk

max_results = 10
availability_start = "01/01/2025"
availability_end = "31/12/2025"
# medical_request = "Médecin généraliste"
medical_request = "medecin-generaliste"
insurance_type = "secteur 1"
consultation_type = "in-person"
price_min = "50"
price_max = "150"
geographical_filter = "Paris"


# === Configuration WebDriver ===
# chrome_options = Options()
# chrome_options.add_argument("--start-maximized")
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


 
# # === Aller sur Doctolib ===
# driver.get("https://www.doctolib.fr")

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()
half_width = screen_width // 2
driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install())
driver.set_page_load_timeout(3000)
driver.implicitly_wait(10)
driver.get("https://www.doctolib.fr")
driver.set_window_size(half_width, screen_height)
driver.set_window_position(0, 0)
wait = WebDriverWait(driver, 15)
 


accepter_btn = wait.until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button")))
if accepter_btn.is_displayed():
    accepter_btn.click()


search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.searchbar-query-input")))
place_input = driver.find_element(By.CSS_SELECTOR, "input.searchbar-place-input")

search_input.send_keys(medical_request)
time.sleep(1)
place_input.clear()
place_input.send_keys(geographical_filter)
time.sleep(2)
 
# === Cliquer sur Rechercher ===
submit_btn = driver.find_element(By.CSS_SELECTOR, "button.searchbar-submit-button")
submit_btn.click()
time.sleep(2)

driver.get(f"https://www.doctolib.fr/search?location={geographical_filter}&speciality={medical_request}")
# https://www.doctolib.fr/search?location=fontainebleau&speciality=medecin-generaliste
# driver.get("https://www.doctolib.fr/search?location=fontainebleau&speciality=medecin-generaliste")

time.sleep(2)
 

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)
 
# === Extraire les cartes de médecins ===
cards = driver.find_elements(By.CSS_SELECTOR, "div.dl-card-content")[1:]
print(f"🔍 {len(cards)} cartes de médecins détectées")
 
medecins = []
print("cards", len(cards))
# time.sleep(200)
 
for card in cards:
    try:
        print("card", card.find_element(By.CSS_SELECTOR, "h2").text.strip())
    except Exception as e:
        print("card", "No title found")
    if len(medecins) >= max_results:
        break 

    try:
        nom = card.find_element(By.CSS_SELECTOR, "h2").text.strip()
    except:
        nom = "Non précisé"
        
    try:
        availabilities_container = driver.find_element(By.CSS_SELECTOR, "div[data-test-id='availabilities-container']")
        container_text = availabilities_container.text.strip()
        print(f"✅ Texte extrait : {container_text}")
    except:
        container_text = "Aucun horaire affiché"        
        
        
    
 
    medecins.append({
        "Nom": nom,
        "Disponibilités": container_text
    })
    print("medecins", medecins)
 
# === Sauvegarde CSV ===
if medecins:
    with open("medecins_doctolib.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=medecins[0].keys())
        writer.writeheader()
        writer.writerows(medecins)
    print(f"✅ {len(medecins)} médecins exportés dans medecins_doctolib.csv")
else:
    print("❌ Aucun médecin avec horaires affichés n'a été trouvé.")
 
driver.quit()