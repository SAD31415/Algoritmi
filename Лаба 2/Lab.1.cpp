#include <iostream>
#include <cmath>
#include <iomanip>

double function(double x) {
    return (x * x * x) + (x * x) + 20.0;
}

double simpson_rule(double (*f)(double), double a, double b, int n) {
    if (n % 2 == 1) n++;
    double h = (b - a) / n;
    double sum = f(a) + f(b);
    for (int i = 1; i < n; i += 2) {
        sum += 4 * f(a + i * h);
    }
    for (int i = 2; i < n; i += 2) {
        sum += 2 * f(a + i * h);
    }
    return (h / 3) * sum;
}

int main() {
    double a = -3.079596;
    double b = 2.0;

    std::cout << std::setprecision(6) << std::fixed;

    int test_cases[] = { 2, 4, 10, 20, 50, 100 };
    for (int n : test_cases) {
        double result = simpson_rule(function, a, b, n);
        std::cout << n << "\t" << b << "\t" << result << "\n";
    }
    return 0;
}
