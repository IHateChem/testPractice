package unit;

public class CafeKioskRunner {
    public static void main(String[] args) {
        CafeKiosk cafeKiosk = new CafeKiosk();
        cafeKiosk.add(new Americano());
        cafeKiosk.add(new Latte());

        int totalPrice = cafeKiosk.caclulateTotalPricae();
        System.out.println("totalPrice = " + totalPrice);
    }
}
