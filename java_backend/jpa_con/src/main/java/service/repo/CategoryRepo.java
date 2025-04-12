package service.repo;

import service.entities.Category;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface CategoryRepo extends JpaRepository<Category, UUID> {
    List<Category> findByCategoryName(String categoryName);
}
