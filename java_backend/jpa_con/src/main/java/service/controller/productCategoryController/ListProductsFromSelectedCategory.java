package service.controller.productCategoryController;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import service.DTO.SearchRequest;
import service.controller.controllerEndpoints.ProductControllerEndpoints;
import service.entities.Product;
import service.repo.ProductRepo;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping(ProductControllerEndpoints.REQUEST_PRODUCT_LIST)
public class ListProductsFromSelectedCategory {
    @Autowired
    ProductRepo productRepo;

    @PostMapping(ProductControllerEndpoints.GET_PRODUCTS_FROM_SELECTED_CATEGORY)
    public ResponseEntity<Map<String, Object>> getProductsFromSelectedCategory(@RequestBody SearchRequest request) {
        PageRequest pageable = PageRequest.of(
                request.getPage(),
                request.getLimit(),
                Sort.by("title").ascending()
        );


        System.out.println("Получен запрос: " + request);


        Page<Product> productList = productRepo.searchProductsByKey(request.getQuery(), pageable);

        Map<String, Object> response = new HashMap<>();
        response.put("products", productList.getContent());
        response.put("totalCount", productList.getTotalElements());
        response.put("totalPages", productList.getTotalPages());
        return ResponseEntity.ok(response);
    }
}
