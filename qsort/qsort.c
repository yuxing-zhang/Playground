#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void swap(int* a, int* b) {
    int t = *a;
    *a = *b;
    *b = t;
}

void qs(int *arry, int n) {
    if (n <= 1) { return; }
    int i = 1, j = n-1;
    while (1) {
        while (i < n && arry[i] <= arry[0]) {i++;}
        while (j > 0 && arry[j] >= arry[0]) {j--;}
        if (i > j) { break; }
        swap(arry+i, arry+j);
    }
    swap(arry, arry+j);
    qs(arry, j);
    qs(arry+i, n-i);
}


int main() {
    int arry[10];
    srand(time(0));
    for (int i = 0; i < 10; i++) {
        arry[i] = rand() % 100;
    }
    qs(arry, 10);
    for (int i = 0; i < 10; i++) {
        printf("%d ", arry[i]);
    }
    putchar('\n');
}	
