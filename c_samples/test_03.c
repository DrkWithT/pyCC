// test_03.c
// Added by DrkWithT

int maxOfTwo(int a, int b) {
    if (a < b) {
        return b;
    } else {
        return a;
    }
}

int avgTwo(int x, int y) {
    return (x + y) / 2;
}

int main() {
    int something_big = maxOfTwo(420, 69);
    int my_average = avgTwo(21, 63);
    return 0;
}