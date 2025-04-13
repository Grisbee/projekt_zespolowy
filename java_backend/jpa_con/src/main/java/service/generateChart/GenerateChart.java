package service.generateChart;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import service.entities.Product;
import service.generateChart.chartOptions.GeneratePriceChart;
import service.generateChart.chartOptions.GenerateRatingChart;
import service.generateChart.chartOptions.GenerateReviewChart;
import service.pythonService.PythonService;

import java.util.List;

@Service
public class GenerateChart implements GenerateChartOption {
    private final GeneratePriceChart priceChart;
    private final GenerateRatingChart ratingChart;
    private final GenerateReviewChart reviewChart;


    public GenerateChart(GeneratePriceChart priceChart, GenerateRatingChart ratingChart, GenerateReviewChart reviewChart) {
        this.priceChart = priceChart;
        this.ratingChart = ratingChart;
        this.reviewChart = reviewChart;
    }

    @Override
    public String generatePriceChart(List<Product> products) {
        return priceChart.generatePriceChart(products);
    }

    @Override
    public String generateReviewChart(List<Product> products) {
        return reviewChart.generateReviewChart(products);
    }

    @Override
    public String generateRatingChart(List<Product> products) {;
        return ratingChart.generateRatingChart(products);
    }
}
