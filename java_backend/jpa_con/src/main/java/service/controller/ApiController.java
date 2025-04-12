package service.controller;

import service.entities.Product;
import service.repo.CategoryRepo;
import service.repo.ProductCategoryRepo;
import service.repo.ProductRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class ApiController {

    @Autowired
    private ProductRepo productRepo;
    private ProductCategoryRepo productCategoryRepo;
    private CategoryRepo categoryRepo;


    @GetMapping(value = "/")
    public String getPage(){
        return "Hello World";
    }

    @GetMapping(value = "/products")
    public List<Product> getAllProducts(){
        return productRepo.findAll();
    }
}
