package service.controller.productCategoryController;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import service.controller.controllerEndpoints.ProductControllerEndpoints;
import service.entities.Category;
import service.entities.Product;
import service.DTO.ProductFilterRequest;
import service.repo.CategoryRepo;
import service.repo.ProductRepo;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping(ProductControllerEndpoints.REQUEST_PRODUCT_LIST)
public class IntroCategoriesAndProductsController {

    @Autowired
    private ProductRepo productRepo;
    @Autowired
    private CategoryRepo categoryRepo;

    @PostMapping(ProductControllerEndpoints.GET_INTRO_PRODUCTS)
    public List<String> getCategoryNameList() {
        List<Category> categories = categoryRepo.findAll();
        return categories.stream()
                .map(Category::getCategoryName)
                .collect(Collectors.toList());
    }

    @PostMapping(ProductControllerEndpoints.GET_PRODUCTS)
    public ResponseEntity<Map<String, Object>> getProducts(@RequestBody ProductFilterRequest request) {
        PageRequest pageable = PageRequest.of(
                request.getPage() - 1,
                request.getLimit(),
                Sort.by("title").ascending()
        );

        Page<Product> productPage;

        if (request.getCategories().isEmpty()) {
            productPage = productRepo.findAllProducts(pageable);
            System.out.println(productPage.getContent());
        } else {
            productPage = productRepo.findProductsByCategoryNames(request.getCategories(), pageable);
        }

        Map<String, Object> response = new HashMap<>();
        response.put("products", productPage.getContent());
        response.put("totalCount", productPage.getTotalElements());
        response.put("totalPages", productPage.getTotalPages());
        return ResponseEntity.ok(response);
    }


}
