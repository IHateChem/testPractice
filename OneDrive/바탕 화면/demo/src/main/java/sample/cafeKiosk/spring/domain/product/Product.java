package sample.cafeKiosk.spring.domain.product;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import sample.cafeKiosk.spring.domain.BaseEntity;

@Entity
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Product extends BaseEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String productNumber;
    @Builder
    private Product(String productNumber, ProductType type, ProductSellingStatus sellingStatus, String name, int price) {
        this.productNumber = productNumber;
        this.type = type;
        this.sellingStatus = sellingStatus;
        this.name = name;
        this.price = price;
    }

    @Enumerated(EnumType.STRING)
    @Column(name = "type")
    private ProductType type;
    @Enumerated(EnumType.STRING)
    @Column(name = "selling_status")
    private ProductSellingStatus sellingStatus;

    private String name;
    private int price;

}
