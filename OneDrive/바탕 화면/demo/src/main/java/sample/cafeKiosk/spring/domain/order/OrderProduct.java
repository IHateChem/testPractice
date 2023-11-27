package sample.cafeKiosk.spring.domain.order;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;
import sample.cafeKiosk.spring.domain.BaseEntity;
import sample.cafeKiosk.spring.domain.product.Product;

@Entity
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class OrderProduct  extends BaseEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    private Order order;

    public OrderProduct(Order order, Product product) {
        this.order = order;
        this.product = product;
    }

    @ManyToOne
    private Product product;
}
