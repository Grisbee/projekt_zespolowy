package service.pythonService;

import lombok.Getter;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import service.pythonService.pythonEndpoints.PythonEndpoints;

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
}
