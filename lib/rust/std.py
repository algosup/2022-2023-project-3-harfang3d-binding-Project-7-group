import lang.rust

def bind_std(gen):
	class RustConstCharPtrConverter(lang.rust.RustTypeConverterCommon):
		def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=None):
			super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
		
		def get_type_glue(self, gen, module_name):
			return ''

		def get_type_api(self, module_name):
			return ''

		def to_c_call(self, in_var, out_var_p, is_pointer=False):
			if is_pointer:
				out = f"let *mut {out_var_p.replace('&', '_')} : &str = wrapString(*{in_var})\n"
				#out += f"{out_var_p.replace('&', '_')} := &{out_var_p.replace('&', '_')}1\n"
			else:
				out = f"let *mut {out_var_p.replace('&', '_')} : &str = wrapString({in_var})\n"
				#out += f"defer idFin{out_var_p.replace('&', '_')}()\n"
			return out

		def from_c_call(self, out_var, expr, ownership):
			return "C.GoString(%s)" % (out_var)

	gen.bind_type(RustConstCharPtrConverter("&str"))

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

	gen.bind_type(RustBasicTypeConverter('char','c_char', 'i8'))
	gen.bind_type(RustBasicTypeConverter('signed char','c_schar', 'i8'))
	gen.bind_type(RustBasicTypeConverter('unsigned char','c_uchar', 'u8'))

	gen.bind_type(RustBasicTypeConverter('short','c_short', 'i16'))
	gen.bind_type(RustBasicTypeConverter('unsigned short','c_ushort', 'u16'))

	gen.bind_type(RustBasicTypeConverter('int','c_int', 'i32'))
	gen.bind_type(RustBasicTypeConverter('unsigned int','c_uint', 'u32'))

	gen.bind_type(RustBasicTypeConverter('long','c_long', 'i64'))
	gen.bind_type(RustBasicTypeConverter('unsigned long','c_ulong', 'u64'))

	gen.bind_type(RustBasicTypeConverter('int8_t','c_char', 'i8'))
	gen.bind_type(RustBasicTypeConverter('uint8_t','c_ushort', 'u8'))

	gen.bind_type(RustBasicTypeConverter('int16_t','c_short', 'i16'))
	gen.bind_type(RustBasicTypeConverter('uint16_t','c_ushort', 'u16'))

	gen.bind_type(RustBasicTypeConverter('int32_t','c_int', 'i32'))
	gen.bind_type(RustBasicTypeConverter('uint32_t','c_uint', 'u32'))

	gen.bind_type(RustBasicTypeConverter('int64_t','c_long', 'i64'))
	gen.bind_type(RustBasicTypeConverter('uint64_t','c_ulong', 'u64'))

	gen.bind_type(RustBasicTypeConverter('char16_t','c_short', 'i16'))
	gen.bind_type(RustBasicTypeConverter('char32_t','c_int', 'i32'))

	#TODO: This should be defined at runtime instead to support systems other than 64bits
	gen.bind_type(RustBasicTypeConverter('size_t','c_long', 'isize'))

	gen.bind_type(RustBasicTypeConverter('float','c_float', 'f32'))
	gen.bind_type(RustBasicTypeConverter('double','c_double', 'f64'))

	class RustBoolConverter(lang.rust.RustTypeConverterCommon):
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