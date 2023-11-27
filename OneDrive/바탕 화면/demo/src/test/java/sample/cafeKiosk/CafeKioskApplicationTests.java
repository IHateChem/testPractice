package sample.cafeKiosk;

import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import unit.Americano;
import unit.CafeKiosk;


class CafeKioskApplicationTests {
	@Test
	void add(){
		CafeKiosk cafeKiosk =  new CafeKiosk();
		cafeKiosk.add(new Americano());
		Assertions.assertThat(cafeKiosk.getBeverages()).hasSize(1);
		Assertions.assertThat(cafeKiosk.getBeverages().get(0).getName()).isEqualTo("Americano");
	}

	@Test
	void contextLoads() {
	}

}
