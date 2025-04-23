package config;

import lombok.Data;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;


@Configuration
//@PropertySource("classpath:application.properties")
@Data
public class DynamicFrontendConfig  {

    @Value("${request.product.list}")
    private String requestProductListEndpoint;

    @Value("${get.intro.produtcs}")
    private String getIntroProductsEndpoint;

}
