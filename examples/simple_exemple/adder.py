import lib

def bind(gen):
    gen.start('adder')
    gen.add_include('./adder.h', True)
    lib.bind_defaults(gen)
    gen.bind_function('adder', 'int', ['int a', 'int b'])
    gen.bind_function('adder', 'float', ['float a', 'float b'])
    gen.finalize()
    return gen.get_output()