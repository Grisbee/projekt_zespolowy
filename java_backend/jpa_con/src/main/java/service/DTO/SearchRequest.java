package service.DTO;

import lombok.Data;

@Data
public class SearchRequest {
    private String query;
    private int page;
    private int limit;
}
