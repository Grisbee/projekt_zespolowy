package service.controller.chartController;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import service.controller.controllerEndpoints.ChartControllerEndpoints;
import service.entities.Product;
import service.generateChart.GenerateChartOption;

import java.util.List;

@RestController
@RequestMapping(ChartControllerEndpoints.BASE)
public class ChartController {

    private final GenerateChartOption generateChart;

    public ChartController(GenerateChartOption generateChart) {
        this.generateChart = generateChart;
    }

    @PostMapping(ChartControllerEndpoints.PRICE_CHART)
    public String generatePriceChart(@RequestBody List<Product> products) {
        return generateChart.generatePriceChart(products);
    }

    @PostMapping(ChartControllerEndpoints.RATING_CHART)
    public String generateRatingChart(@RequestBody List<Product> products) {
        return generateChart.generateRatingChart(products);
    }

    @PostMapping(ChartControllerEndpoints.REVIEW_CHART)
    public String generateReviewChart(@RequestBody List<Product> products) {
        return generateChart.generateReviewChart(products);
    }
}
