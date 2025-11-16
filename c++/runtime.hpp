#pragma once

#include <string>
#include <vector>
#include <map>
#include <iostream>
#include <stdexcept>
#include <sstream>

// Forward declaration
struct PyValue;

using PyList = std::vector<PyValue>;
using PyDict = std::map<std::string, PyValue>;

struct PyValue {
    enum Type {
        NONE,
        INT,
        FLOAT,
        BOOL,
        STRING,
        LIST,
        DICT
    };

    Type type;

    long long int_value;
    double float_value;
    bool bool_value;
    std::string string_value;
    PyList list_value;
    PyDict dict_value;

    // ----- Constructors -----

    PyValue() : type(NONE),
                int_value(0),
                float_value(0.0),
                bool_value(false) {}

    PyValue(long long v) : type(INT),
                           int_value(v),
                           float_value(0.0),
                           bool_value(false) {}

    PyValue(int v) : type(INT),
                     int_value(v),
                     float_value(0.0),
                     bool_value(false) {}

    PyValue(double v) : type(FLOAT),
                        int_value(0),
                        float_value(v),
                        bool_value(false) {}

    PyValue(bool v) : type(BOOL),
                      int_value(0),
                      float_value(0.0),
                      bool_value(v) {}

    PyValue(const std::string &s) : type(STRING),
                                    int_value(0),
                                    float_value(0.0),
                                    bool_value(false),
                                    string_value(s) {}

    PyValue(const char *s) : type(STRING),
                             int_value(0),
                             float_value(0.0),
                             bool_value(false),
                             string_value(s) {}

    PyValue(const PyList &lst) : type(LIST),
                                 int_value(0),
                                 float_value(0.0),
                                 bool_value(false),
                                 list_value(lst) {}

    PyValue(const PyDict &dict) : type(DICT),
                                  int_value(0),
                                  float_value(0.0),
                                  bool_value(false),
                                  dict_value(dict) {}

    // ----- Helpers -----

    std::string type_name() const {
        switch (type) {
            case NONE:   return "None";
            case INT:    return "int";
            case FLOAT:  return "float";
            case BOOL:   return "bool";
            case STRING: return "str";
            case LIST:   return "list";
            case DICT:   return "dict";
            default:     return "unknown";
        }
    }

    bool is_truthy() const {
        switch (type) {
            case NONE:
                return false;
            case INT:
                return int_value != 0;
            case FLOAT:
                return float_value != 0.0;
            case BOOL:
                return bool_value;
            case STRING:
                return !string_value.empty();
            case LIST:
                return !list_value.empty();
            case DICT:
                return !dict_value.empty();
            default:
                return false;
        }
    }

    std::string to_string() const {
        std::ostringstream oss;

        switch (type) {
            case NONE:
                oss << "None";
                break;
            case INT:
                oss << int_value;
                break;
            case FLOAT:
                oss << float_value;
                break;
            case BOOL:
                oss << (bool_value ? "True" : "False");
                break;
            case STRING:
                oss << string_value;
                break;
            case LIST:
                oss << "[";
                for (std::size_t i = 0; i < list_value.size(); ++i) {
                    if (i > 0) {
                        oss << ", ";
                    }
                    oss << list_value[i].to_string();
                }
                oss << "]";
                break;
            case DICT: {
                oss << "{";
                bool first = true;
                for (const auto &kv : dict_value) {
                    if (!first) {
                        oss << ", ";
                    }
                    first = false;
                    oss << kv.first << ": " << kv.second.to_string();
                }
                oss << "}";
                break;
            }
        }

        return oss.str();
    }
};


// ====================== Printing ======================

inline void py_print(const PyValue &v) {
    std::cout << v.to_string() << std::endl;
}

// Optional: print multiple arguments like Python's print(a, b, c)
inline void py_print_many(const std::vector<PyValue> &args) {
    for (std::size_t i = 0; i < args.size(); ++i) {
        if (i > 0) {
            std::cout << " ";
        }
        std::cout << args[i].to_string();
    }
    std::cout << std::endl;
}


// ====================== Arithmetic helpers ======================

inline double as_double_for_arith(const PyValue &v) {
    if (v.type == PyValue::INT) {
        return static_cast<double>(v.int_value);
    }
    if (v.type == PyValue::FLOAT) {
        return v.float_value;
    }
    throw std::runtime_error("TypeError: expected numeric type, got " + v.type_name());
}

inline long long as_int_for_mod(const PyValue &v) {
    if (v.type == PyValue::INT) {
        return v.int_value;
    }
    throw std::runtime_error("TypeError: expected int for modulus, got " + v.type_name());
}


// a + b
inline PyValue py_add(const PyValue &a, const PyValue &b) {
    // int + int -> int
    if (a.type == PyValue::INT && b.type == PyValue::INT) {
        return PyValue(a.int_value + b.int_value);
    }

    // numeric (int/float) + numeric (int/float) -> float
    if ((a.type == PyValue::INT || a.type == PyValue::FLOAT) &&
        (b.type == PyValue::INT || b.type == PyValue::FLOAT)) {
        double da = as_double_for_arith(a);
        double db = as_double_for_arith(b);
        return PyValue(da + db);
    }

    // str + str -> str
    if (a.type == PyValue::STRING && b.type == PyValue::STRING) {
        return PyValue(a.string_value + b.string_value);
    }

    throw std::runtime_error(
        "TypeError: unsupported operand types for +: '" +
        a.type_name() + "' and '" + b.type_name() + "'");
}

// a - b
inline PyValue py_sub(const PyValue &a, const PyValue &b) {
    // int - int -> int
    if (a.type == PyValue::INT && b.type == PyValue::INT) {
        return PyValue(a.int_value - b.int_value);
    }

    // numeric -> float
    if ((a.type == PyValue::INT || a.type == PyValue::FLOAT) &&
        (b.type == PyValue::INT || b.type == PyValue::FLOAT)) {
        double da = as_double_for_arith(a);
        double db = as_double_for_arith(b);
        return PyValue(da - db);
    }

    throw std::runtime_error(
        "TypeError: unsupported operand types for -: '" +
        a.type_name() + "' and '" + b.type_name() + "'");
}

// a * b
inline PyValue py_mul(const PyValue &a, const PyValue &b) {
    // int * int -> int
    if (a.type == PyValue::INT && b.type == PyValue::INT) {
        return PyValue(a.int_value * b.int_value);
    }

    // numeric -> float
    if ((a.type == PyValue::INT || a.type == PyValue::FLOAT) &&
        (b.type == PyValue::INT || b.type == PyValue::FLOAT)) {
        double da = as_double_for_arith(a);
        double db = as_double_for_arith(b);
        return PyValue(da * db);
    }

    throw std::runtime_error(
        "TypeError: unsupported operand types for *: '" +
        a.type_name() + "' and '" + b.type_name() + "'");
}

// a / b
inline PyValue py_div(const PyValue &a, const PyValue &b) {
    double da = as_double_for_arith(a);
    double db = as_double_for_arith(b);
    if (db == 0.0) {
        throw std::runtime_error("ZeroDivisionError: division by zero");
    }
    return PyValue(da / db);
}

// a % b (integers only)
inline PyValue py_mod(const PyValue &a, const PyValue &b) {
    long long ia = as_int_for_mod(a);
    long long ib = as_int_for_mod(b);
    if (ib == 0) {
        throw std::runtime_error("ZeroDivisionError: integer modulo by zero");
    }
    return PyValue(ia % ib);
}


// ====================== Comparisons ======================

inline PyValue py_eq(const PyValue &a, const PyValue &b) {
    // Same type basic comparison
    if (a.type == b.type) {
        switch (a.type) {
            case PyValue::NONE:
                return PyValue(true);  // None == None
            case PyValue::INT:
                return PyValue(a.int_value == b.int_value);
            case PyValue::FLOAT:
                return PyValue(a.float_value == b.float_value);
            case PyValue::BOOL:
                return PyValue(a.bool_value == b.bool_value);
            case PyValue::STRING:
                return PyValue(a.string_value == b.string_value);
            default:
                // For LIST/DICT we could implement deep compare, but it's not needed now.
                return PyValue(false);
        }
    }

    // int == float or float == int
    if ((a.type == PyValue::INT || a.type == PyValue::FLOAT) &&
        (b.type == PyValue::INT || b.type == PyValue::FLOAT)) {
        double da = as_double_for_arith(a);
        double db = as_double_for_arith(b);
        return PyValue(da == db);
    }

    // Different/unsupported types: treat as not equal
    return PyValue(false);
}

inline PyValue py_ne(const PyValue &a, const PyValue &b) {
    PyValue eq = py_eq(a, b);
    return PyValue(!eq.bool_value);
}

inline PyValue py_lt(const PyValue &a, const PyValue &b) {
    double da = as_double_for_arith(a);
    double db = as_double_for_arith(b);
    return PyValue(da < db);
}

inline PyValue py_le(const PyValue &a, const PyValue &b) {
    double da = as_double_for_arith(a);
    double db = as_double_for_arith(b);
    return PyValue(da <= db);
}

inline PyValue py_gt(const PyValue &a, const PyValue &b) {
    double da = as_double_for_arith(a);
    double db = as_double_for_arith(b);
    return PyValue(da > db);
}

inline PyValue py_ge(const PyValue &a, const PyValue &b) {
    double da = as_double_for_arith(a);
    double db = as_double_for_arith(b);
    return PyValue(da >= db);
}


// ====================== Logical ops (and, or, not) ======================

// Note: arguments already evaluated.
// We only implement truthiness and boolean-like behavior.

inline PyValue py_not(const PyValue &v) {
    return PyValue(!v.is_truthy());
}

inline PyValue py_and(const PyValue &a, const PyValue &b) {
    // Returns first falsy or second
    if (!a.is_truthy()) {
        return a;
    }
    return b;
}

inline PyValue py_or(const PyValue &a, const PyValue &b) {
    // Returns first truthy or second
    if (a.is_truthy()) {
        return a;
    }
    return b;
}
