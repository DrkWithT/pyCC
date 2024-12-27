// test_logical_01.c

int main() {
    int a = 10;
    int b = 20;

    if (a != b && b != a) {
        return 0;
    }

    return 1;
}