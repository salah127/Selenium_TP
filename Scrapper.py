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
from Get_Inputs import ask_user_input



user_input = ask_user_input()

# Update variables with user input
max_results = user_input["max_results"]
availability_start = user_input["availability_start"]
availability_end = user_input["availability_end"]
medical_request = user_input["medical_request"]
insurance_type = user_input["insurance_type"]
consultation_type = user_input["consultation_type"]
price_min = user_input["price_min"]
price_max = user_input["price_max"]
geographical_filter = user_input["geographical_filter"]



root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()
half_width = screen_width // 2
driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install())
driver.set_page_load_timeout(3000)
driver.implicitly_wait(10)
driver.set_window_size(screen_width, screen_height)
driver.get("https://www.doctolib.fr")
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
 
 
submit_btn = driver.find_element(By.CSS_SELECTOR, "button.searchbar-submit-button")
submit_btn.click()
time.sleep(2)

# driver.get(f"https://www.doctolib.fr/search?location={geographical_filter}&speciality={medical_request}")
# time.sleep(2)
 

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)
 
cards = driver.find_elements(By.CSS_SELECTOR, "div.dl-card-content")[1:]
print(f" {len(cards)} cartes de médecins détectées")
 
medecins = []
print("cards", len(cards))
# time.sleep(2000)
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
        availabilities_container = card.find_element(By.CLASS_NAME, "m-16")
        Disponibilités = availabilities_container.text.strip()
        if Disponibilités.startswith(("Prochaines")) or Disponibilités.startswith(("Aucun")) or Disponibilités.startswith(("lundi")) or Disponibilités.startswith(("mardi")) or Disponibilités.startswith(("mercredi")) or Disponibilités.startswith(("jeudi")) or Disponibilités.startswith(("vendredi")) or Disponibilités.startswith(("samedi")) or Disponibilités.startswith(("dimanche")):
            Disponibilités = " ".join(line.strip() for line in Disponibilités.strip().split("\n") if line.strip())
    except:
        Disponibilités = "Aucun horaire affiché"
    
   
    try:
        additional_info = card.find_element(By.CSS_SELECTOR, "div.relative.w-48.h-48")
        if additional_info and additional_info.find_elements(By.TAG_NAME, "div"):
            consultation = "Téléconsultation"
        else:
            consultation = "in-person"
    except:
        consultation = "Informations supplémentaires non disponibles"
    
    try:
        flex_elements = card.find_elements(By.CSS_SELECTOR, ".flex.flex-wrap.gap-x-4")
        for index, element in enumerate(flex_elements):
            if index % 2 != 0:  # Process only even indices
                Secteur = element.text.strip()
                print("Flex Element Text:", element.text.strip())
            else:
                Adresse = element.find_elements(By.CSS_SELECTOR, ".XZWvFVZmM9FHf461kjNO.G5dSlmEET4Zf5bQ5PR69")
                for index, element in enumerate(Adresse):
                    if index % 2 != 0:
                        Code_postal_Ville = element.text.strip()
                        Code_postal = Code_postal_Ville.split(" ")[0]
                        Ville = Code_postal_Ville.split(" ")[-1]
                    else:
                        Rue = element.text.strip()
    except:
        Secteur = "Pharmacie non précisée"
        Rue = "Rue non précisée"
        Code_postal = "Code postal non précisé"
        Ville = "Ville non précisée"
        print("No elements with 'flex flex-wrap gap-x-4' found")
    
    
    
    Tarif = "Tarif non précisé"
            

    
    if (consultation_type == "in-person" and consultation == "in-person") or (consultation_type == "Téléconsultation" and consultation == "teleconsultation") or (consultation_type == ""):
        medecins.append({
        "Nom": nom,
        "Disponibilités": Disponibilités,
        "consultation_type": consultation,
        "Secteur": Secteur,
        "Tarif": Tarif,        
        "Rue": Rue,
        "Code_postal": Code_postal,
        "Ville": Ville,
    })
        print("medecins", medecins)


# === Sauvegarde CSV ===
if medecins:
    with open("medecins_doctolib.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=medecins[0].keys())
        writer.writeheader()
        writer.writerows(medecins)
    print(f" {len(medecins)} médecins exportés dans medecins_doctolib.csv")
else:
    print(" Aucun médecin avec horaires affichés n'a été trouvé.")
 
driver.quit()