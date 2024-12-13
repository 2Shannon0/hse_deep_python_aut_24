#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static PyObject* parse_json(const char* json_str) {
    PyObject *dict = NULL;

    if (!(dict = PyDict_New())) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to create a new dictionary");
        return NULL;
    }

    const char* ptr = json_str;
    while (*ptr && *ptr != '{') ptr++;

    if (*ptr != '{') {
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        Py_DECREF(dict);
        return NULL;
    }

    ptr++;

    while (*ptr && *ptr != '}') {
        while (*ptr && isspace(*ptr)) ptr++;

        if (*ptr != '"') {
            PyErr_Format(PyExc_TypeError, "Expected key as string");
            Py_DECREF(dict);
            return NULL;
        }
        ptr++;
        
        const char* key_start = ptr;
        while (*ptr && *ptr != '"') ptr++;

        if (*ptr != '"') {
            PyErr_Format(PyExc_TypeError, "Unterminated key string");
            Py_DECREF(dict);
            return NULL;
        }
        
        PyObject* key = PyUnicode_FromStringAndSize(key_start, ptr - key_start);
        ptr++;

        while (*ptr && isspace(*ptr)) ptr++;
        if (*ptr != ':') {
            PyErr_Format(PyExc_TypeError, "Expected ':' after key");
            Py_DECREF(key);
            Py_DECREF(dict);
            return NULL;
        }
        ptr++;

        while (*ptr && isspace(*ptr)) ptr++;

        PyObject* value = NULL;
        if (*ptr == '"') {
            ptr++;
            const char* value_start = ptr;
            while (*ptr && *ptr != '"') ptr++;

            if (*ptr != '"') {
                PyErr_Format(PyExc_TypeError, "Unterminated value string");
                Py_DECREF(key);
                Py_DECREF(dict);
                return NULL;
            }

            value = PyUnicode_FromStringAndSize(value_start, ptr - value_start);
            ptr++;
        } else if (isdigit(*ptr) || *ptr == '-') {
            char* end_ptr;
            long num = strtol(ptr, &end_ptr, 10);
            if (ptr == end_ptr) {
                PyErr_Format(PyExc_TypeError, "Invalid number");
                Py_DECREF(key);
                Py_DECREF(dict);
                return NULL;
            }
            value = PyLong_FromLong(num);
            ptr = end_ptr;
        } else {
            PyErr_Format(PyExc_TypeError, "Unsupported value type");
            Py_DECREF(key);
            Py_DECREF(dict);
            return NULL;
        }

        if (PyDict_SetItem(dict, key, value) < 0) {
            Py_DECREF(key);
            Py_DECREF(value);
            Py_DECREF(dict);
            return NULL;
        }

        Py_DECREF(key);
        Py_DECREF(value);

        while (*ptr && isspace(*ptr)) ptr++;
        if (*ptr == ',') ptr++;
    }

    if (*ptr != '}') {
        PyErr_Format(PyExc_TypeError, "Expected closing brace");
        Py_DECREF(dict);
        return NULL;
    }

    return dict;
}

static PyObject* custom_json_loads(PyObject* self, PyObject* args) {
    const char* json_str;

    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        return NULL;
    }

    return parse_json(json_str);
}

static int serialize_dict(PyObject* dict, PyObject* str_list) {
    PyObject *key, *value;
    Py_ssize_t pos = 0;

    PyList_Append(str_list, PyUnicode_FromString("{"));

    int first = 1;
    while (PyDict_Next(dict, &pos, &key, &value)) {
        if (!first) {
            PyList_Append(str_list, PyUnicode_FromString(", "));
        }
        first = 0;

        PyObject* key_str_obj = PyObject_Str(key);
        const char *key_str = PyUnicode_AsUTF8(key_str_obj);

        if (PyUnicode_Check(value)) {
            const char *str_value = PyUnicode_AsUTF8(value);
            if (!str_value) {
                Py_DECREF(key_str_obj);
                Py_DECREF(str_list);
                return -1;
            }
            PyList_Append(str_list, PyUnicode_FromFormat("\"%s\": \"%s\"", key_str, str_value));
        } else if (PyLong_Check(value)) {
            long num_value = PyLong_AsLong(value);
            PyList_Append(str_list, PyUnicode_FromFormat("\"%s\": %ld", key_str, num_value));
        } else {
            PyErr_Format(PyExc_TypeError, "Unsupported value type");
            Py_DECREF(key_str_obj);
            Py_DECREF(str_list);
            return -1;
        }

        Py_DECREF(key_str_obj);
    }

    PyList_Append(str_list, PyUnicode_FromString("}"));
    return 0;
}

static PyObject* custom_json_dumps(PyObject* self, PyObject* args) {
    PyObject* dict;

    if (!PyArg_ParseTuple(args, "O!", &PyDict_Type, &dict)) {
        return NULL;
    }

    PyObject* str_list = PyList_New(0);
    if (serialize_dict(dict, str_list) < 0) {
        Py_DECREF(str_list);
        return NULL;
    }

    PyObject* result = PyUnicode_Join(PyUnicode_FromString(""), str_list);
    Py_DECREF(str_list);

    return result;
}

static PyMethodDef CustomJsonMethods[] = {
    {"loads", custom_json_loads, METH_VARARGS, "Parse a JSON string into a Python dictionary."},
    {"dumps", custom_json_dumps, METH_VARARGS, "Serialize a Python dictionary into a JSON string."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef customjsonmodule = {
    PyModuleDef_HEAD_INIT,
    "custom_json",
    "Custom JSON parser and serializer.",
    -1,
    CustomJsonMethods
};

PyMODINIT_FUNC PyInit_custom_json(void) {
    return PyModule_Create(&customjsonmodule);
}
