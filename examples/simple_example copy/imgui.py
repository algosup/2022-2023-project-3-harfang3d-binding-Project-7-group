import lib

def bind(gen):
    gen.start('imgui')
    gen.add_include('./imgui.h', True)
    lib.bind_defaults(gen)
    gen.bind_function('createwindow','void',[])
    gen.bind_function('initializeDirectX','int',[]) 
    gen.bind_function('displayWindow','void',[])
    gen.bind_function('setupImGui','void',[])
    gen.bind_function('pollbackend','bool',[])
    gen.bind_function('createframe','void',[])
    gen.bind_function('showwindow','void',[])
    gen.bind_function('displaysimplewindow','void',[])
    gen.bind_function('otherwindow','void',[])
    gen.bind_function('RenderFrame','void',[])
    gen.bind_function('WaitForLastSubmittedFrame','void',[])
    gen.bind_function('Cleanall','void',[])

    gen.finalize()
    return gen.get_output()