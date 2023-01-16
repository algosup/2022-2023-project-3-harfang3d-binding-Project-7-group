

import lang.rust


def bind_stl(gen):
    gen.include('vector',True)
    gen.include('string',True)

    class RustStringConverter(lang.rust.RustTypeConverterCommon):
        def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
            super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
            self.rust_to_c_type = "*char"
            self.rust_type = "string"
            
        def get_type_glue(self, gen, module_name):
            return ''

        def get_type_api(self, module_name):
            return ''

        def to_c_call(self, in_var, out_var_p, is_pointer=False):
            if is_pointer:
                out = f"{out_var_p.replace('&', '_')}1 := C.CString(*{in_var})\n"
                out += f"{out_var_p.replace('&', '_')} := &{out_var_p.replace('&', '_')}1\n"
            else:
                out = f"{out_var_p.replace('&', '_')}, idFin{out_var_p.replace('&', '_')} := wrapString({in_var})\n"
                out += f"defer idFin{out_var_p.replace('&', '_')}()\n"
            return out

        def from_c_call(self, out_var, expr, ownership):
            return "C.GoString(%s)" % (out_var)