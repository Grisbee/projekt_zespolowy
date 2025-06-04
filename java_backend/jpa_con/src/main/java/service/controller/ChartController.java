package service.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import service.controller.controllerEndpoints.ControllerEndpoints;
import service.entities.NewProduct;
import service.generateChart.GenerateChart;
import service.generateChart.GenerateChartOption;
import service.generateChart.chartOptions.GeneratePriceChart;

import java.util.List;

@RestController
@RequestMapping(ControllerEndpoints.BASE)
public class ChartController {

    private final GenerateChartOption generateChart;

    public ChartController(GenerateChartOption generateChart) {
        this.generateChart = generateChart;
    }

    @PostMapping(ControllerEndpoints.PRICE_CHART)
    public String generatePriceChart(@RequestBody List<NewProduct> products) {
        System.out.println("Generating price chart...");
        return generateChart.generatePriceChart(products);
    }

    @PostMapping(ControllerEndpoints.RATING_CHART)
    public String generateRatingChart(@RequestBody List<NewProduct> products) {
        System.out.println("Generating rating chart...");
        return generateChart.generateRatingChart(products);
    }

    @PostMapping(ControllerEndpoints.REVIEW_CHART)
    public String generateReviewChart(@RequestBody List<NewProduct> products) {
        System.out.println("Generating review chart...");
        return generateChart.generateReviewChart(products);
    }
}
