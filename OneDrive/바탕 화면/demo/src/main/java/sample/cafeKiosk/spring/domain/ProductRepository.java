package sample.cafeKiosk.spring.domain;

import org.springframework.data.jpa.repository.JpaRepository;
import sample.cafeKiosk.spring.domain.product.Product;
import sample.cafeKiosk.spring.domain.product.ProductSellingStatus;

import java.util.List;

public interface ProductRepository extends JpaRepository<Product, Long> {
    List<Product> findAllBySellingStatusIn(List<ProductSellingStatus> sellingStatuses);
}
