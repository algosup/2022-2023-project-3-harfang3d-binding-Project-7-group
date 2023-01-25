import lib

def bind_adder(gen):
    gen.add_include('./adder.h', True)
    gen.bind_function('adder', 'int', ['int a', 'int b'])
    gen.bind_function('adder', 'float', ['float a', 'float b'])
    

def bind_subtracter(gen):
    gen.add_include('./subtracter.h', True)
    gen.bind_function('subtracter', 'int', ['int a', 'int b'])
    gen.bind_function('subtracter', 'float', ['float a', 'float b'])

def bind(gen):
    gen.start('adder')
    lib.bind_defaults(gen)
    bind_adder(gen)
    bind_subtracter(gen)
    gen.finalize()
    return gen.get_output()