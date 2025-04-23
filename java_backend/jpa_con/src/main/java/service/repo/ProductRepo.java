package service.repo;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import service.entities.Product;

import java.util.List;

public interface ProductRepo extends JpaRepository<Product, Long> {

    @Query("SELECT p FROM Product p")
    Page<Product> findAllProducts(Pageable pageable);

    @Query("SELECT DISTINCT p FROM Product p " +
            "JOIN ProductCategory pc ON p.productId = pc.id.productId " +
            "JOIN Category c ON pc.id.categoryId = c.categoryId " +
            "WHERE c.categoryName IN :categories")
    Page<Product> findProductsByCategoryNames(@Param("categories") List<String> categoryNames, Pageable pageable);

    @Query("SELECT COUNT(DISTINCT p ) FROM Product p " +
            "JOIN ProductCategory pc ON p.productId = pc.id.productId " +
            "JOIN Category c ON pc.id.categoryId = c.categoryId " +
            "WHERE c.categoryName IN :categories")
    long countByCategoryNames(@Param("categories") List<String> categories);


    @Query("SELECT p FROM Product p WHERE LOWER(p.title) LIKE LOWER(CONCAT('%', :query, '%'))")
        //przeszukiwanie klucza w całym tytule
    Page<Product> searchProductsByKey(@Param("query") String query, Pageable pageable);

}

