package service.repo;

import service.entities.NewProduct;
import org.springframework.data.jpa.repository.JpaRepository;

public interface NewProductRepo extends JpaRepository<NewProduct, String> {

} 