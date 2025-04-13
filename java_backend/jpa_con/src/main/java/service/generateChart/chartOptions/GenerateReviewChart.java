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
public class GenerateReviewChart {
    private final RestTemplate restTemplate;

    private static final String REVIEW_CHART_ENDPOINT = PythonEndpoints.getPYTHON_REVIEW_CHART_ENDPOINT();

    public GenerateReviewChart(PythonService pythonService) {
        this.restTemplate = pythonService.getRestTemplate();
    }

    public String generateReviewChart(List<Product> products) {

        try{
            Map<String, Object> request = Map.of(
                    "products", products.stream().map(p -> Map.of(
                                    "productSource", p.getProductSource(),
                                    "review", p.getReviewCount(),
                                    "title", p.getTitle()
                            ))
                            .collect(Collectors.toList())
            );
            PostRequest postRequest = new PostRequest();
            return postRequest.postRequest(restTemplate, REVIEW_CHART_ENDPOINT, request);
        } catch (Exception e){
            throw new RuntimeException("error calling Python service", e);
        }

    }
}
