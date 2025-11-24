#pragma once

#include <string>
#include <vector>
#include <map>
#include <unordered_map>
#include <iostream>
#include <stdexcept>
#include <sstream>

// Forward declaration
struct PyValue;

using PyList  = std::vector<PyValue>;
using PyDict  = std::map<std::string, PyValue>;
using PyTuple = std::vector<PyValue>;
using PySet   = std::unordered_map<std::string, PyValue>;

struct PyValue {
    enum Type {
        NONE,
        INT,
        FLOAT,
        BOOL,
        STRING,
        LIST,
        DICT,
        TUPLE,
        SET
    };

    Type type;

    long long     int_value;
    double        float_value;
    bool          bool_value;
    std::string   string_value;
    PyList        list_value;
    PyDict        dict_value;
    PyTuple       tuple_value;
    PySet         set_value;

    // ----- Constructors -----

    PyValue()
        : type(NONE),
          int_value(0),
          float_value(0.0),
          bool_value(false) {}

    PyValue(long long v)
        : type(INT),
          int_value(v),
          float_value(0.0),
          bool_value(false) {}

    PyValue(int v)
        : type(INT),
          int_value(v),
          float_value(0.0),
          bool_value(false) {}

    PyValue(double v)
        : type(FLOAT),
          int_value(0),
          float_value(v),
          bool_value(false) {}

    PyValue(bool v)
        : type(BOOL),
          int_value(0),
          float_value(0.0),
          bool_value(v) {}

    PyValue(const std::string& s)
        : type(STRING),
          int_value(0),
          float_value(0.0),
          bool_value(false),
          string_value(s) {}

    PyValue(const char* s)
        : type(STRING),
          int_value(0),
          float_value(0.0),
          bool_value(false),
          string_value(s) {}

    PyValue(const PyList& lst)
        : type(LIST),
          int_value(0),
          float_value(0.0),
          bool_value(false),
          list_value(lst) {}

    PyValue(const PyDict& dict)
        : type(DICT),
          int_value(0),
          float_value(0.0),
          bool_value(false),
          dict_value(dict) {}

    // We build TUPLE and SET via helper functions (py_tuple, py_set_from_list).

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
            case TUPLE:  return "tuple";
            case SET:    return "set";
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
            case TUPLE:
                return !tuple_value.empty();
            case SET:
                return !set_value.empty();
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
            case LIST: {
                oss << "[";
                for (std::size_t i = 0; i < list_value.size(); ++i) {
                    if (i > 0) {
                        oss << ", ";
                    }
                    oss << list_value[i].to_string();
                }
                oss << "]";
                break;
            }
            case DICT: {
                oss << "{";
                bool first = true;
                for (const auto& kv : dict_value) {
                    if (!first) {
                        oss << ", ";
                    }
                    first = false;
                    oss << kv.first << ": " << kv.second.to_string();
                }
                oss << "}";
                break;
            }
            case TUPLE: {
                oss << "(";
                for (std::size_t i = 0; i < tuple_value.size(); ++i) {
                    if (i > 0) {
                        oss << ", ";
                    }
                    oss << tuple_value[i].to_string();
                }
                // Single-element tuple: add trailing comma
                if (tuple_value.size() == 1) {
                    oss << ",";
                }
                oss << ")";
                break;
            }
            case SET: {
                oss << "{";
                bool first = true;
                for (const auto& kv : set_value) {
                    if (!first) {
                        oss << ", ";
                    }
                    first = false;
                    oss << kv.second.to_string();
                }
                oss << "}";
                break;
            }
        }

        return oss.str();
    }
};


// ====================== Printing ======================

inline void py_print(const PyValue& v) {
    std::cout << v.to_string() << std::endl;
}

inline void py_print_many(const std::vector<PyValue>& args) {
    for (std::size_t i = 0; i < args.size(); ++i) {
        if (i > 0) {
            std::cout << " ";
        }
        std::cout << args[i].to_string();
    }
    std::cout << std::endl;
}


// ====================== Arithmetic helpers ======================

inline double as_double_for_arith(const PyValue& v) {
    if (v.type == PyValue::INT) {
        return static_cast<double>(v.int_value);
    }
    if (v.type == PyValue::FLOAT) {
        return v.float_value;
    }
    throw std::runtime_error("TypeError: expected numeric type, got " + v.type_name());
}

inline long long as_int_for_mod(const PyValue& v) {
    if (v.type == PyValue::INT) {
        return v.int_value;
    }
    throw std::runtime_error("TypeError: expected int for modulus, got " + v.type_name());
}


// a + b
inline PyValue py_add(const PyValue& a, const PyValue& b) {
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
        a.type_name() + "' and '" + b.type_name() + "'"
    );
}

// a - b
inline PyValue py_sub(const PyValue& a, const PyValue& b) {
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
        a.type_name() + "' and '" + b.type_name() + "'"
    );
}

// a * b
inline PyValue py_mul(const PyValue& a, const PyValue& b) {
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
        a.type_name() + "' and '" + b.type_name() + "'"
    );
}

// a / b
inline PyValue py_div(const PyValue& a, const PyValue& b) {
    double da = as_double_for_arith(a);
    double db = as_double_for_arith(b);
    if (db == 0.0) {
        throw std::runtime_error("ZeroDivisionError: division by zero");
    }
    return PyValue(da / db);
}

// a % b (integers only)
inline PyValue py_mod(const PyValue& a, const PyValue& b) {
    long long ia = as_int_for_mod(a);
    long long ib = as_int_for_mod(b);
    if (ib == 0) {
        throw std::runtime_error("ZeroDivisionError: integer modulo by zero");
    }
    return PyValue(ia % ib);
}


// ====================== Comparisons ======================

inline PyValue py_eq(const PyValue& a, const PyValue& b) {
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
                // For LIST/DICT/TUPLE/SET we skip deep compare for now.
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

inline PyValue py_ne(const PyValue& a, const PyValue& b) {
    PyValue eq = py_eq(a, b);
    return PyValue(!eq.bool_value);
}

inline PyValue py_lt(const PyValue& a, const PyValue& b) {
    double da = as_double_for_arith(a);
    double db = as_double_for_arith(b);
    return PyValue(da < db);
}

inline PyValue py_le(const PyValue& a, const PyValue& b) {
    double da = as_double_for_arith(a);
    double db = as_double_for_arith(b);
    return PyValue(da <= db);
}

inline PyValue py_gt(const PyValue& a, const PyValue& b) {
    double da = as_double_for_arith(a);
    double db = as_double_for_arith(b);
    return PyValue(da > db);
}

inline PyValue py_ge(const PyValue& a, const PyValue& b) {
    double da = as_double_for_arith(a);
    double db = as_double_for_arith(b);
    return PyValue(da >= db);
}


// ====================== Logical ops (and, or, not) ======================

inline PyValue py_not(const PyValue& v) {
    return PyValue(!v.is_truthy());
}

inline PyValue py_and(const PyValue& a, const PyValue& b) {
    // Return first falsy or second
    if (!a.is_truthy()) {
        return a;
    }
    return b;
}

inline PyValue py_or(const PyValue& a, const PyValue& b) {
    // Return first truthy or second
    if (a.is_truthy()) {
        return a;
    }
    return b;
}


// ====================== Builtins: str() and len() ======================

inline PyValue py_str(const PyValue& v) {
    return PyValue(v.to_string());
}

inline PyValue py_len(const PyValue& v) {
    switch (v.type) {
        case PyValue::STRING:
            return PyValue(static_cast<long long>(v.string_value.size()));
        case PyValue::LIST:
            return PyValue(static_cast<long long>(v.list_value.size()));
        case PyValue::DICT:
            return PyValue(static_cast<long long>(v.dict_value.size()));
        case PyValue::TUPLE:
            return PyValue(static_cast<long long>(v.tuple_value.size()));
        case PyValue::SET:
            return PyValue(static_cast<long long>(v.set_value.size()));
        default:
            throw std::runtime_error(
                "TypeError: object of type '" + v.type_name() + "' has no len()"
            );
    }
}


// ====================== Containers: list, dict, tuple, set ======================

// Build a list from items.
inline PyValue py_list(const std::vector<PyValue>& items) {
    return PyValue(items);
}

// Build a dict from (key, value) pairs; keys use to_string().
inline PyValue py_dict(const std::vector<std::pair<PyValue, PyValue>>& items) {
    PyDict dict;

    for (const auto& kv : items) {
        const PyValue& k = kv.first;
        const PyValue& v = kv.second;
        std::string key_str = k.to_string();
        dict[key_str] = v;
    }

    return PyValue(dict);
}

// Build a tuple from items.
inline PyValue py_tuple(const std::vector<PyValue>& items) {
    PyValue v;
    v.type        = PyValue::TUPLE;
    v.int_value   = 0;
    v.float_value = 0.0;
    v.bool_value  = false;
    v.tuple_value = items;
    return v;
}

// Build a set from a list/tuple (used for set(...) builtin).
inline PyValue py_set_from_list(const PyValue& iterable) {
    if (iterable.type != PyValue::LIST && iterable.type != PyValue::TUPLE) {
        throw std::runtime_error(
            "TypeError: set() expects a list or tuple"
        );
    }

    PyValue v;
    v.type        = PyValue::SET;
    v.int_value   = 0;
    v.float_value = 0.0;
    v.bool_value  = false;

    if (iterable.type == PyValue::LIST) {
        for (const auto& item : iterable.list_value) {
            std::string key_str = item.to_string();
            v.set_value[key_str] = item;
        }
    } else { // TUPLE
        for (const auto& item : iterable.tuple_value) {
            std::string key_str = item.to_string();
            v.set_value[key_str] = item;
        }
    }

    return v;
}


// Implements Python-like indexing: value[index].
inline PyValue py_getitem(const PyValue& container, const PyValue& index) {
    // list[index]
    if (container.type == PyValue::LIST) {
        if (index.type != PyValue::INT) {
            throw std::runtime_error("TypeError: list indices must be integers");
        }
        long long i = index.int_value;
        if (i < 0 || i >= static_cast<long long>(container.list_value.size())) {
            throw std::runtime_error("IndexError: list index out of range");
        }
        return container.list_value[static_cast<std::size_t>(i)];
    }

    // tuple[index]
    if (container.type == PyValue::TUPLE) {
        if (index.type != PyValue::INT) {
            throw std::runtime_error("TypeError: tuple indices must be integers");
        }
        long long i = index.int_value;
        if (i < 0 || i >= static_cast<long long>(container.tuple_value.size())) {
            throw std::runtime_error("IndexError: tuple index out of range");
        }
        return container.tuple_value[static_cast<std::size_t>(i)];
    }

    // string[index]  -> a 1-character string
    if (container.type == PyValue::STRING) {
        if (index.type != PyValue::INT) {
            throw std::runtime_error("TypeError: string indices must be integers");
        }
        long long i = index.int_value;
        if (i < 0 || i >= static_cast<long long>(container.string_value.size())) {
            throw std::runtime_error("IndexError: string index out of range");
        }
        char c = container.string_value[static_cast<std::size_t>(i)];
        return PyValue(std::string(1, c));
    }

    // dict[key]
    if (container.type == PyValue::DICT) {
        std::string key_str;

        if (index.type == PyValue::STRING) {
            key_str = index.string_value;
        } else {
            key_str = index.to_string();
        }

        auto it = container.dict_value.find(key_str);
        if (it == container.dict_value.end()) {
            throw std::runtime_error("KeyError: key not found: " + key_str);
        }
        return it->second;
    }

    // set is not subscriptable
    if (container.type == PyValue::SET) {
        throw std::runtime_error(
            "TypeError: 'set' object is not subscriptable"
        );
    }

    // Not subscriptable
    throw std::runtime_error(
        "TypeError: object of type '" + container.type_name() + "' is not subscriptable"
    );
}


// ====================== List helpers (methods) ======================

// list.append(x) -> mutates list, returns None.
inline PyValue py_list_append(PyValue& list, const PyValue& item) {
    if (list.type != PyValue::LIST) {
        throw std::runtime_error("TypeError: append() only valid on list");
    }
    list.list_value.push_back(item);
    return PyValue();  // None
}

// list.sublist(start, end) -> returns new list with slice [start, end).
inline PyValue py_list_sublist(const PyValue& list,
                               const PyValue& start,
                               const PyValue& end) {
    if (list.type != PyValue::LIST) {
        throw std::runtime_error("TypeError: sublist() only valid on list");
    }
    if (start.type != PyValue::INT || end.type != PyValue::INT) {
        throw std::runtime_error("TypeError: sublist indices must be integers");
    }

    long long s = start.int_value;
    long long e = end.int_value;
    if (s < 0) s = 0;
    if (e < s) e = s;

    PyList result;
    for (long long i = s; i < e && i < (long long)list.list_value.size(); ++i) {
        result.push_back(list.list_value[(std::size_t)i]);
    }
    return PyValue(result);
}


// ====================== Dict / Set helpers (methods) ======================

// dict.add(key, value) or set.add(value)
// Mutates container, returns None.
inline PyValue py_dict_or_set_add(PyValue& container,
                                  const PyValue& key_or_value) {
    // Used for set.add(value)
    if (container.type != PyValue::SET) {
        throw std::runtime_error("TypeError: single-arg add() only valid on set");
    }

    std::string key_str = key_or_value.to_string();
    container.set_value[key_str] = key_or_value;
    return PyValue();  // None
}

inline PyValue py_dict_or_set_add(PyValue& container,
                                  const PyValue& key,
                                  const PyValue& value) {
    // Used for dict.add(key, value)
    if (container.type != PyValue::DICT) {
        throw std::runtime_error("TypeError: two-arg add() only valid on dict");
    }

    std::string key_str = key.to_string();
    container.dict_value[key_str] = value;
    return PyValue();  // None
}

// dict.get(key) -> value or None (if not found)
// set.get(value) -> True/False (membership)
inline PyValue py_dict_or_set_get(const PyValue& container,
                                  const PyValue& key_or_value) {
    if (container.type == PyValue::DICT) {
        std::string key_str = key_or_value.to_string();
        auto it = container.dict_value.find(key_str);
        if (it == container.dict_value.end()) {
            // Python's dict.get() returns None if missing.
            return PyValue();
        }
        return it->second;
    }

    if (container.type == PyValue::SET) {
        std::string key_str = key_or_value.to_string();
        auto it = container.set_value.find(key_str);
        return PyValue(it != container.set_value.end());
    }

    throw std::runtime_error("TypeError: get() only valid on dict or set");
}

// remove(...) for list, dict, set (mutates, returns None).
inline PyValue py_container_remove(PyValue& container,
                                   const PyValue& key_or_index) {
    if (container.type == PyValue::LIST) {
        if (key_or_index.type != PyValue::INT) {
            throw std::runtime_error("TypeError: list remove() index must be int");
        }
        long long idx = key_or_index.int_value;
        if (idx < 0 || idx >= (long long)container.list_value.size()) {
            throw std::runtime_error("IndexError: list index out of range in remove()");
        }
        container.list_value.erase(container.list_value.begin() + (std::size_t)idx);
        return PyValue();
    }

    if (container.type == PyValue::DICT) {
        std::string key_str = key_or_index.to_string();
        auto it = container.dict_value.find(key_str);
        if (it == container.dict_value.end()) {
            throw std::runtime_error("KeyError: key not found in dict remove()");
        }
        container.dict_value.erase(it);
        return PyValue();
    }

    if (container.type == PyValue::SET) {
        std::string key_str = key_or_index.to_string();
        auto it = container.set_value.find(key_str);
        if (it == container.set_value.end()) {
            throw std::runtime_error("KeyError: value not found in set remove()");
        }
        container.set_value.erase(it);
        return PyValue();
    }

    throw std::runtime_error("TypeError: remove() only valid on list, dict or set");
}
