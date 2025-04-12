package service.repo;

import service.entities.ProductCategory;
import service.entities.ProductCategoryId;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface ProductCategoryRepo extends JpaRepository<ProductCategory, ProductCategoryId> {

    List<ProductCategory> findByProduct_ProductId(Long product_id);
    List<ProductCategory> findByCategory_CategoryId(UUID categoryId);

}
