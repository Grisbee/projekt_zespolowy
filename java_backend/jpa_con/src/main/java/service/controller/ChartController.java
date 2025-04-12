package service.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import service.entities.Product;
import service.generateChart.chartOptions.GeneratePriceChart;

import java.util.List;

@RestController
@RequestMapping("/api/charts")
public class ChartController {

    private final GeneratePriceChart generateChart;

    public ChartController(GeneratePriceChart generateChart) {
        this.generateChart = generateChart;
    }

    @PostMapping("/price-chart")
    public String generatePriceChart(@RequestBody List<Product> products) {
        return generateChart.generatePriceChart(products);
    }
}
