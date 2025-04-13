package service.pythonService.pythonEndpoints;

import lombok.Getter;

public class PythonEndpoints {
    @Getter
    private static final String PYTHON_PRICE_CHART_ENDPOINT = "/python-price-chart";
    @Getter
    private static final String PYTHON_RATING_CHART_ENDPOINT = "/python-rating-chart";
    @Getter
    private static final String PYTHON_REVIEW_CHART_ENDPOINT = "/python-review-chart";

    @Getter
    private static final String PYTHON_API_URL = "http://localhost:8082";
}
