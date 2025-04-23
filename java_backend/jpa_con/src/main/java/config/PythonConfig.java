package config;


import lombok.Data;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

@Configuration
//@PropertySource("classpath:application.properties")
@Data
public class PythonConfig  {

    @Value("${python.api.url}")
    private String pythonApiUrl;

    @Value("${python.api.generate.chart.url}")
    private String pythonApiGenerateChartUrl;

    @Value("${python.review.chart.endpoint}")
    private String pythonReviewChartEndpoint;

    @Value("${python.price.chart.endpoint}")
    private String pythonPriceChartEndpoint;

    @Value("${python.rating.chart.endpoint}")
    private String PythonRatingChartEndpoint;

//
//    @Override
//    public String getPythonPriceChartEndpoint() {
//        return pythonPriceChartEndpoint;
//    }
//
//    @Override
//    public String getPythonRatingChartEndpoint() {
//        return PythonRatingChartEndpoint;
//    }
//
//    @Override
//    public String getPythonReviewChartEndpoint() {
//        return pythonReviewChartEndpoint;
//    }
//
//    @Override
//    public String getPythonApiUrl() {
//        return pythonApiUrl;
//    }
//
//    @Override
//    public String getPythonApiGenerateChartUrl() {
//        return pythonApiGenerateChartUrl;
//    }
}
