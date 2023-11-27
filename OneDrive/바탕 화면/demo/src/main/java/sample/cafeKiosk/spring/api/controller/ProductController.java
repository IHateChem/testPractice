package sample.cafeKiosk.spring.api.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import sample.cafeKiosk.spring.api.service.product.ProductResponse;
import sample.cafeKiosk.spring.api.service.product.ProductService;

import java.util.List;

@RestController
@RequiredArgsConstructor
public class ProductController {
    private final ProductService productService;
    @GetMapping("/api/v1/products/selling")
    public List<ProductResponse> getSellingProduct(){
        return productService.getSellingProducts();
    }
}
