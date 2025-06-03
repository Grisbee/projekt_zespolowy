package service.generateChart.chartOptions;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import service.entities.Product;
import service.entities.NewProduct;
import service.pythonService.PostRequest;
import service.pythonService.PythonService;
import service.pythonService.pythonEndpoints.PythonEndpoints;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.Optional;

@Service
public class GeneratePriceChart {
    private final RestTemplate restTemplate;

    private static final String PRICE_CHART_ENDPOINT = PythonEndpoints.getPYTHON_PRICE_CHART_ENDPOINT();

    public GeneratePriceChart(PythonService pythonService) {
        this.restTemplate = pythonService.getRestTemplate();
    }

    public String generatePriceChart(List<NewProduct> products) {

        try{
            Map<String, Object> request = Map.of(
                    "products", products.stream().map(p -> {
                        String title = Optional.ofNullable(p.getAmazonTitle())
                                .orElseGet(() -> Optional.ofNullable(p.getKeepaName()).orElse(""));
                        return Map.of(
                                "productSource", Optional.ofNullable(p.getProductSrc()).orElse(""),
                                "price", Optional.ofNullable(p.getPriceNew()).orElse(0),
                                "title", title
                        );
                    })
                            .collect(Collectors.toList())
            );
            PostRequest postRequest = new PostRequest();
            return postRequest.postRequest(restTemplate, PRICE_CHART_ENDPOINT, request);
        } catch (Exception e){
            throw new RuntimeException("error calling Python service", e);
        }

    }
}
