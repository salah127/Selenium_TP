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
medical_request = "dentiste"
insurance_type = "secteur 1"
consultation_type = "in-person"
price_min = "50"
price_max = "150"
geographical_filter = "75015"


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
 
# === Entrer la requête médicale ===

accepter_btn = wait.until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button")))
accepter_btn.click()

search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.searchbar-query-input")))
place_input = driver.find_element(By.CSS_SELECTOR, "input.searchbar-place-input")

search_input.send_keys(medical_request)
# place_input.clear()
place_input.send_keys(geographical_filter)
 
# === Cliquer sur Rechercher ===
submit_btn = driver.find_element(By.CSS_SELECTOR, "button.searchbar-submit-button")
submit_btn.click()
 
# === Attendre les résultats + faire défiler pour tout charger ===è
time.sleep(4)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)
 
# === Extraire les cartes de médecins ===
cards = driver.find_elements(By.CSS_SELECTOR, "li.w-full")[:max_results]
print(f"🔍 {len(cards)} cartes de médecins détectées")
 
medecins = []
print("cards", len(cards))
time.sleep(200)
 
for card in cards:
    if len(medecins) >= max_results:
        break 

    try:
        nom = card.find_element(By.CSS_SELECTOR, "h2").text.strip()
    except:
        nom = "Non précisé"
 
    try:
        specialite = card.find_element(By.CSS_SELECTOR, ".dl-doctor-card-speciality-title").text.strip()
    except:
        specialite = "Non précisée"
 
    try:
        adresse_lines = card.find_elements(By.CSS_SELECTOR, "p.dl-text-neutral-130")
        adresse = adresse_lines[0].text.strip()
        cp_ville = adresse_lines[1].text.strip()
        code_postal = cp_ville.split(' ')[0]
        ville = ' '.join(cp_ville.split(' ')[1:])
    except:
        adresse = code_postal = ville = "Non précisé"
 
    try:
        dispo_slots = card.find_elements(By.CSS_SELECTOR, "div[data-test='available-slot']")
        disponibilites = [slot.text.strip() for slot in dispo_slots if slot.text.strip()]
        disponibilite = ", ".join(disponibilites) if disponibilites else "Non précisée"
    except:
        disponibilite = "Non précisée"
 
    if disponibilite == "Non précisée":
        continue  # Ne garde que les médecins avec des horaires visibles
 
    medecins.append({
        "Nom": nom,
        "Spécialité": specialite,
        "Adresse": adresse,
        "Code Postal": code_postal,
        "Ville": ville,
        "Disponibilités": disponibilite
    })
 
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