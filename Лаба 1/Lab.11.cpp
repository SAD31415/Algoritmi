#include <iostream>
#include <list>
#include <vector>
#include <chrono>
#include <utility>

bool fill_list(std::list<int>& l, int count) {
    for (int i = 0; i < count; ++i) {
        l.push_back(i); 
    }
    return true;
}

template <typename Func, typename... Args>
auto measure_execution_time(Func&& func, Args&&... args) {
    auto start_time = std::chrono::high_resolution_clock::now();
    auto result = func(std::forward<Args>(args)...);
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);
    return std::make_pair(result, duration.count());
}

int main() {
    setlocale(LC_ALL, "Russian");
    std::vector<int> sizes = { 10, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000 };
    for (int n : sizes) {
        std::list<int> my_list;
        auto [success, time] = measure_execution_time(fill_list, my_list, n);
        std::cout << "Количество элементов: " << n
            << " | Время выполнения: " << time << " мкс" << std::endl;
    }

    return 0;
}
