package service.pythonService;

import lombok.Value;
import org.hibernate.annotations.Comments;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import service.pythonService.pythonEndpoints.PythonEndpoints;

import java.util.Map;


@Component
public class PostRequest {

    String pythonApiUrl = PythonEndpoints.getPYTHON_API_URL();

    public String postRequest(RestTemplate restTemplate, String endpoint, Map<String, Object> request) {
        String pythonApiUrlWithEndpoint = pythonApiUrl + endpoint;


        return restTemplate.postForObject(
                pythonApiUrlWithEndpoint,
                request,
                String.class
        );
    }
}
