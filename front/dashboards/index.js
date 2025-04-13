document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generateChartBtn');
    const chartContainer = document.getElementById('chartContainer');
    
    generateBtn.addEventListener('click', async function() {
      const selectedChart = getSelectedChart(); // jedna opcja
      console.log("Wybrany wykres:", selectedChart); 
      const productTitle = document.querySelector('.search-input').value;
      
      if (!selectedChart || !productTitle) {
        alert('Please select a chart type and enter product title');
        return;
      }
  
      try {
        chartContainer.innerHTML = '<div class="loader">Generating chart...</div>';
        
        const chartData = await generateChart(selectedChart);
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


    async function generateChart(chartType) {
        const backendUrl = 'http://localhost:8081';

        const endpoints = {
        'price': `${backendUrl}/api/charts/price-chart`,
        'review': `${backendUrl}/api/charts/review-chart`,
        'rating': `${backendUrl}/api/charts/rating-chart`
        };
            
        const requestBody = {
            title: "productTitle",
            productSource: "amazon", // Przykład
            price: 100.00,
            rating: 4.5,
            reviewCount: 123
          };

        console.log("Wysyłam body:", JSON.stringify(requestBody));
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
        //  implementacja renderowania wykresu
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