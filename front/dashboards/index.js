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
            renderChart(chartData);
            
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
            'price': `${backendUrl}/api/charts/price-chart`,
            'review': `${backendUrl}/api/charts/review-chart`,
            'rating': `${backendUrl}/api/charts/rating-chart`
        };

        console.log('Dane produktu przed budowaniem requestBody:', {
            priceNew: product.priceNew,
            rating: product.rating,
            reviewCount: product.reviewCount
        });

        const requestBody = {
            title: product.amazonTitle || product.keepaName,
            productSource: product.productSrc || 'amazon',
            price: product.priceNew ? (product.priceNew / 100) : 0,
            rating: parseFloat(product.rating) || 0,
            reviewCount: parseInt(product.reviewCount) || 0
        };

        console.log("Wysyłam body:", JSON.stringify([requestBody]));
        console.log("Endpoint:", endpoints[chartType]);
    
        const response = await fetch(endpoints[chartType], {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify([requestBody])
        });
    
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    
        return await response.json();
    }

    function renderChart(chartData) {
        chartContainer.innerHTML = `
            <div class="chart-item">
                <h3>${chartData.chartType || 'Generated Chart'}</h3>
                <div class="chart-content">
                    ${JSON.stringify(chartData, null, 2)}
                </div>
            </div>
        `;
    }
});