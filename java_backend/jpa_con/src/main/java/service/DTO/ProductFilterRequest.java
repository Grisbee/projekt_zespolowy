package service.DTO;

import lombok.Data;

import java.util.Collections;
import java.util.List;

@Data
public class ProductFilterRequest {
    private int page;
    private int limit ;
    private List<String> categories = Collections.emptyList();
}
