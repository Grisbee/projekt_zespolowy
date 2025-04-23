# Migracja z JPA na Supabase API

## Podsumowanie zmian dla metod repozytorium

| Metoda JPA | Funkcja Supabase | Uwagi |
|------------|-----------------|-------|
| `findAllProducts(Pageable)` | `find_all_products(p_page_size, p_page_number)` | Wymagane dodatkowe wywołanie `count_all_products()` |
| `findProductsByCategoryNames(List<String>, Pageable)` | `find_products_by_category_names(p_categories, p_page_size, p_page_number)` | Wymagane dodatkowe wywołanie `count_products_by_categories(p_categories)` |
| `searchProductsByKey(String, Pageable)` | `search_products_by_key(p_query, p_page_size, p_page_number)` | Wymagane dodatkowe wywołanie `count_products_by_key(p_query)` |
