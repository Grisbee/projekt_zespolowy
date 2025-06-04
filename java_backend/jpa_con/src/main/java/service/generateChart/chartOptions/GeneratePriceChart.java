//package service.generateChart.chartOptions;
//
//import org.springframework.stereotype.Service;
//import org.springframework.web.client.RestTemplate;
//// import service.entities.Product; // Usuń import starej encji Product
//import service.entities.NewProduct; // Importuj nową encję NewProduct
//import service.pythonService.PostRequest;
//import service.pythonService.PythonService;
//import service.pythonService.pythonEndpoints.PythonEndpoints;
//
//import java.util.List;
//import java.util.Map;
//import java.util.stream.Collectors;
//import java.util.Optional; // Importuj Optional
//
//@Service
//public class GeneratePriceChart {
//    private final RestTemplate restTemplate;
//
//    private static final String PRICE_CHART_ENDPOINT = PythonEndpoints.getPYTHON_PRICE_CHART_ENDPOINT();
//
//    public GeneratePriceChart(PythonService pythonService) {
//        this.restTemplate = pythonService.getRestTemplate();
//    }
//
//    // Zmień parametr wejściowy na List<NewProduct>
//    public String generatePriceChart(List<NewProduct> products) {
//
//        try{
//            Map<String, Object> request = Map.of(
//                    "products", products.stream().map(p -> {
//                        String title = Optional.ofNullable(p.getAmazonTitle())
//                                .orElseGet(() -> Optional.ofNullable(p.getKeepaName()).orElse("")); // Użyj pustego stringa jeśli oba są null
//                        Integer priceNew = Optional.ofNullable(p.getPriceNew()).orElse(0); // Obsłuż null dla priceNew, użyj 0 jako domyślne
//
//                        return Map.of(
//                                "productSource", Optional.ofNullable(p.getProductSrc()).orElse(""),
//                                "price", priceNew, // Użyj zmiennej priceNew, która nie powinna być null
//                                "title", title // Użyj zmiennej title, która nie powinna być null
//                        );
//                    })
//                            .collect(Collectors.toList())
//            );
//            PostRequest postRequest = new PostRequest();
//            return postRequest.postRequest(restTemplate, PRICE_CHART_ENDPOINT, request);
//        } catch (Exception e){
//            throw new RuntimeException("error calling Python service", e);
//        }
//
//    }
//}
