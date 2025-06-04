// Funkcja do pobierania produktów z backendu
async function fetchProducts() {
    try {
        const response = await fetch('http://localhost:8081/products');

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`HTTP error! status: ${response.status}`, errorText);
            return; // Zatrzymaj wykonywanie jeśli odpowiedź nie jest OK
        }

        // Zmieniamy parsowanie na tekst, żeby zobaczyć surową odpowiedź
        const responseText = await response.text();
        console.log('Surowa odpowiedź z backendu:', responseText);

        // Spróbuj sparsować jako JSON po obejrzeniu surowej odpowiedzi
        const products = JSON.parse(responseText);
        displayProducts(products);

    } catch (error) {
        console.error('Error fetching products:', error);
    }
}

// Funkcja do wyświetlania produktów
function displayProducts(products) {
    const productsContainer = document.querySelector('.products-container');
    productsContainer.innerHTML = ''; // Wyczyść kontener

    products.forEach(product => {
        const productCard = createProductCard(product);
        productsContainer.appendChild(productCard);
    });
}

// Funkcja do tworzenia karty produktu
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';

    // Używamy nowych nazw pól z NewProduct
    const title = product.amazonTitle || product.keepaName;
    const rating = product.rating || 'N/A';
    const reviewCount = product.reviewCount || '0';
    // Cena przychodzi w groszach/centach, dzielimy przez 100 i formatujemy
    const price = product.priceNew !== null && product.priceNew !== undefined ? (product.priceNew / 100).toFixed(2) : 'N/A';
    const currency = product.currency || 'USD';

    card.innerHTML = `
        <div class="product-image">
            <span class="material-symbols-outlined">image</span>
        </div>
        <div class="product-info">
            <h3 class="product-title">${title}</h3>
            <div class="product-meta">
                <div class="product-rating">
                    <span class="rating-value">Rating: ${rating}</span>
                </div>
                <div class="review-count">${reviewCount} reviews</div>
            </div>
            <p class="product-price">${price} ${currency}</p>
            <a href="dashboards.html" class="product-generate" data-product='${JSON.stringify(product)}'>
                Generate Dashboard
            </a>
        </div>
    `;

    // Dodaj obsługę kliknięcia przycisku Generate Dashboard
    const generateButton = card.querySelector('.product-generate');
    generateButton.addEventListener('click', (e) => {
        e.preventDefault();
        const productData = JSON.parse(generateButton.dataset.product);
        
        // Use keepaName for identifying the product and save it to the cookie
        if (!productData.keepaName) {
            console.error('Product keepaName is missing:', productData);
            alert('Error: Product identifier is missing. Please try again.');
            return;
        }
        
        console.log('Przekazywany produkt (do cookies):', productData);
        
        // Save the entire product object (which includes keepaName) in the cookie
        document.cookie = 'selectedProduct=' + encodeURIComponent(JSON.stringify(productData)) + '; path=/; max-age=3600'; // Ciasteczko ważne przez 1 godzinę
        
        window.location.href = 'dashboards.html';
    });

    return card;
}

// Funkcja do wyszukiwania produktów
function setupSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchButton = document.querySelector('.search-button');

    searchButton.addEventListener('click', () => {
        const searchTerm = searchInput.value.toLowerCase();
        const productCards = document.querySelectorAll('.product-card');

        productCards.forEach(card => {
            const title = card.querySelector('.product-title').textContent.toLowerCase();
            if (title.includes(searchTerm)) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    });

    // Dodaj obsługę wyszukiwania po naciśnięciu Enter
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchButton.click();
        }
    });
}

// Inicjalizacja
document.addEventListener('DOMContentLoaded', () => {
    fetchProducts();
    setupSearch();
});
