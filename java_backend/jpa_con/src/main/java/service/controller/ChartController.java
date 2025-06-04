package service.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import service.pythonService.PythonService;
import service.pythonService.PostRequest;

import java.util.Map;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://127.0.0.1:5500")
public class ChartController {

    private final PythonService pythonService;

    @Autowired
    public ChartController(PythonService pythonService) {
        this.pythonService = pythonService;
    }

    @PostMapping("/price-new")
    public Map<String, String> getPriceNewChart(@RequestBody PostRequest request) {
        return pythonService.getPriceNewChart(request);
    }

    @PostMapping("/price-used")
    public Map<String, String> getPriceUsedChart(@RequestBody PostRequest request) {
        return pythonService.getPriceUsedChart(request);
    }

    @PostMapping("/price-box")
    public Map<String, String> getPriceBoxChart(@RequestBody PostRequest request) {
        return pythonService.getPriceBoxChart(request);
    }

    @PostMapping("/product-data")
    public Map<String, Object> getProductData(@RequestBody PostRequest request) {
        return pythonService.getProductData(request);
    }
}
