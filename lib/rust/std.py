import lang.rust

def bind_std(gen):
	class RustConstCharPtrConverter(lang.rust.RustTypeConverterCommon):
		def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=None):
			super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)

	gen.bind_type(RustConstCharPtrConverter("const char *"))

	class RustBasicTypeConverter(lang.rust.RustTypeConverterCommon):
		def __init__(self, type, c_type, rust_type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
			super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
			self.rust_to_c_type = c_type
			self.rust_type = rust_type

		def get_type_glue(self, gen, module_name):
			return ''

		def get_type_api(self, module_name):
			return ''

		def to_c_call(self, in_var, out_var_p, is_pointer):
			if is_pointer:
				out = f"let mut {out_var_p} : *mut {self.rust_type} = {in_var} as *{self.rust_to_c_type};\n"
			else:
				out = f"let mut {out_var_p} : {self.rust_type} = {in_var} as {self.rust_to_c_type};\n"
			return out

		def from_c_call(self, out_var, expr, ownership):
			return f"{out_var} as {self.rust_to_c_type}"
	
	gen.bind_type(RustBasicTypeConverter('char', 'i8'))
	gen.bind_type(RustBasicTypeConverter('short', 'i16'))
	gen.bind_type(RustBasicTypeConverter('int', 'i32'))
	gen.bind_type(RustBasicTypeConverter('long', 'i32'))
	gen.bind_type(RustBasicTypeConverter('long long', 'i64'))


	gen.bind_type(RustBasicTypeConverter('int8_t', 'i8'))
	gen.bind_type(RustBasicTypeConverter('int16_t', 'i16'))
	gen.bind_type(RustBasicTypeConverter('int32_t', 'i32'))
	gen.bind_type(RustBasicTypeConverter('int64_t', 'i64'))

	gen.bind_type(RustBasicTypeConverter('char16_t', 'i16'))
	gen.bind_type(RustBasicTypeConverter('char32_t', 'i32'))

	gen.bind_type(RustBasicTypeConverter('unsigned char', 'u8'))
	gen.bind_type(RustBasicTypeConverter('unsigned short', 'u16'))
	gen.bind_type(RustBasicTypeConverter('unsigned int', 'u32'))
	gen.bind_type(RustBasicTypeConverter('unsigned long', 'u32'))
	gen.bind_type(RustBasicTypeConverter('unsigned long long', 'u64'))

	gen.bind_type(RustBasicTypeConverter('uint8_t', 'u8'))
	gen.bind_type(RustBasicTypeConverter('uint16_t', 'u16'))
	gen.bind_type(RustBasicTypeConverter('uint32_t', 'u32'))
	gen.bind_type(RustBasicTypeConverter('uint64_t', 'u64'))

	gen.bind_type(RustBasicTypeConverter('size_t', 'isize'))

	gen.bind_type(RustBasicTypeConverter('float', 'f32'))
	gen.bind_type(RustBasicTypeConverter('double', 'f64'))


	class RustBoolConverter(lang.go.GoTypeConverterCommon):
		def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
			super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
			self.rust_to_c_type = "bool"

		def get_type_glue(self, gen, module_name):
			return ''

		def get_type_api(self, module_name):
			return ''

		def to_c_call(self, in_var, out_var_p, is_pointer):
			if is_pointer:
				out = f"let mut {out_var_p} : *mut bool = {in_var} as *bool;\n"
			else:
				out = f"let mut {out_var_p} : bool = {in_var} as bool\n"
			return out

		def from_c_call(self, out_var, expr, ownership):
			return f"{out_var} as bool"

	gen.bind_type(RustBoolConverter('bool')).nobind = True