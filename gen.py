from pypeg2 import re, flag, name, Plain, optional, attr, K, parse
import copy


#
typename = re.compile(r"((::)*(_|[A-z])[A-z0-9_]*)+")
ref_re = re.compile(r"[&*]+")


def get_fully_qualified_ctype_name(type):
	out = ''
	if type.const:
		out += 'const '
	out += type.unqualified_name
	if hasattr(type, 'ref'):
		out += ' ' + type.ref
	return out


def get_type_clean_name(type):
	""" Return a type name cleaned so that it may be used as variable name in the generator output."""
	parts = type.split(' ')

	def clean_type_name_part(part):
		part = part.replace('*', 'ptr')  # pointer
		part = part.replace('&', '_r')  # reference
		part = part.replace('::', '__')  # namespace
		return part

	parts = [clean_type_name_part(part) for part in parts]
	return '_'.join(parts)


def ctypes_to_string(ctypes):
	return ','.join([repr(ctype) for ctype in ctypes])


class _CType:
	def __repr__(self):
		return get_fully_qualified_ctype_name(self)

	def get_ref(self, extra_transform=''):
		return (self.ref if hasattr(self, 'ref') else '') + extra_transform

	def add_ref(self, ref):
		t = copy.deepcopy(self)
		if hasattr(self, 'ref'):
			t.ref += ref
		else:
			setattr(t, 'ref', ref)
		return t


_CType.grammar = flag("const", K("const")), optional([flag("signed", K("signed")), flag("unsigned", K("unsigned"))]), attr("unqualified_name", typename), optional(attr("ref", ref_re))


#
def clean_c_symbol_name(name):
	name = name.replace('::', '__')
	return name


#
def _prepare_ctypes(ctypes, template):
	if not type(ctypes) is type([]):
		ctypes = [ctypes]
	return [parse(type, template) for type in ctypes]


#
class _CArg:
	def __repr__(self):
		out = repr(self.ctype)
		if hasattr(self, 'name'):
			out += ' ' + str(self.name)
		return out


_CArg.grammar = attr("ctype", _CType), optional(name())


#
def ctype_ref_to(src_ref, dst_ref):
	i = 0
	while i < len(src_ref) and i < len(dst_ref):
		if src_ref[i] != dst_ref[i]:
			break
		i += 1

	src_ref = src_ref[i:]
	dst_ref = dst_ref[i:]

	if src_ref == '&':
		if dst_ref == '&':
			return ''  # ref to ref
		elif dst_ref == '*':
			return '&'  # ref to ptr
		else:
			return ''  # ref to value
	elif src_ref == '*':
		if dst_ref == '&':
			return '*'  # ptr to ref
		elif dst_ref == '*':
			return ''  # ptr to ptr
		else:
			return '*'  # ptr to value
	else:
		if dst_ref == '&':
			return ''  # value to ref
		elif dst_ref == '*':
			return '&'  # value to ptr
		else:
			return ''  # value to value


def transform_var_ref_to(var, from_ref, to_ref):
	return ctype_ref_to(from_ref, to_ref) + var


class TypeConverter:
	def __init__(self, type, storage_type=None):
		if not storage_type:
			storage_type = type

		self.ctype = parse(type, _CType)
		self.storage_ctype = parse(storage_type, _CType)

		self.clean_name = get_type_clean_name(type)
		self.bound_name = self.clean_name
		self.fully_qualified_name = get_fully_qualified_ctype_name(self.ctype)
		self.type_tag = '__%s_type_tag' % self.clean_name

		self.constructor = None
		self.members = []
		self.methods = []

		self.bases = []  # type derives from the following types

	def get_type_api(self, module_name):
		return ''

	def finalize_type(self):
		return ''

	def to_c_call(self, out_var, in_var_p):
		assert 'to_c_call not implemented in converter'

	def from_c_call(self, ctype, out_var, in_var_p):
		assert 'from_c_call not implemented in converter'

	def prepare_var_for_conv(self, var, var_ref):
		"""Prepare a variable for use with the converter from_c/to_c methods."""
		return transform_var_ref_to(var, var_ref, self.ctype.get_ref('*'))

	def get_all_methods(self):
		"""Return a list of all the type methods (including inherited methods)."""
		all_methods = copy.copy(self.methods)

		def collect_base_methods(base):
			for method in base.methods:
				if not any(m['name'] == method['name'] for m in all_methods):
					all_methods.append(method)

			for _base in base.bases:
				collect_base_methods(_base)

		for base in self.bases:
			collect_base_methods(base)

		return all_methods

	def can_upcast_to(self, type):
		clean_name = get_type_clean_name(type)

		if self.clean_name == clean_name:
			return True

		for base in self.bases:
			if base.can_upcast_to(type):
				return True

		return False


#
class FABGen:
	def output_header(self):
		common = "// This file is automatically generated, do not modify manually!\n\n"

		self._source += "// FABgen .cpp\n"
		self._source += common
		self._header += "// FABgen .h\n"
		self._header += common

	def output_includes(self):
		self.add_include('cstdint', True)

		self._source += '{{{__WRAPPER_INCLUDES__}}}\n'

	def start(self, name):
		self._name = name
		self._header, self._source = "", ""

		self.__system_includes, self.__user_includes = [], []

		self.__type_convs = {}
		self.__function_templates = {}

		self._bound_types = []  # list of bound types
		self._bound_functions = []  # list of bound functions

		self.output_header()
		self.output_includes()

		self._source += 'enum OwnershipPolicy { NonOwning, Copy, Owning };\n\n'
		self._source += 'void *_type_tag_upcast(void *in_p, const char *in_type_tag, const char *out_type_tag);\n\n'

	def add_include(self, path, is_system_include = False):
		if is_system_include:
			self.__system_includes.append(path)
		else:
			self.__user_includes.append(path)

	def insert_code(self, code, in_source=True, in_header=True):
		if in_header:
			self._header += code
		if in_source:
			self._source += code

	#
	def raise_exception(self, type, reason):
		assert 'raise_exception not implemented in generator'

	#
	def proto_check(self, name, ctype):
		assert 'proto_check not implemented in generator'
	def proto_to_c(self, name, ctype):
		assert 'proto_check not implemented in generator'
	def proto_from_c(self, name, ctype):
		assert 'proto_check not implemented in generator'

	#
	def _begin_type(self, conv):
		"""Declare a new type converter."""
		self._bound_types.append(conv)
		self.__type_convs[conv.fully_qualified_name] = conv
		return conv

	def _end_type(self, conv):
		self._header += conv.get_type_api(self._name)
		self._source += '// %s type glue\n' % conv.fully_qualified_name
		self._source += 'static const char *%s = "%s";\n\n' % (conv.type_tag, conv.fully_qualified_name)
		self._source += conv.get_type_glue(self._name)
		self.insert_code('\n')

	#
	def bind_type(self, conv):
		self._begin_type(conv)
		self._end_type(conv)

	#
	def get_class_default_converter(self):
		assert "missing class type default converter"

	def begin_class(self, name):
		class_default_conv = self.get_class_default_converter()

		conv = class_default_conv(name)
		api = conv.get_type_api(self._name)
		self._source += api + '\n'

		return self._begin_type(conv)

	def end_class(self, conv):
		self._end_type(conv)

	#
	def add_class_base(self, obj, base):
		base_conv = self.__type_convs[base]
		obj.bases.append(base_conv)

	#
	def select_ctype_conv(self, ctype):
		"""Select a type converter."""
		full_qualified_ctype_name = get_fully_qualified_ctype_name(ctype)

		if full_qualified_ctype_name == 'void':
			return None

		if full_qualified_ctype_name in self.__type_convs:
			return self.__type_convs[full_qualified_ctype_name]

		return self.__type_convs[ctype.unqualified_name]

	#
	def decl_var(self, ctype, name, end_of_expr=';\n'):
		return '%s %s%s' % (get_fully_qualified_ctype_name(ctype), name, end_of_expr)

	#
	def select_args_convs(self, args):
		return [{'conv': self.select_ctype_conv(arg.ctype), 'ctype': arg.ctype} for i, arg in enumerate(args)]

	def cleanup_args(self, args):
		pass

	#
	def commit_rvals(self, rval):
		assert "missing return values template"

	def cleanup_rvals(self, rval):
		pass

	#
	@staticmethod
	def __get_proxy_function_name(name, prefix=''):
		return '_' + prefix + clean_c_symbol_name(name)

	def _declare_and_convert_function_call_args(self, args):
		args = self.select_args_convs(args)

		c_call_args = []
		for i, arg in enumerate(args):
			conv = arg['conv']
			if not conv:
				continue

			arg_name = 'arg%d' % i
			self._source += self.decl_var(conv.storage_ctype, arg_name)
			self._source += conv.to_c_call(self.get_arg(i), '&' + arg_name)

			c_call_arg_transform = ctype_ref_to(conv.storage_ctype.get_ref(), arg['ctype'].get_ref())
			c_call_args.append(c_call_arg_transform + arg_name)

		return c_call_args

	def _declare_return_value(self, rval):
		rval_conv = self.select_ctype_conv(rval)
		if rval_conv:
			self._source += self.decl_var(rval, 'rval', ' = ')
		return rval_conv

	def _declare_and_convert_self(self, obj, var_in, var_out):
		self._source += '\t' + self.decl_var(obj.storage_ctype, var_out)
		self._source += '\t' + obj.to_c_call(var_in, '&' + var_out)

	def __ref_to_ownership_policy(self, ctype):
		return 'Copy' if ctype.get_ref() == '' else 'NonOwning'

	def _convert_rval(self, rval, rval_conv, ownership):
		if rval_conv:
			self.rval_from_c_ptr(rval, 'rval', rval_conv, ctype_ref_to(rval.get_ref(), rval_conv.ctype.get_ref() + '*') + 'rval', ownership)

		self.commit_rvals(rval)
		self.cleanup_rvals(rval)

	#
	def bind_function(self, name, rval, args):
		rval = parse(rval, _CType)
		args = _prepare_ctypes(args, _CArg)

		self.insert_code('// %s %s(%s)\n' % (rval, name, ctypes_to_string(args)), True, False)

		proxy_name = self.__get_proxy_function_name(name)
		self.open_function(proxy_name, args)

		self._bound_functions.append({'name': name, 'proxy_name': proxy_name, 'rval': rval, 'args': args})

		# declare and convert args
		c_call_args = self._declare_and_convert_function_call_args(args)

		# declare rval
		rval_conv = self._declare_return_value(rval)

		# perform function call
		self._source += '%s(%s);\n' % (name, ', '.join(c_call_args))

		# cleanup arguments
		self.cleanup_args(args)

		# convert return values
		self._convert_rval(rval, rval_conv, self.__ref_to_ownership_policy(rval))

		self.close_function()
		self._source += '\n'

	def bind_function_with_overloads(self, name, protos):
		self.insert_code('// %s dispatcher\n' % name, True, False)

		proxy_name = self.__get_proxy_function_name(name)
		self.open_function(proxy_name)

		for proto in protos:
			rval, args = proto

		self.close_function()
		self._source += '\n'

	# class member/method
	def bind_class_method(self, obj, name, rval, args):
		rval = parse(rval, _CType)
		args = _prepare_ctypes(args, _CArg)

		self.insert_code('// %s %s::%s(%s)\n' % (rval, obj.fully_qualified_name, name, ctypes_to_string(args)), True, False)

		proxy_name = self.__get_proxy_function_name(name, obj.clean_name + '_')
		arg_vars = self.open_method(proxy_name, args)

		# declare and convert self and args
		self._declare_and_convert_self(obj, arg_vars[0], 'self')
		c_call_args = self._declare_and_convert_function_call_args(args, arg_vars[1:])  # note: drop self from arg_vars

		# declare rval
		rval_conv = self._declare_return_value(rval)

		# perform method call
		self._source += 'self->%s(%s);\n' % (name, ', '.join(c_call_args))

		# cleanup arguments
		self.cleanup_args(args)

		# convert return values
		self._convert_rval(rval, rval_conv, self.__ref_to_ownership_policy(rval))

		self.close_method()
		self._source += '\n'

		obj.methods.append({'name': name, 'proxy_name': proxy_name, 'rval': rval, 'args': args})

	#
	def bind_class_constructor(self, obj, args):
		rval = obj.ctype
		args = _prepare_ctypes(args, _CArg)

		self.insert_code('// %s(%s)\n' % (obj.fully_qualified_name, ctypes_to_string(args)), True, False)

		proxy_name = self.__get_proxy_function_name("constructor_proxy", obj.clean_name + '_')
		arg_vars = self.open_method(proxy_name, args)

		# declare and convert args
		c_call_args = self._declare_and_convert_function_call_args(args, arg_vars[1:])  # note: drop self from arg_vars

		# declare rval
		rval_conv = self._declare_return_value(rval.add_ref('*'))

		# perform method call
		self._source += 'new %s(%s);\n' % (obj.fully_qualified_name, ', '.join(c_call_args))

		# cleanup arguments
		self.cleanup_args(args)

		# convert return values
		self._convert_rval(rval, rval_conv, "Owning")

		self.close_method()
		self._source += '\n'

		obj.constructor = {'proxy_name': proxy_name, 'args': args}

	#
	def bind_class_member(self, obj, member):
		member = parse(member, _CArg)
		member_conv = self.select_ctype_conv(member.ctype)

		getset_expr = member_conv.prepare_var_for_conv('self->%s' % member.name, member.ctype.get_ref())  # pointer to the converter supported type

		#
		self._source += '// get/set %s %s::%s\n' % (member.ctype, member_conv.clean_name, member.name)

		# getter
		arg_vars = self.open_getter_function('_%s_get_%s' % (obj.clean_name, member.name))

		self._declare_and_convert_self(obj, arg_vars[0], 'self')

		rval = [member.ctype]
		self.rval_from_c_ptr(member.ctype, 'rval', member_conv, getset_expr, self.__ref_to_ownership_policy(member.ctype))
		self.commit_rvals(rval)
		self.cleanup_rvals(rval)
		self.close_getter_function()

		# setter
		arg_vars = self.open_setter_function('_%s_set_%s' % (obj.clean_name, member.name))

		self._declare_and_convert_self(obj, arg_vars[0], 'self')
		self._source += member_conv.to_c_call(arg_vars[1], getset_expr)
		self.close_setter_function()

		self._source += '\n'

		obj.members.append(member)

	# global function template
	def decl_function_template(self, tmpl_name, tmpl_args, rval, args):
		self.__function_templates[tmpl_name] = {'tmpl_args': tmpl_args, 'rval': rval, 'args': args}

	def bind_function_template(self, tmpl_name, bound_name, bind_args):
		tmpl = self.__function_templates[tmpl_name]
		tmpl_args = tmpl['tmpl_args']

		assert len(tmpl_args) == len(bind_args)

		def bind_tmpl_arg(arg):
			return bind_args[tmpl_args.index(arg)] if arg in tmpl_args else arg

		bound_rval = bind_tmpl_arg(tmpl['rval'])
		bound_args = [bind_tmpl_arg(arg) for arg in tmpl['args']]

		bound_named_args = ['%s arg%d' % (arg, idx) for idx, arg in enumerate(bound_args)]

		# output wrapper
		self._source += '// %s<%s> wrapper\n' % (tmpl_name, ', '.join(bind_args))
		self._source += 'static %s %s(%s) {\n' % (bound_rval, bound_name, ', '.join(bound_named_args))
		if bound_rval != 'void':
			self._source += 'return '
		self._source += '%s<%s>(%s);\n' % (tmpl_name, ', '.join(bind_args), ', '.join(['arg%d' % i for i in range(len(bound_args))]))
		self._source += '}\n\n'

		# bind wrapper
		self.bind_function(bound_name, bound_rval, bound_args)

	#
	def output_summary(self):
		self._source += '// Bound %d global functions:\n' % len(self._bound_functions)
		for f in self._bound_functions:
			self._source += '//	- %s bound as %s\n' % (f['name'], f['bound_name'])
		self._source += '\n'

	def get_type_tag_cast_function(self):
		downcasts = {}
		for type in self._bound_types:
			downcasts[type] = []

		def register_upcast(type, bases):
			for base in bases:
				downcasts[base].append(type)
				register_upcast(type, base.bases)

		for type in self._bound_types:
			register_upcast(type, type.bases)

		#
		out = '// type_tag based cast system\n'
		out += 'void *_type_tag_upcast(void *in_p, const char *in_type_tag, const char *out_type_tag) {\n'
		out += '	if (out_type_tag == in_type_tag)\n'
		out += '		return in_p;\n\n'

		out += '	void *out_p = NULL;\n\n'

		i = 0
		for base in self._bound_types:
			if len(downcasts[base]) == 0:
				continue

			out += '	' if i == 0 else ' else '
			out += 'if (out_type_tag == %s) {\n' % base.type_tag

			for j, downcast in enumerate(downcasts[base]):
				out += '		' if j == 0 else '		else '
				out += 'if (in_type_tag == %s)\n' % downcast.type_tag
				out += '			out_p = (%s *)((%s *)in_p);\n' % (get_fully_qualified_ctype_name(base.ctype), get_fully_qualified_ctype_name(downcast.ctype))

			out += '	}'
			i += 1

		out += '''

	return out_p;
}\n\n'''
		return out

	def finalize(self):
		# insert includes
		system_includes = ''
		if len(self.__system_includes) > 0:
			system_includes = ''.join(['#include <%s>\n' % path for path in self.__system_includes])

		user_includes = ''
		if len(self.__user_includes) > 0:
			user_includes = ''.join(['#include "%s"\n' % path for path in self.__user_includes])

		self._source = self._source.replace('{{{__WRAPPER_INCLUDES__}}}', system_includes + user_includes)

		# cast to
		self._source += self.get_type_tag_cast_function()

	def get_output(self):
		return self._header, self._source
