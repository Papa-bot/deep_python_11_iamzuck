#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <unicodeobject.h>
#include <ctype.h>
#include <stdio.h>

#ifndef PyUnicodeWriter
#define PyUnicodeWriter                          _PyUnicodeWriter
#define PyUnicodeWriter_Init                     _PyUnicodeWriter_Init
#define PyUnicodeWriter_Dealloc                  _PyUnicodeWriter_Dealloc
#define PyUnicodeWriter_Finish                   _PyUnicodeWriter_Finish
#define PyUnicodeWriter_WriteASCIIString         _PyUnicodeWriter_WriteASCIIString
#define PyUnicodeWriter_WriteChar                _PyUnicodeWriter_WriteChar
#endif

static inline int w_ascii(PyUnicodeWriter *w, const char *s, Py_ssize_t n) {
    return PyUnicodeWriter_WriteASCIIString(w, s, n);
}

static const char *skip_ws(const char *p, const char *end) {
    while (p < end && (*p == ' ' || *p == '\t' || *p == '\n' || *p == '\r')) ++p;
    return p;
}

static int dump_value(PyUnicodeWriter *w, PyObject *v);
static PyObject *parse_value(const char **pp, const char *end);

static int dump_string(PyUnicodeWriter *w, PyObject *v) {
    Py_ssize_t n;
    const char *s = PyUnicode_AsUTF8AndSize(v, &n);
    if (!s) return -1;
    if (w_ascii(w, "\"", 1) < 0) return -1;
    const char *look = s;
    while (look < s + n && *look != '"' && *look != '\\' && (unsigned char)*look >= 0x20) ++look;
    if (look == s + n) {
        if (w_ascii(w, s, n) < 0) return -1;
        return w_ascii(w, "\"", 1);
    }
    for (Py_ssize_t i = 0; i < n; ++i) {
        unsigned char c = s[i];
        switch (c) {
            case '\"': if (w_ascii(w, "\\\"", 2) < 0) return -1; break;
            case '\\': if (w_ascii(w, "\\\\", 2) < 0) return -1; break;
            case '\b': if (w_ascii(w, "\\b", 2) < 0) return -1; break;
            case '\f': if (w_ascii(w, "\\f", 2) < 0) return -1; break;
            case '\n': if (w_ascii(w, "\\n", 2) < 0) return -1; break;
            case '\r': if (w_ascii(w, "\\r", 2) < 0) return -1; break;
            case '\t': if (w_ascii(w, "\\t", 2) < 0) return -1; break;
            default:
                if (c < 0x20) {
                    char buf[7];
                    snprintf(buf, sizeof buf, "\\u%04x", c);
                    if (w_ascii(w, buf, 6) < 0) return -1;
                } else {
                    if (w_ascii(w, (const char *)&c, 1) < 0) return -1;
                }
        }
    }
    return w_ascii(w, "\"", 1);
}

static int dump_long(PyUnicodeWriter *w, PyObject *v) {
    int ov = 0;
    long long s = PyLong_AsLongLongAndOverflow(v, &ov);
    if (!ov) {
        char buf[64];
        int len = snprintf(buf, sizeof buf, "%lld", s);
        return w_ascii(w, buf, len);
    }
    PyObject *u = PyObject_Str(v);
    if (!u) return -1;
    Py_ssize_t n;
    const char *str = PyUnicode_AsUTF8AndSize(u, &n);
    int rc = str ? w_ascii(w, str, n) : -1;
    Py_DECREF(u);
    return rc;
}

static int dump_dict(PyUnicodeWriter *w, PyObject *d) {
    if (w_ascii(w, "{", 1) < 0) return -1;
    Py_ssize_t pos = 0;
    PyObject *k, *val;
    int first = 1;
    while (PyDict_Next(d, &pos, &k, &val)) {
        if (!PyUnicode_CheckExact(k)) {
            PyErr_SetString(PyExc_TypeError, "Keys must be str");
            return -1;
        }
        if (!first && w_ascii(w, ",", 1) < 0) return -1;
        first = 0;
        if (dump_string(w, k) < 0) return -1;
        if (w_ascii(w, ":", 1) < 0) return -1;
        if (dump_value(w, val) < 0) return -1;
    }
    return w_ascii(w, "}", 1);
}

static int dump_value(PyUnicodeWriter *w, PyObject *v) {
    if (PyLong_CheckExact(v)) return dump_long(w, v);
    if (PyUnicode_CheckExact(v)) return dump_string(w, v);
    if (PyDict_CheckExact(v)) return dump_dict(w, v);
    PyErr_SetString(PyExc_TypeError, "Unsupported value type");
    return -1;
}

static PyObject *cj_dumps(PyObject *self, PyObject *args) {
    PyObject *obj;
    if (!PyArg_ParseTuple(args, "O", &obj)) return NULL;
    if (!PyDict_Check(obj)) {
        PyErr_SetString(PyExc_TypeError, "Expected dict");
        return NULL;
    }
    PyUnicodeWriter w;
    PyUnicodeWriter_Init(&w);
    w.min_length = 64;
    w.overallocate = 1;
    if (dump_dict(&w, obj) < 0) {
        PyUnicodeWriter_Dealloc(&w);
        return NULL;
    }
    return PyUnicodeWriter_Finish(&w);
}

static PyObject *parse_string(const char **pp, const char *end) {
    const char *p = *pp + 1;
    PyUnicodeWriter w;
    PyUnicodeWriter_Init(&w);
    while (p < end) {
        unsigned char c = *p++;
        if (c == '"') {
            *pp = p;
            return PyUnicodeWriter_Finish(&w);
        }
        if (c == '\\') {
            if (p >= end) goto err;
            c = *p++;
            switch (c) {
                case '"':  if (w_ascii(&w, "\"", 1) < 0) goto errw; break;
                case '\\': if (w_ascii(&w, "\\", 1) < 0) goto errw; break;
                case '/':  if (w_ascii(&w, "/", 1) < 0) goto errw; break;
                case 'b':  if (w_ascii(&w, "\b", 1) < 0) goto errw; break;
                case 'f':  if (w_ascii(&w, "\f", 1) < 0) goto errw; break;
                case 'n':  if (w_ascii(&w, "\n", 1) < 0) goto errw; break;
                case 'r':  if (w_ascii(&w, "\r", 1) < 0) goto errw; break;
                case 't':  if (w_ascii(&w, "\t", 1) < 0) goto errw; break;
                case 'u': {
                    if (end - p < 4) goto err;
                    Py_UCS4 ch = 0;
                    for (int i = 0; i < 4; ++i) {
                        unsigned char h = p[i];
                        ch <<= 4;
                        if (h >= '0' && h <= '9') ch |= h - '0';
                        else if (h >= 'A' && h <= 'F') ch |= h - 'A' + 10;
                        else if (h >= 'a' && h <= 'f') ch |= h - 'a' + 10;
                        else goto err;
                    }
                    p += 4;
                    if (PyUnicodeWriter_WriteChar(&w, ch) < 0) goto errw;
                    break;
                }
                default: goto err;
            }
            continue;
        }
        if (c < 0x20) goto err;
        if (w_ascii(&w, (const char *)&c, 1) < 0) goto errw;
    }
err: PyErr_SetString(PyExc_ValueError, "Invalid string escape");
errw: PyUnicodeWriter_Dealloc(&w); return NULL;
}

static int is_digit(unsigned char c) { return c >= '0' && c <= '9'; }

static PyObject *parse_number(const char **pp, const char *end) {
    const char *p = *pp, *q = p;
    int is_int = 1;
    if (*q == '-') ++q;
    if (q >= end || !is_digit(*q)) goto bad;
    while (q < end && is_digit(*q)) ++q;
    if (q < end && *q == '.') { is_int = 0; ++q; while (q < end && is_digit(*q)) ++q; }
    if (q < end && (*q == 'e' || *q == 'E')) {
        is_int = 0; ++q;
        if (q < end && (*q == '+' || *q == '-')) ++q;
        if (q >= end || !is_digit(*q)) goto bad;
        while (q < end && is_digit(*q)) ++q;
    }
    PyObject *res;
    if (is_int) {
        PyObject *tmp = PyUnicode_DecodeUTF8(p, q - p, NULL);
        if (!tmp) return NULL;
        res = PyLong_FromUnicodeObject(tmp, 10);
        Py_DECREF(tmp);
    } else {
        char *endp;
        double d = PyOS_string_to_double(p, &endp, NULL);
        if (endp != q) goto bad;
        res = PyFloat_FromDouble(d);
    }
    if (!res) return NULL;
    *pp = q;
    return res;
bad: PyErr_SetString(PyExc_ValueError, "Invalid number"); return NULL;
}

static PyObject *parse_object(const char **pp, const char *end) {
    const char *p = skip_ws(*pp, end);
    if (*p != '{') { PyErr_SetString(PyExc_ValueError, "Expected '{'"); return NULL; }
    ++p;
    PyObject *d = PyDict_New();
    if (!d) return NULL;
    p = skip_ws(p, end);
    if (*p == '}') { *pp = p + 1; return d; }
    while (p < end) {
        PyObject *k = parse_string(&p, end);
        if (!k) { Py_DECREF(d); return NULL; }
        p = skip_ws(p, end);
        if (*p != ':') { Py_DECREF(d); Py_DECREF(k); PyErr_SetString(PyExc_ValueError, "Expected ':'"); return NULL; }
        ++p;
        PyObject *val = parse_value(&p, end);
        if (!val) { Py_DECREF(d); Py_DECREF(k); return NULL; }
        if (PyDict_SetItem(d, k, val) < 0) { Py_DECREF(d); Py_DECREF(k); Py_DECREF(val); return NULL; }
        Py_DECREF(k); Py_DECREF(val);
        p = skip_ws(p, end);
        if (*p == '}') { *pp = p + 1; return d; }
        if (*p != ',') { Py_DECREF(d); PyErr_SetString(PyExc_ValueError, "Expected ','"); return NULL; }
        ++p;
        p = skip_ws(p, end);
    }
    Py_DECREF(d); PyErr_SetString(PyExc_ValueError, "Invalid object syntax"); return NULL;
}

static PyObject *parse_value(const char **pp, const char *end) {
    const char *p = skip_ws(*pp, end);
    if (p >= end) { PyErr_SetString(PyExc_ValueError, "Unexpected end"); return NULL; }
    PyObject *res = NULL;
    if (*p == '{') res = parse_object(&p, end);
    else if (*p == '"') res = parse_string(&p, end);
    else res = parse_number(&p, end);
    if (res) *pp = p;
    return res;
}

static PyObject *cj_loads(PyObject *self, PyObject *args) {
    const char *s; Py_ssize_t n;
    if (!PyArg_ParseTuple(args, "s#", &s, &n)) return NULL;
    const char *p = s;
    PyObject *obj = parse_value(&p, s + n);
    if (!obj) return NULL;
    p = skip_ws(p, s + n);
    if (p != s + n) { Py_DECREF(obj); PyErr_SetString(PyExc_ValueError, "Extra data after object"); return NULL; }
    return obj;
}

static PyMethodDef Methods[] = {
    {"loads", cj_loads, METH_VARARGS, NULL},
    {"dumps", cj_dumps, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = { PyModuleDef_HEAD_INIT, "custom_json", NULL, -1, Methods };

PyMODINIT_FUNC PyInit_custom_json(void) { return PyModule_Create(&module); }