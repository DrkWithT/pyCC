// test_bad_03.c

void foo() {
    // nothing here to see!
}

int bar() {
    return 42;
}

int main() {
    int blah = foo() + 1;
    int two_bars = bar() + bar();
    return 0;
}