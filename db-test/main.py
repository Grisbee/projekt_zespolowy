#!/usr/bin/env python3
"""
Skrypt Python testujący funkcje SQL w bazie Supabase dla systemu zarządzania produktami.
Dane konfiguracyjne są odczytywane z pliku .env
"""

import requests
import json
from pprint import pprint
import time
import os
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()

# Konfiguracja Supabase - dane pobierane z pliku .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Sprawdzenie, czy zmienne zostały poprawnie załadowane
if not SUPABASE_URL or not SUPABASE_KEY:
    print("Błąd: Brak wymaganych zmiennych w pliku .env")
    print("Upewnij się, że plik .env zawiera SUPABASE_URL i SUPABASE_KEY")
    exit(1)

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def call_function(function_name, data={}):
    """Wywołuje funkcję RPC w Supabase."""
    url = f"{SUPABASE_URL}/rest/v1/rpc/{function_name}"
    response = requests.post(url, headers=HEADERS, json=data)
    
    print(f"\n=== Wywołanie: {function_name} ===")
    print(f"Dane wejściowe: {json.dumps(data, indent=2)}")
    print(f"Status: {response.status_code}")
    
    try:
        result = response.json()
        print("Wynik:")
        pprint(result)
        return result
    except ValueError:
        print("Brak danych JSON w odpowiedzi")
        print(response.text)
        return None

def main():
    """Główna funkcja testująca."""
    print("\n=== TESTY FUNKCJI BAZY DANYCH SUPABASE (PYTHON) ===\n")
    print(f"Używam bazy: {SUPABASE_URL}")
    
    # 1. Dodawanie produktów testowych
    print("\n--- Test 1: Dodawanie produktów ---")
    products = [
        {
            "title": "Smartfon Samsung Galaxy S21",
            "description": "Flagowy smartfon z procesorem Exynos, 8GB RAM, 128GB pamięci",
            "price": 3499.99,
            "url": "https://example.com/samsung-s21",
            "product_source": "web",
            "currency": "PLN",
            "rating": 4.6,
            "review_count": 892,
            "img_url": "https://example.com/images/samsung-s21.jpg"
        },
        {
            "title": "Słuchawki Sony WH-1000XM4",
            "description": "Bezprzewodowe słuchawki z aktywną redukcją szumów",
            "price": 1299.99,
            "url": "https://example.com/sony-wh1000xm4",
            "product_source": "store",
            "currency": "PLN",
            "rating": 4.9,
            "review_count": 3210,
            "img_url": "https://example.com/images/sony-wh1000xm4.jpg"
        }
    ]
    
    product_ids = []
    for product in products:
        product_id = call_function("add_product", product)
        if product_id:
            product_ids.append(product_id)
            print(f"Dodano produkt o ID: {product_id}")
    
    if not product_ids:
        print("Błąd: Nie udało się dodać produktów testowych!")
        return
    
    time.sleep(1)  # Krótka pauza między operacjami
    
    # 2. Dodawanie kategorii
    print("\n--- Test 2: Dodawanie kategorii ---")
    categories = ["Elektronika", "Smartfony", "Audio", "Akcesoria"]
    category_ids = []
    
    for category_name in categories:
        category_id = call_function("add_category", {"p_category_name": category_name})
        if category_id:
            category_ids.append(category_id)
            print(f"Dodano kategorię '{category_name}' o ID: {category_id}")
    
    time.sleep(1)
    
    # 3. Przypisywanie produktów do kategorii
    print("\n--- Test 3: Przypisywanie produktów do kategorii ---")
    # Pierwszy produkt - smartfon
    call_function("assign_product_to_category", {
        "p_product_id": product_ids[0],
        "p_category_name": "Elektronika"
    })
    
    call_function("assign_product_to_category", {
        "p_product_id": product_ids[0],
        "p_category_name": "Smartfony"
    })
    
    # Drugi produkt - słuchawki
    call_function("assign_product_to_category", {
        "p_product_id": product_ids[1],
        "p_category_name": "Elektronika"
    })
    
    call_function("assign_product_to_category", {
        "p_product_id": product_ids[1],
        "p_category_name": "Audio"
    })
    
    time.sleep(1)
    
    # 4. Dodawanie historii cen
    print("\n--- Test 4: Dodawanie historii cen ---")
    # Historia cen dla pierwszego produktu
    price_history_smartphone = [
        {"price": 3699.99, "history_id": "20240401-" + str(product_ids[0])},
        {"price": 3599.99, "history_id": "20240410-" + str(product_ids[0])},
        {"price": 3499.99, "history_id": "20240420-" + str(product_ids[0])}
    ]
    
    for entry in price_history_smartphone:
        call_function("add_price_history", {
            "p_product_id": product_ids[0],
            "p_price": entry["price"],
            "p_history_id": entry["history_id"]
        })
    
    # Historia cen dla drugiego produktu
    price_history_headphones = [
        {"price": 1399.99, "history_id": "20240401-" + str(product_ids[1])},
        {"price": 1349.99, "history_id": "20240410-" + str(product_ids[1])},
        {"price": 1299.99, "history_id": "20240420-" + str(product_ids[1])}
    ]
    
    for entry in price_history_headphones:
        call_function("add_price_history", {
            "p_product_id": product_ids[1],
            "p_price": entry["price"],
            "p_history_id": entry["history_id"]
        })
    
    time.sleep(1)
    
    # 5. Testowanie wyszukiwania produktów
    print("\n--- Test 5: Wyszukiwanie produktów ---")
    search_tests = [
        {"p_search_term": "Samsung"},
        {"p_min_price": 3000, "p_max_price": 5000},
        {"p_category": "Audio"},
        {"p_min_rating": 4.8}
    ]
    
    for i, search_params in enumerate(search_tests):
        print(f"\nWyszukiwanie {i+1}:")
        call_function("search_products", search_params)
        time.sleep(0.5)
    
    # 6. Testowanie statystyk i raportów
    print("\n--- Test 6: Statystyki i raporty ---")
    
    # Statystyki cenowe produktu
    for product_id in product_ids:
        call_function("get_product_price_stats", {"p_product_id": product_id})
        time.sleep(0.5)
    
    # Statystyki kategorii
    call_function("get_category_stats")
    
    time.sleep(1)
    
    # 7. Testowanie szczegółów produktu
    print("\n--- Test 7: Szczegóły produktu ---")
    for product_id in product_ids:
        call_function("get_product_details", {"p_product_id": product_id})
        time.sleep(0.5)
    
    # 8. Aktualizacja produktu
    print("\n--- Test 8: Aktualizacja produktu ---")
    update_result = call_function("update_product", {
        "p_product_id": product_ids[0],
        "p_price": 3399.99,
        "p_description": "Flagowy smartfon z procesorem Exynos, 8GB RAM, 128GB pamięci, promocja!"
    })
    
    print(f"Aktualizacja powiodła się: {update_result}")
    
    print("\nTesty zakończone!")

if __name__ == "__main__":
    main()