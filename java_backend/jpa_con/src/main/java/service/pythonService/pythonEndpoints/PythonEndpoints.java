package service.pythonService.pythonEndpoints;

import lombok.Getter;

public class PythonEndpoints {
    @Getter
    private static final String PYTHON_PRICE_NEW_ENDPOINT = "/python-price-new";
    @Getter
    private static final String PYTHON_PRICE_USED_ENDPOINT = "/python-price-used";
    @Getter
    private static final String PYTHON_PRICE_BOX_ENDPOINT = "/python-price-box";
    @Getter
    private static final String PYTHON_PRODUCT_DATA_ENDPOINT = "/python-product-data";

    @Getter
    private static final String PYTHON_API_URL = "http://localhost:8082";
}
