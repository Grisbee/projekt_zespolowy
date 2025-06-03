package service.entities;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "Product") // Mapowanie na nową tabelę Product
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class NewProduct {

    @Id
    @Column(name = "keepa_name")
    private String keepaName;

    @Column(name = "amazon_title", columnDefinition = "TEXT")
    private String amazonTitle;

    @Column(name = "link_keepa", columnDefinition = "TEXT")
    private String linkKeepa;

    @Column(name = "link_amazon", columnDefinition = "TEXT")
    private String linkAmazon;

    @Column(name = "chart_url", columnDefinition = "TEXT")
    private String chartUrl;

    @Column(name = "price_box")
    private Integer priceBox;

    @Column(name = "price_new")
    private Integer priceNew;

    @Column(name = "price_used")
    private Integer priceUsed;

    @Column(name = "product_category", length = 255)
    private String productCategory;

    @Column(name = "rating", length = 10)
    private String rating;

    @Column(name = "review_count", length = 20)
    private String reviewCount;

    @Column(name = "currency", length = 3)
    private String currency;

    @Column(name = "product_src", length = 50)
    private String productSrc;

    // Możemy dodać relację do SimilarProducts później, jeśli będzie potrzebna
} 