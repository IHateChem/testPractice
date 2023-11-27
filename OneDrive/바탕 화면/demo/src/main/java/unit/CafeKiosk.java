package unit;

import lombok.Getter;
import unit.order.Order;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
@Getter
public class CafeKiosk {
    private List<Beverage> beverages = new ArrayList<>();
    public void add(Beverage beverage){
        beverages.add(beverage);

    }
    public void remove(Beverage beverage){
        beverages.remove(beverage);
    }
    public void clear(){
        beverages.clear();
    }

    public int caclulateTotalPricae() {
        return beverages.stream().mapToInt(Beverage::getPrice).sum();
    }

    public Order createOrder(){
        return new Order(LocalDateTime.now(), beverages);
    }
}
