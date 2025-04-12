package service.generateChart;

import org.springframework.web.client.RestTemplate;
import service.entities.Product;

import java.util.List;

public interface GenerateChartOption {
    public String generatePriceChart(List<Product> products);
    public String generateReviewChart();
    public String generateRatingChart();
}
