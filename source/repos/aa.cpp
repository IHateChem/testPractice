#include <stdio.h>

int main() {

    int a;
    int b;
    scanf("%d", &a);
    scanf("%d", &b);
    int partition;
    if (a < 0) {
        partition = 2;
    }
    else {
        partition = 1;
    }
    if (b < 0) {
        partition = partition + 4;
    }
    partitiion = partition % 4
        printf();
    return 0;

}