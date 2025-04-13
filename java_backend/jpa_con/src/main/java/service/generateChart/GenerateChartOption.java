package service.generateChart;

import org.springframework.web.client.RestTemplate;
import service.entities.Product;

import java.util.List;

public interface GenerateChartOption {
    String generatePriceChart(List<Product> products);
    String generateReviewChart(List<Product> products);
    String generateRatingChart(List<Product> products);
}
