// c++/test_runtime.cpp
#include "runtime.hpp"

int main() {
    // ----- cambio de tipo en la misma variable -----
    PyValue a = 4;              // int
    py_print(a);                // 4

    PyValue b = 5;              // int
    PyValue c = py_add(a, b);   // 4 + 5 = 9
    py_print(c);                // 9

    a = std::string("hola");    // ahora a es str
    py_print(a);                // hola

    // ----- listas -----
    PyList lst;
    lst.push_back(PyValue(1));
    lst.push_back(PyValue(std::string("mundo")));
    lst.push_back(PyValue(true));

    PyValue vlist(lst);
    py_print(vlist);            // [1, mundo, True]

    // ----- comparación y truthiness -----
    PyValue cond = py_lt(PyValue(3), PyValue(10));  // 3 < 10
    if (cond.bool_value) {      // cond es un PyValue BOOL
        py_print(std::string("3 is less than 10"));
    }

    // ----- operación que debería fallar (int + str) -----
    try {
        PyValue bad = py_add(PyValue(1), PyValue(std::string("x")));
        py_print(bad);
    } catch (const std::exception &ex) {
        std::cout << "Caught error: " << ex.what() << std::endl;
    }

    return 0;
}
