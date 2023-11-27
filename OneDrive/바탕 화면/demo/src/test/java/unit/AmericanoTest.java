package unit;

import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class AmericanoTest {

    @Test
    void getPrice() {
        Americano americano = new Americano();
        Assertions.assertThat(americano.getName()).isEqualTo("Americano");
    }

    @Test
    void getName() {
        Americano americano = new Americano();
        Assertions.assertThat(americano.getPrice()).isEqualTo(4000);
    }
}