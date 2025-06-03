package service.controller;

import service.entities.Product;
import service.repo.CategoryRepo;
import service.repo.ProductCategoryRepo;
import service.repo.ProductRepo;
import service.entities.NewProduct;
import service.repo.NewProductRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.CrossOrigin;

import java.util.List;

@RestController
@CrossOrigin(origins = "http://127.0.0.1:5500")
public class ApiController {

    @Autowired
    private ProductRepo productRepo;

    @Autowired
    private NewProductRepo newProductRepo;

    private ProductCategoryRepo productCategoryRepo;
    private CategoryRepo categoryRepo;

    @GetMapping(value = "/")
    public String getPage(){
        return "Hello World";
    }

    @GetMapping(value = "/products")
    public List<NewProduct> getAllProducts(){
        return newProductRepo.findAll();
    }
}
