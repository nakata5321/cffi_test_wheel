from cffi.model import *


def test_void_type():
    assert void_type.get_c_name() == "void"
    assert void_type.get_c_name("foo") == "void foo"
    assert void_type.get_c_name("*foo") == "void *foo"

def test_primitive_type():
    int_type = PrimitiveType("int")
    assert int_type.get_c_name() == "int"
    assert int_type.get_c_name("foo") == "int foo"
    assert int_type.get_c_name("*foo") == "int *foo"
    assert int_type.get_c_name("[5]") == "int[5]"

def test_raw_function_type():
    int_type = PrimitiveType("int")
    fn_type = RawFunctionType([], int_type, False)
    assert fn_type.get_c_name() == "int()(void)"
    assert fn_type.get_c_name("*") == "int( *)(void)"
    assert fn_type.get_c_name("*foo") == "int( *foo)(void)"
    fn_type = RawFunctionType([int_type], int_type, False)
    assert fn_type.get_c_name() == "int()(int)"
    fn_type = RawFunctionType([int_type] * 2, int_type, False)
    assert fn_type.get_c_name() == "int()(int, int)"
    #
    fn_type = RawFunctionType([int_type], int_type, True)
    assert fn_type.get_c_name() == "int()(int, ...)"
    assert fn_type.get_c_name("*foo") == "int( *foo)(int, ...)"
    #
    res_type = FunctionPtrType([int_type], int_type, True)
    fn_type = RawFunctionType([int_type], res_type, True)
    assert fn_type.get_c_name("x") == "int(*( x)(int, ...))(int, ...)"

def test_function_ptr_type():
    int_type = PrimitiveType("int")
    fn_type = FunctionPtrType([], int_type, False)
    assert fn_type.get_c_name() == "int(*)(void)"
    assert fn_type.get_c_name("*") == "int(* *)(void)"
    assert fn_type.get_c_name("*foo") == "int(* *foo)(void)"
    fn_type = FunctionPtrType([int_type], int_type, False)
    assert fn_type.get_c_name() == "int(*)(int)"
    fn_type = FunctionPtrType([int_type] * 2, int_type, False)
    assert fn_type.get_c_name() == "int(*)(int, int)"
    #
    fn_type = FunctionPtrType([int_type], int_type, True)
    assert fn_type.get_c_name() == "int(*)(int, ...)"

def test_pointer_type():
    ptr_type = PointerType(PrimitiveType("int"))
    assert ptr_type.get_c_name("x") == "int * x"

def test_const_pointer_type():
    ptr_type = ConstPointerType(PrimitiveType("int"))
    assert ptr_type.get_c_name("x") == "int const * x"
    ptr_type = ConstPointerType(ArrayType(PrimitiveType("int"), 5))
    assert ptr_type.get_c_name("") == "int const (*)[5]"
    assert ptr_type.get_c_name("*x") == "int const (* *x)[5]"
    ptr_type = ConstPointerType(ArrayType(
        ConstPointerType(PrimitiveType("int")), 5))
    assert ptr_type.get_c_name("x") == "int const * const (* x)[5]"
    ptr_type = PointerType(ArrayType(
        ConstPointerType(PrimitiveType("int")), 5))
    assert ptr_type.get_c_name("x") == "int const *(* x)[5]"
    ptr_type = ConstPointerType(ArrayType(
        PointerType(PrimitiveType("int")), 5))
    assert ptr_type.get_c_name("x") == "int * const (* x)[5]"

def test_qual_pointer_type():
    ptr_type = PointerType(PrimitiveType("long long"), Q_RESTRICT)
    assert ptr_type.get_c_name("") == "long long __restrict *"
    assert const_voidp_type.get_c_name("") == "void const *"

def test_unknown_pointer_type():
    ptr_type = unknown_ptr_type("foo_p")
    assert ptr_type.get_c_name("") == "foo_p"
    assert ptr_type.get_c_name("x") == "foo_p x"

def test_unknown_type():
    u_type = unknown_type("foo_t")
    assert u_type.get_c_name("") == "foo_t"
    assert u_type.get_c_name("x") == "foo_t x"

def test_array_type():
    a_type = ArrayType(PrimitiveType("int"), None)
    assert a_type.get_c_name("") == "int[]"
    assert a_type.get_c_name("x") == "int x[]"
    assert a_type.get_c_name("*x") == "int(*x)[]"
    assert a_type.get_c_name(" *x") == "int(*x)[]"
    assert a_type.get_c_name("[5]") == "int[5][]"
    a_type = ArrayType(unknown_type("foo_t"), 5)
    assert a_type.get_c_name("") == "foo_t[5]"
    assert a_type.get_c_name("x") == "foo_t x[5]"
    assert a_type.get_c_name("*x") == "foo_t(*x)[5]"
    a_type = ArrayType(unknown_ptr_type("foo_p"), None)
    assert a_type.get_c_name("") == "foo_p[]"
    assert a_type.get_c_name("x") == "foo_p x[]"
    assert a_type.get_c_name("*x") == "foo_p(*x)[]"
    a_type = ArrayType(ConstPointerType(PrimitiveType("int")), None)
    assert a_type.get_c_name("") == "int const *[]"
    assert a_type.get_c_name("x") == "int const * x[]"
    assert a_type.get_c_name("*x") == "int const *(*x)[]"
    fn_type = FunctionPtrType([], PrimitiveType("int"), False)
    a_type = ArrayType(fn_type, 5)
    assert a_type.get_c_name("") == "int(*[5])(void)"
    assert a_type.get_c_name("x") == "int(* x[5])(void)"
    assert a_type.get_c_name("*x") == "int(*(*x)[5])(void)"

def test_struct_type():
    struct_type = StructType("foo_s", None, None, None)
    assert struct_type.get_c_name() == "struct foo_s"
    assert struct_type.get_c_name("*x") == "struct foo_s *x"

def test_union_type():
    union_type = UnionType("foo_s", None, None, None)
    assert union_type.get_c_name() == "union foo_s"

def test_enum_type():
    enum_type = EnumType("foo_e", [], [])
    assert enum_type.get_c_name() == "enum foo_e"
