package service.pythonService;

import lombok.Getter;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import service.pythonService.pythonEndpoints.PythonEndpoints;
import service.pythonService.PostRequest;

import java.util.Map;

@Service
public class PythonService {

    @Getter
    private final RestTemplate restTemplate;

    String pythonApiUrl = PythonEndpoints.getPYTHON_API_URL();

    public PythonService(RestTemplateBuilder restTemplateBuilder) {
        this.restTemplate = restTemplateBuilder
                .rootUri(pythonApiUrl)
                .build();
    }

    public Map<String, String> getPriceNewChart(PostRequest request) {
        return restTemplate.postForObject(
            PythonEndpoints.getPYTHON_PRICE_NEW_ENDPOINT(),
            request,
            Map.class
        );
    }

    public Map<String, String> getPriceUsedChart(PostRequest request) {
        return restTemplate.postForObject(
            PythonEndpoints.getPYTHON_PRICE_USED_ENDPOINT(),
            request,
            Map.class
        );
    }

    public Map<String, String> getPriceBoxChart(PostRequest request) {
        return restTemplate.postForObject(
            PythonEndpoints.getPYTHON_PRICE_BOX_ENDPOINT(),
            request,
            Map.class
        );
    }

    public Map<String, Object> getProductData(PostRequest request) {
        return restTemplate.postForObject(
            PythonEndpoints.getPYTHON_PRODUCT_DATA_ENDPOINT(),
            request,
            Map.class
        );
    }
}
