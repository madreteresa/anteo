import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.spaziocinema.info/cinema"

def fetch_anteo_schedule():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print(f"Errore durante il download della pagina: {response.status_code}")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    schedule_data = {}

    # Trova tutti i blocchi di film / giorni presenti nella pagina
    # SpazioCinema organizza i film per data, sala e orari
    items = soup.select('.item-cinema, .film-item, article') 

    for item in items:
        # Estrazione del titolo
        title_el = item.select_one('.title, h2, h3, .film-title')
        if not title_el:
            continue
        title = title_el.get_text(strip=True)

        # Estrazione della sala
        sala_el = item.select_one('.sala, .cinema-sala')
        sala = sala_el.get_text(strip=True) if sala_el else "Anteo Palazzo del Cinema"

        # Estrazione orari
        showtimes = [st.get_text(strip=True) for st in item.select('.orario, .time, .showtime')]
        
        # Estrazione data (se disponibile, altrimenti usa la data odierna)
        date_el = item.select_one('.data, .date')
        if date_el:
            date_str = date_el.get_text(strip=True)
            # Converte la data nel formato YYYY-MM-DD
            try:
                date_key = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                date_key = datetime.now().strftime("%Y-%m-%d")
        else:
            date_key = datetime.now().strftime("%Y-%m-%d")

        if date_key not in schedule_data:
            schedule_data[date_key] = []

        schedule_data[date_key].append({
            "film": title,
            "sala": sala,
            "genre": "",
            "duration": "",
            "showtimes": showtimes
        })

    return schedule_data

if __name__ == "__main__":
    data = fetch_anteo_schedule()
    with open("schedule.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Mappatura completata e salvata in schedule.json!")