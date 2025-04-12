package service.generateChart.chartOptions;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import service.entities.Product;
import service.pythonService.PostRequest;
import service.pythonService.PythonService;
import service.pythonService.pythonEndpoints.PythonEndpoints;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class GeneratePriceChart {
    private final RestTemplate restTemplate;

    private static final String PRICE_CHART_ENDPOINT = PythonEndpoints.getPYTHON_PRICE_CHART_ENDPOINT();

    public GeneratePriceChart(PythonService pythonService) {
        this.restTemplate = pythonService.getRestTemplate();
    }

    public String generatePriceChart(List<Product> products) {

        try{
            Map<String, Object> request = Map.of(
                    "products", products.stream().map(p -> Map.of(
                            "productSource", p.getProductSource(),
                            "price", p.getPrice(),
                            "title", p.getTitle()
                    ))
                            .collect(Collectors.toList())
            );
            PostRequest postRequest = new PostRequest();
            return postRequest.postRequest(restTemplate, PRICE_CHART_ENDPOINT, request);
        } catch (Exception e){
            throw new RuntimeException("error calling Python service", e);
        }

    }
}
