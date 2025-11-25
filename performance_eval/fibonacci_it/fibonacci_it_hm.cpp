#include <iostream>
#include <vector>
#include <chrono>
#include <string>

using namespace std::chrono;
using namespace std;

int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    int a = 0;
    int b = 1;
    for (int i = 0; i < n-1; i++) {
        int t = a + b;
        a = b;
        b = t;
    }
    return b;
}

int main() {

    vector<string> t_list;
    for(int i = 1; i <= 50; i++) {
        auto t1 = high_resolution_clock::now();

        cout << "Fibonacci(" << i << "): " << fibonacci(i) << "\n";

        auto t2 = high_resolution_clock::now();
        duration<double> d = t2 - t1;
        string time = std::to_string(d.count());
        // Replace '.' with ',':
        for (char &c : time) {
            if (c == '.') c = ',';
        }
        t_list.push_back(time);
    }
    for(int i = 0; i < 50; i++) {
        cout << t_list.at(i) << "\n";
    }
    return 0;
}
