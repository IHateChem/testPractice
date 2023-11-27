package unit.order;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import unit.Beverage;

import java.time.LocalDateTime;
import java.util.List;

@Getter @Setter @RequiredArgsConstructor
public class Order {
    private final LocalDateTime dateTime;
    private final List<Beverage> beverages;
}
