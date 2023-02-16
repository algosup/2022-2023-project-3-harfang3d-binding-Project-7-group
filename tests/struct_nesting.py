import lib


def bind_test(gen):
	gen.start('my_test')

	lib.bind_defaults(gen)

	# inject test code in the wrapper
	gen.insert_code('''\
struct nested_struct {
	int v{8};
};

struct enclosing_struct {
	nested_struct n;
};
''', True, False)

	nested_struct = gen.begin_class('nested_struct')
	gen.bind_constructor(nested_struct, [])
	gen.bind_member(nested_struct, 'int v')
	gen.end_class(nested_struct)

	enclosing_struct = gen.begin_class('enclosing_struct')
	gen.bind_constructor(enclosing_struct, [])
	gen.bind_member(enclosing_struct, 'nested_struct n')
	gen.end_class(enclosing_struct)

	gen.finalize()
	return gen.get_output()


test_python = '''\
import my_test

#
n = my_test.nested_struct()
assert n.v == 8
n.v -= 4
assert n.v == 4

#
e = my_test.enclosing_struct()
assert e.n.v == 8
e.n.v = 12
assert e.n.v == 12
e.n.v *= 4
assert e.n.v == 48
e.n.v //= 2
assert e.n.v == 24
'''

test_lua = '''\
my_test = require "my_test"

--
n = my_test.nested_struct()
assert(n.v == 8)
n.v = n.v - 4
assert(n.v == 4)

--
e = my_test.enclosing_struct()
assert(e.n.v == 8)
e.n.v = 12
assert(e.n.v == 12)
e.n.v = e.n.v * 4
assert(e.n.v == 48)
e.n.v = e.n.v / 2
assert(e.n.v == 24)
'''

test_go = '''\
package mytest

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Test ...
func Test(t *testing.T) {
	n := NewNestedStruct()
	assert.Equal(t, n.GetV(), int32(8), "should be the same.")
	n.SetV(n.GetV() - 4)
	assert.Equal(t, n.GetV(), int32(4), "should be the same.")

	//
	e := NewEnclosingStruct()
	assert.Equal(t, e.GetN().GetV(), int32(8), "should be the same.")
	e.GetN().SetV(12)
	assert.Equal(t, e.GetN().GetV(), int32(12), "should be the same.")
	e.GetN().SetV(e.GetN().GetV() * 4)
	assert.Equal(t, e.GetN().GetV(), int32(48), "should be the same.")
	e.GetN().SetV(e.GetN().GetV() / 2)
	assert.Equal(t, e.GetN().GetV(), int32(24), "should be the same.")
}
'''

test_rust = '''\
mod my_test;

#[test]
fn test() {
	unsafe {
		let n = my_test::MyTestConstructorNestedStruct();
		assert_eq!(my_test::MyTestNestedStructGetV(n), 8);
		my_test::MyTestNestedStructSetV(n, my_test::MyTestNestedStructGetV(n) - 4);
		assert_eq!(my_test::MyTestNestedStructGetV(n), 4);

		//
		let e = my_test::MyTestConstructorEnclosingStruct();
		assert_eq!(my_test::MyTestNestedStructGetV(my_test::MyTestEnclosingStructGetN(e)), 8);
		my_test::MyTestNestedStructSetV(my_test::MyTestEnclosingStructGetN(e),12);
		assert_eq!(my_test::MyTestNestedStructGetV(my_test::MyTestEnclosingStructGetN(e)), 12);
		my_test::MyTestNestedStructSetV(my_test::MyTestEnclosingStructGetN(e),my_test::MyTestNestedStructGetV(my_test::MyTestEnclosingStructGetN(e)) * 4);
		assert_eq!(my_test::MyTestNestedStructGetV(my_test::MyTestEnclosingStructGetN(e)), 48);
		my_test::MyTestNestedStructSetV(my_test::MyTestEnclosingStructGetN(e),my_test::MyTestNestedStructGetV(my_test::MyTestEnclosingStructGetN(e)) / 2);
		assert_eq!(my_test::MyTestNestedStructGetV(my_test::MyTestEnclosingStructGetN(e)), 24);
	}
}
'''