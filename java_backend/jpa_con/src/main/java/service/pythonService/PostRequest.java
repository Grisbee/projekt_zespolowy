package service.pythonService;

import lombok.Value;
import org.hibernate.annotations.Comments;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Component
public class PostRequest {


    public String postRequest(RestTemplate restTemplate, String endpoint, Map<String, Object> request) {
        String pythonApiUrl = "http://localhost:8082" + endpoint;


        return restTemplate.postForObject(
                pythonApiUrl,
                request,
                String.class
        );
    }
}
