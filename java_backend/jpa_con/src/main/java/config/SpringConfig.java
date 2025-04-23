package config;

import lombok.Data;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

@Configuration
@PropertySource("classpath:application.properties")
@Data
public class SpringConfig  {

//
//    @Value("${chart.base.endpoint}")
//    private String chartBaseEndpoint;
//
//    @Value("${chart.price_chart.endpoint}")
//    private String chartPriceEndpoint;
//
//    @Value("${chart.rating_chart.endpoint}")
//    private String chartRatingEndpoint;
//
//    @Value("${chart.review_chart.endpoint}")
//    private String chartReviewEndpoint;

//
//    @Override
//    public String getBaseChartEndpoint() {
//        return chartBaseEndpoint;
//    }
//
//    @Override
//    public String getPriceChartEndpoint() {
//        return chartPriceEndpoint;
//    }
//
//    @Override
//    public String getRatingChartEndpoint() {
//        return chartRatingEndpoint;
//    }
//
//    @Override
//    public String getReviewChartEndpoint() {
//        return chartReviewEndpoint;
//    }

}
