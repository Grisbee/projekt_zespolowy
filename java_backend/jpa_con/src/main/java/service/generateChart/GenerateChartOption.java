package service.generateChart;

import org.springframework.web.client.RestTemplate;
import service.entities.NewProduct;
import service.entities.Product;

import java.util.List;

public interface GenerateChartOption {
    String generatePriceChart(List<NewProduct> products);
    String generateReviewChart(List<NewProduct> products);
    String generateRatingChart(List<NewProduct> products);
}
