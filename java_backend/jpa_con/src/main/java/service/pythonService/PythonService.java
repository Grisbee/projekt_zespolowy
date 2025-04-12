package service.pythonService;

import lombok.Getter;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class PythonService {

    @Getter
    private final RestTemplate restTemplate;

    public PythonService(RestTemplateBuilder restTemplateBuilder) {
        this.restTemplate = restTemplateBuilder
                .rootUri("http://localhost:8082")
                .build();
    }
}
