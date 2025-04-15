package service.controller;

import lombok.Getter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import service.controller.controllerEndpoints.ControllerEndpoints;
import service.entities.Category;
import service.entities.ProductCategory;
import service.repo.CategoryRepo;
import service.repo.ProductCategoryRepo;
import service.repo.ProductRepo;

import java.util.List;
import java.util.stream.Collectors;

@RestController
public class ProductListController {

    @Autowired
    private ProductRepo productRepo;
    @Autowired
    private CategoryRepo categoryRepo;

    @GetMapping(ControllerEndpoints.REQUEST_PRODUCT_LIST)
    public List<String> getCategoryNameList() {
        List<Category> categories = categoryRepo.findAll();
        return categories.stream()
                .map(Category::getCategoryName)
                .collect(Collectors.toList());
    }

//    @PostMapping(ControllerEndpoints.REQUEST_PRODUCT_LIST)
//    public List<String> getCategoryName(){
//
//    }
}
