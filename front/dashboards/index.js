document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generateChartBtn');
    const chartContainer = document.getElementById('chartContainer');
    
    // Funkcja pomocnicza do odczytu ciasteczka po nazwie
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Pobierz wybrany produkt z ciasteczka
    const selectedProductCookie = getCookie('selectedProduct');
    let selectedProduct = null;
    if (selectedProductCookie) {
        try {
            selectedProduct = JSON.parse(decodeURIComponent(selectedProductCookie));
            console.log('Odczytany produkt z ciasteczka:', selectedProduct);
        } catch (e) {
            console.error('Error parsing product data from cookie:', e);
        }
    }
    
    if (selectedProduct) {
        document.querySelector('.search-input').value = selectedProduct.amazonTitle || selectedProduct.keepaName;
    }
    
    generateBtn.addEventListener('click', async function() {
        const selectedChart = getSelectedChart();
        console.log("Wybrany wykres:", selectedChart);
        
        if (!selectedChart || !selectedProduct) {
            alert('Please select a chart type and make sure a product is selected');
            return;
        }
  
        try {
            chartContainer.innerHTML = '<div class="loader">Generating chart...</div>';
            
            const chartData = await generateChart(selectedChart, selectedProduct);

            if (selectedChart === 'product-data') {
                renderProductData(chartData);
            } else {
                renderChartImage(chartData);
            }
            
        } catch (error) {
            console.error('Error:', error);
            chartContainer.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        }
    });

    function getSelectedChart() {
        const checked = document.querySelector('.settings-panel input[type="checkbox"]:checked');
        return checked ? checked.dataset.type : null;
    }

    async function generateChart(chartType, product) {
        const backendUrl = 'http://localhost:8081';

        const endpoints = {
            'price-new': `${backendUrl}/api/price-new`,
            'price-used': `${backendUrl}/api/price-used`,
            'price-box': `${backendUrl}/api/price-box`,
            'product-data': `${backendUrl}/api/product-data`
        };

        console.log('Dane produktu przed budowaniem requestBody:', {
            priceNew: product.priceNew,
            rating: product.rating,
            reviewCount: product.reviewCount
        });

        const requestBody = {
            keepa_name: product.keepaName || product.amazonTitle
        };

        console.log("Wysyłam body:", JSON.stringify(requestBody));
        console.log("Endpoint:", endpoints[chartType]);
    
        const response = await fetch(endpoints[chartType], {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });
    
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    
        return await response.json();
    }

    function renderChartImage(chartData) {
        // Clear previous content
        chartContainer.innerHTML = '';

        if (chartData && chartData.chart) {
            const img = document.createElement('img');
            img.src = chartData.chart; // Set the source to the base64 data URL
            img.alt = 'Generated Chart';
            img.style.maxWidth = '100%'; // Optional: Make the image responsive
            img.style.height = 'auto'; // Optional: Maintain aspect ratio
            chartContainer.appendChild(img);
        } else {
            chartContainer.innerHTML = '<div class="error">Could not load chart data.</div>';
            console.error('Invalid chart data received:', chartData);
        }
    }

    function renderProductData(data) {
        // Clear previous content
        chartContainer.innerHTML = '';

        if (data && data.product) {
            const product = data.product;
            let html = `
                <div class="product-details">
                    <h3>Product Details</h3>
                    <p><strong>Keepa Name:</strong> ${product.keepa_name}</p>
                    <p><strong>Amazon Title:</strong> ${product.amazon_title}</p>
                    <p><strong>Keepa Link:</strong> <a href="${product.link_keepa}" target="_blank">${product.link_keepa}</a></p>
                    <p><strong>Amazon Link:</strong> <a href="${product.link_amazon}" target="_blank">${product.link_amazon}</a></p>
                    <p><strong>Price (New):</strong> ${product.price_new ? (product.price_new / 100).toFixed(2) : 'N/A'}</p>
                    <p><strong>Price (Used):</strong> ${product.price_used ? (product.price_used / 100).toFixed(2) : 'N/A'}</p>
                    <p><strong>Price (Box):</strong> ${product.price_box ? (product.price_box / 100).toFixed(2) : 'N/A'}</p>
                    <p><strong>Rating:</strong> ${product.rating || 'N/A'}</p>
                    <p><strong>Review Count:</strong> ${product.review_count || '0'}</p>
                    <p><strong>Currency:</strong> ${product.currency || 'N/A'}</p>
                    <p><strong>Product Source:</strong> ${product.product_src || 'N/A'}</p>
                </div>
            `;

            if (data.similar_products && data.similar_products.length > 0) {
                html += `
                    <div class="similar-products">
                        <h3>Similar Products</h3>
                        <ul>
                `;
                data.similar_products.forEach(similarProduct => {
                    html += `<li>${similarProduct.amazon_title || similarProduct.keepa_name}</li>`;
                });
                html += `
                        </ul>
                    </div>
                `;
            }

            chartContainer.innerHTML = html;
        } else {
            chartContainer.innerHTML = '<div class="error">Could not load product data.</div>';
            console.error('Invalid product data received:', data);
        }
    }
});