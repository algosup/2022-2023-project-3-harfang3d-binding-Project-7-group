import lang.cpython

import lib.std
import lib.stl
import lib
import copy

######## helpers ########
def check_bool_rval_lambda(gen, msg):
	return lambda rvals, ctx: 'if (!%s) {\n%s}\n' % (rvals[0], gen.proxy_call_error(msg, ctx))


def route_lambda(name):
	return lambda args: '%s(%s);' % (name, ', '.join(args))

# TODO: rework this
def bind_std_vector(gen, T_conv, bound_name=None):
	if gen.get_language() == 'CPython':
		PySequence_T_type = 'PySequenceOf%s' % T_conv.bound_name
		gen.bind_type(lib.cpython.stl.PySequenceToStdVectorConverter(PySequence_T_type, T_conv))
	elif gen.get_language() == 'Lua':
		LuaTable_T_type = 'LuaTableOf%s' % T_conv.bound_name
		gen.bind_type(lib.lua.stl.LuaTableToStdVectorConverter(LuaTable_T_type, T_conv))
	elif gen.get_language() == 'Go':
		GoTable_T_type = 'GoSliceOf%s' % T_conv.bound_name
		gen.bind_type(lib.go.stl.GoSliceToStdVectorConverter(GoTable_T_type, T_conv))

	if bound_name is None:
		bound_name = '%sList' % T_conv.bound_name

	conv = gen.begin_class('std::vector<%s>' % T_conv.ctype, bound_name=bound_name, features={'sequence': lib.std.VectorSequenceFeature(T_conv)})
	if gen.get_language() == 'CPython':
		gen.bind_constructor(conv, ['?%s sequence' % PySequence_T_type])
	elif gen.get_language() == 'Lua':
		gen.bind_constructor(conv, ['?%s sequence' % LuaTable_T_type])
	elif gen.get_language() == 'Go':
		gen.bind_constructor(conv, ['?%s sequence' % GoTable_T_type])

	def validate_std_vector_at_idx(gen, var, ctx):
		out = 'if ((_self->size() == 0) || (%s >= _self->size())) {\n' % var
		out += gen.proxy_call_error("Invalid index", ctx)
		out += '}\n'
		return out

	gen.bind_method(conv, 'clear', 'void', [])
	gen.bind_method(conv, 'reserve', 'void', ['size_t size'])
	gen.bind_method(conv, 'push_back', 'void', ['%s v' % T_conv.ctype])
	gen.bind_method(conv, 'size', 'size_t', [])
	gen.bind_method(conv, 'at', repr(T_conv.ctype), ['size_t idx'], features={'validate_arg_in': [validate_std_vector_at_idx]})

	gen.end_class(conv)
	return conv

# TODO: figure out what this is
def insert_non_embedded_setup_free_code(gen):
	if gen.get_language() == 'CPython':
		gen.insert_binding_code('''
#include "foundation/log.h"
#include <iostream>

static void OnHarfangLog(const char *msg, int mask, const char *details, void *user) {
	if (mask & hg::LL_Error)
		PyErr_SetString(PyExc_RuntimeError, msg);
	else if (mask & hg::LL_Warning)
		PyErr_WarnEx(PyExc_Warning, msg, 1);
	else
		std::cout << msg << std::endl;
}

static void InstallLogHook() { hg::set_log_hook(OnHarfangLog, nullptr); }
''')
	elif gen.get_language() == 'Lua':
		gen.insert_binding_code('''
''')

	gen.insert_binding_code('''
#include "foundation/build_info.h"

static void OutputLicensingTerms(const char *lang) {
	hg::log(
		hg::format("Harfang %1 for %2 on %3 (build %4 %5 %6)")
		.arg(hg::get_version_string()).arg(lang).arg(hg::get_target_string())
		.arg(hg::get_build_sha()).arg(__DATE__).arg(__TIME__)
	);
	hg::log("See https://www.harfang3d.com/license for licensing terms");
}
''')

	if gen.get_language() == 'Lua':
		gen.add_custom_init_code('OutputLicensingTerms("Lua 5.3");\n')
	elif gen.get_language() == 'CPython':
		gen.add_custom_init_code('''
InstallLogHook();
OutputLicensingTerms("CPython 3.2+");
''')

	gen.add_custom_free_code('\n')

######## bindings ########
def bind_input(gen):
	gen.add_include('platform/input_system.h')

	gen.bind_function('hg::InputInit', 'void', [])
	gen.bind_function('hg::InputShutdown', 'void', [])

	keyboard = gen.begin_class('hg::Keyboard')
	gen.bind_constructor(keyboard, ['?const char *name'])
	gen.bind_method(keyboard, 'Down', 'bool', ['hg::Key key'])
	gen.bind_method(keyboard, 'Pressed', 'bool', ['hg::Key key'])
	gen.bind_method(keyboard, 'Released', 'bool', ['hg::Key key'])
	gen.bind_method(keyboard, 'Update', 'void', [])
	gen.end_class(keyboard)

	mouse = gen.begin_class('hg::Mouse')
	gen.bind_constructor(mouse, ['?const char *name'])
	gen.bind_method(mouse, 'X', 'int', [])
	gen.bind_method(mouse, 'Y', 'int', [])
	gen.bind_method(mouse, 'Update', 'void', [])
	gen.end_class(mouse)

	gen.bind_named_enum('hg::Key', [
		'K_Space', 'K_Escape', 'K_S', 'K_W', 'K_X'
	])

def bind_window_system(gen):
	gen.add_include('platform/window_system.h')

	gen.bind_function('hg::WindowSystemInit', 'void', [])
	gen.bind_function('hg::WindowSystemShutdown', 'void', [])
	gen.bind_function('hg::DestroyWindow', 'bool', ['const hg::Window *window'])
	gen.bind_function('hg::IsWindowOpen', 'bool', ['const hg::Window *window'])
	gen.bind_function('hg::UpdateWindow', 'bool', ['const hg::Window *window'])
	gen.bind_ptr('hg::Window *', bound_name='Window')

def bind_audio(gen):
	gen.add_include('engine/audio_stream_interface.h')

	gen.bind_function('hg::AudioInit', 'bool', [])
	gen.bind_function('hg::AudioShutdown', 'void', [])
	gen.bind_function('hg::LoadOGGSoundFile', 'hg::SoundRef', ['const char *path'], {'rval_constants_group': 'SoundRef'})
	gen.bind_function('hg::PlayStereo', 'hg::SourceRef', ['hg::SoundRef snd', 'const hg::StereoSourceState &state'], {'rval_constants_group': 'SourceRef', 'constants_group': {'snd': 'SoundRef'}})

	gen.bind_named_enum('hg::SourceRepeat', ['SR_Loop'])

	# Lets hope this isn't going to break everything
	gen.insert_binding_code('''
static hg::StereoSourceState *__ConstructStereoSourceState(float volume = 1.f, hg::SourceRepeat repeat = hg::SR_Once, float panning = 0.f) {
	return new hg::StereoSourceState{volume, repeat, panning};
}

static hg::SpatializedSourceState *__ConstructSpatializedSourceState(hg::Mat4 mtx = hg::Mat4::Identity, float volume = 1.f, hg::SourceRepeat repeat = hg::SR_Once, const hg::Vec3 &vel = {}) {
	return new hg::SpatializedSourceState{mtx, volume, repeat, vel};
}
''')

	stereo_source_state = gen.begin_class('hg::StereoSourceState')
	gen.bind_members(stereo_source_state, ['float volume', 'hg::SourceRepeat repeat', 'float panning'])
	gen.bind_constructor(stereo_source_state, ['?float volume', '?hg::SourceRepeat repeat', '?float panning'], {'route': route_lambda('__ConstructStereoSourceState')})
	gen.end_class(stereo_source_state)

def bind_render(gen):
	gen.add_include('engine/render_pipeline.h')

	gen.bind_named_enum('bgfx::RendererType::Enum', [
		'Noop', 'Direct3D9', 'Direct3D11', 'Direct3D12', 'Gnm', 'Metal', 'Nvn', 'OpenGLES', 'OpenGL', 'Vulkan', 'Count'
	], bound_name='RendererType', prefix='RT_')

	gen.bind_named_enum('bgfx::TextureFormat::Enum', [
		'BC1', 'BC2', 'BC3', 'BC4', 'BC5', 'BC6H', 'BC7', 'ETC1', 'ETC2', 'ETC2A', 'ETC2A1', 'PTC12', 'PTC14', 'PTC12A', 'PTC14A', 'PTC22', 'PTC24',
		'ATC', 'ATCE', 'ATCI', 'ASTC4x4', 'ASTC5x5', 'ASTC6x6', 'ASTC8x5', 'ASTC8x6', 'ASTC10x5',
		'Unknown',
		'R1', 'A8', 'R8', 'R8I', 'R8U', 'R8S', 'R16', 'R16I', 'R16U', 'R16F', 'R16S', 'R32I', 'R32U', 'R32F', 'RG8', 'RG8I', 'RG8U', 'RG8S',
		'RG16', 'RG16I', 'RG16U', 'RG16F', 'RG16S', 'RG32I', 'RG32U', 'RG32F', 'RGB8', 'RGB8I', 'RGB8U', 'RGB8S', 'RGB9E5F', 'BGRA8', 'RGBA8',
		'RGBA8I', 'RGBA8U', 'RGBA8S', 'RGBA16', 'RGBA16I', 'RGBA16U', 'RGBA16F', 'RGBA16S', 'RGBA32I', 'RGBA32U', 'RGBA32F', 'R5G6B5', 'RGBA4',
		'RGB5A1', 'RGB10A2', 'RG11B10F',
		'UnknownDepth',
		'D16', 'D24', 'D24S8', 'D32', 'D16F', 'D24F', 'D32F', 'D0S8',
	], bound_name='TextureFormat', prefix='TF_')

	gen.bind_named_enum('bgfx::Attrib::Enum', ['Position', 'Normal', 'Tangent', 'Bitangent', 'Color0', 'Color1', 'Color2', 'Color3', 'Indices', 'Weight',
		'TexCoord0', 'TexCoord1', 'TexCoord2', 'TexCoord3', 'TexCoord4', 'TexCoord5', 'TexCoord6', 'TexCoord7'
	], bound_name='Attrib', prefix='A_')
	gen.bind_named_enum('bgfx::AttribType::Enum', ['Uint8', 'Uint10', 'Int16', 'Half', 'Float'], bound_name='AttribType', prefix='AT_')

	vtx_decl = gen.begin_class('bgfx::VertexLayout')
	gen.bind_constructor(vtx_decl, [])
	gen.bind_method(vtx_decl, 'begin', 'bgfx::VertexLayout &', [], bound_name='Begin')
	gen.bind_method(vtx_decl, 'add', 'bgfx::VertexLayout &', ['bgfx::Attrib::Enum attrib', 'uint8_t count', 'bgfx::AttribType::Enum type', '?bool normalized', '?bool as_int'], bound_name='Add')
	gen.bind_method(vtx_decl, 'skip', 'bgfx::VertexLayout &', ['uint8_t size'], bound_name='Skip')
	gen.bind_method(vtx_decl, 'end', 'void', [], bound_name='End')
	gen.bind_method(vtx_decl, 'has', 'bool', ['bgfx::Attrib::Enum attrib'], bound_name='Has')
	gen.bind_method(vtx_decl, 'getOffset', 'uint16_t', ['bgfx::Attrib::Enum attrib'], bound_name='GetOffset')
	gen.bind_method(vtx_decl, 'getStride', 'uint16_t', [], bound_name='GetStride')
	gen.bind_method(vtx_decl, 'getSize', 'uint32_t', ['uint32_t count'], bound_name='GetSize')
	gen.end_class(vtx_decl)

	bgfx_program_handle = gen.begin_class('bgfx::ProgramHandle')
	bgfx_program_handle._inline = True
	gen.end_class(bgfx_program_handle)

	render_state = gen.begin_class('hg::RenderState')
	gen.end_class(render_state)

	pprogram_ref = gen.begin_class('hg::PipelineProgramRef')
	pprogram_ref._inline = True
	#gen.bind_comparison_ops(pprogram_ref, ['==', '!='], ['const hg::PipelineProgramRef &p'])
	gen.end_class(pprogram_ref)

	pipeline_info = gen.begin_class('hg::PipelineInfo')
	gen.bind_member(pipeline_info, 'std::string name')
	gen.end_class(pipeline_info)

	material = gen.begin_class('hg::Material')
	gen.bind_constructor(material, [])
	gen.end_class(material)
	bind_std_vector(gen, material)

	# frame
	fbh = gen.begin_class('bgfx::FrameBufferHandle')
	gen.end_class(fbh)

	# Overloads here are funky, I'm only guessing
	gen.bind_function('hg::RenderInit', 'hg::Window *', ['const char *window_title', 'int width', 'int height', 'bgfx::RendererType::Enum type', '?uint32_t reset_flags', '?bgfx::TextureFormat::Enum format', '?uint32_t debug_flags'], {'constants_group': {'reset_flags': 'ResetFlags', 'debug_flags': 'DebugFlags'}})
	gen.bind_function('hg::RenderShutdown', 'void', [])

	pipe_res = gen.begin_class('hg::PipelineResources')
	gen.bind_constructor(pipe_res, [])
	gen.bind_method(pipe_res, 'AddModel', 'hg::ModelRef', ['const char *name', 'const hg::Model &mdl'], {'route': route_lambda('_PipelineResources_AddModel')})
	gen.end_class(pipe_res)

	gen.bind_function('hg::VertexLayoutPosFloatNormUInt8', 'bgfx::VertexLayout', [])
	gen.bind_function('hg::VertexLayoutPosFloatColorFloat', 'bgfx::VertexLayout', [])

	gen.bind_function('hg::CreateSphereModel', 'hg::Model', ['const bgfx::VertexLayout &decl', 'float radius', 'int subdiv_x', 'int subdiv_y'])
	gen.bind_function('hg::LoadProgramFromAssets', 'bgfx::ProgramHandle', ['const char *name'])
	gen.bind_function('hg::ComputeRenderState', 'hg::RenderState', ['hg::BlendMode blend', '?hg::DepthTest depth_test', '?hg::FaceCulling culling', '?bool write_z', '?bool write_r', '?bool write_g', '?bool write_b', '?bool write_a'])
	gen.bind_function('hg::LoadPipelineProgramRefFromAssets', 'hg::PipelineProgramRef', ['const char *name', 'hg::PipelineResources &resources', 'const hg::PipelineInfo &pipeline'], [])
	gen.bind_function('hg::GetForwardPipelineInfo', 'const hg::PipelineInfo &', [])
	gen.bind_function('hg::CreateMaterial', 'hg::Material', ['hg::PipelineProgramRef prg', 'const char *value_name_0', 'const hg::Vec4 &value_0', 'const char *value_name_1', 'const hg::Vec4 &value_1'])

	vertices = gen.begin_class('hg::Vertices')
	gen.bind_constructor(vertices, ['const bgfx::VertexLayout &decl', 'size_t count'])
	gen.bind_method(vertices, 'Begin', 'hg::Vertices &', ['size_t vertex_index'])
	gen.bind_method(vertices, 'SetPos', 'hg::Vertices &', ['const hg::Vec3 &pos'])
	gen.bind_method(vertices, 'SetColor0', 'hg::Vertices &', ['const hg::Color &color'])
	gen.bind_method(vertices, 'End', 'void', ['?bool validate'])
	gen.end_class(vertices)

	gen.bind_function('hg::DrawLines', 'void', ['bgfx::ViewId view_id', 'const hg::Vertices &vtx', 'bgfx::ProgramHandle prg', '?hg::RenderState render_state', '?uint32_t depth'])
	gen.bind_function('hg::CreateCubeModel', 'hg::Model', ['const bgfx::VertexLayout &decl', 'float x', 'float y', 'float z'])
	gen.bind_function('hg::SetView2D', 'void', ['bgfx::ViewId id', 'int x', 'int y', 'int res_x', 'int res_y', 'float znear', 'float zfar', 'uint16_t flags', 'const hg::Color &color', 'float depth', 'uint8_t stencil', '?bool y_up'], {'constants_group': {'flags': 'ClearFlags'}})

	gen.bind_named_enum('hg::BlendMode', ['BM_Alpha'])
	gen.bind_named_enum('hg::DepthTest', ['DT_Less'])
	gen.bind_named_enum('hg::FaceCulling', ['FC_Disabled'])

	gen.bind_constants('uint16_t', [
		("CF_Depth", "BGFX_CLEAR_DEPTH"),
	], 'ClearFlags')

	gen.bind_function('bgfx::frame', 'uint32_t', [], bound_name='Frame')

	model_ref = gen.begin_class('hg::ModelRef')
	model_ref._inline = True
	#gen.bind_comparison_ops(model_ref, ['==', '!='], ['const hg::ModelRef &m'])
	gen.end_class(model_ref)

	mdl = gen.begin_class('hg::Model')
	gen.end_class(mdl)

	pipeline = gen.begin_class('hg::Pipeline')
	gen.end_class(pipeline)

def bind_scene(gen):
	gen.add_include('engine/scene.h')

	scene = gen.begin_class('hg::Scene', noncopyable=True)
	gen.bind_constructor(scene, [])
	gen.bind_method(scene, 'SetCurrentCamera', 'void', ['const hg::Node &camera'])
	gen.end_class(scene)

	node = gen.begin_class('hg::Node')
	node._inline = True
	gen.bind_method(node, 'GetTransform', 'hg::Transform', [])
	gen.end_class(node)
	bind_std_vector(gen, node)

	gen.bind_function('hg::CreateInstanceFromAssets', 'hg::Node', ['hg::Scene &scene', 'const hg::Mat4 &mtx', 'const std::string &name', 'hg::PipelineResources &resources', 'const hg::PipelineInfo &pipeline', 'bool &success', '?uint32_t flags'], {'constants_group': {'flags': 'LoadSaveSceneFlags'}, 'arg_out': ['success']})

	transform = gen.begin_class('hg::Transform')
	gen.bind_method(transform, 'GetPos', 'hg::Vec3', [])
	gen.bind_method(transform, 'SetPos', 'void', ['const hg::Vec3 &T'])
	gen.bind_method(transform, 'GetRot', 'hg::Vec3', [])
	gen.bind_method(transform, 'SetRot', 'void', ['const hg::Vec3 &R'])
	gen.bind_method(transform, 'GetWorld', 'hg::Mat4', [])
	gen.end_class(transform)

	gen.bind_function('hg::CreateCamera', 'hg::Node', ['hg::Scene &scene', 'const hg::Mat4 &mtx', 'float znear', 'float zfar', '?float fov'])
	gen.bind_function('hg::CreatePhysicCube', 'hg::Node', ['hg::Scene &scene', 'const hg::Vec3 &size', 'const hg::Mat4 &mtx', 'const hg::ModelRef &model_ref', 'std::vector<hg::Material> &materials', 'float mass'])
	gen.bind_function('hg::CreatePhysicSphere', 'hg::Node', ['hg::Scene &scene', 'float radius', 'const hg::Mat4 &mtx', 'const hg::ModelRef &model_ref', 'std::vector<hg::Material> &materials', 'float mass'])

	# This overload is sus because it got an extra input
	gen.bind_function('hg::SubmitSceneToPipeline', 'void', ['bgfx::ViewId &view_id', 'const hg::Scene &scene', 'const hg::Rect<int> &rect', 'bool fov_axis_is_horizontal', 'const hg::ForwardPipeline &pipeline', 'const hg::PipelineResources &resources', 'const hg::SceneForwardPipelinePassViewId &views', '?bgfx::FrameBufferHandle fb', '?const char *debug_name'], {'arg_in_out': ['view_id'], 'arg_out': ['views']})

	# This was bigger normally, might had stuff there we need
	gen.insert_binding_code('''
#include "foundation/data_rw_interface.h"
#include "foundation/file_rw_interface.h"

#include "engine/assets_rw_interface.h"

static bool _LoadSceneFromAssets(const char *name, hg::Scene &scene, hg::PipelineResources &resources, const hg::PipelineInfo &pipeline, uint32_t flags = LSSF_All) {
	hg::LoadSceneContext ctx;
	return hg::LoadSceneFromAssets(name, scene, resources, pipeline, ctx, flags);
}
''')
	gen.bind_function('_LoadSceneFromAssets', 'bool', ['const char *name', 'hg::Scene &scene', 'hg::PipelineResources &resources', 'const hg::PipelineInfo &pipeline', '?uint32_t flags'], {'constants_group': {'flags': 'LoadSaveSceneFlags'}}, bound_name = 'LoadSceneFromAssets')

	sfppo = gen.begin_class('hg::SceneForwardPipelinePassViewId')
	gen.bind_constructor(sfppo, [])
	gen.end_class(sfppo)

def bind_forward_pipeline(gen):
	gen.add_include('engine/forward_pipeline.h')

	forward_pipeline = gen.begin_class('hg::ForwardPipeline')
	gen.add_base(forward_pipeline, gen.get_conv('hg::Pipeline'))
	gen.end_class(forward_pipeline)
	
	gen.bind_function('hg::CreateForwardPipeline', 'hg::ForwardPipeline', ['?int shadow_map_resolution', '?bool spot_16bit_shadow_map'])

def bind_assets(gen):
	gen.add_include('engine/assets.h')

	gen.bind_function('hg::AddAssetsFolder', 'bool', ['const char *path'])

def bind_math(gen):
	# hg::Vec4
	gen.add_include('foundation/vector4.h')
	gen.add_include('foundation/vector3.h')
	gen.add_include('foundation/matrix3.h')
	gen.add_include('foundation/matrix4.h')

	# Come back here if we need arithmetical stuff
	vector4 = gen.begin_class('hg::Vec4')
	vector4._inline = True
	gen.bind_members(vector4, ['float x', 'float y', 'float z', 'float w'])
	gen.bind_constructor(vector4, ['float x', 'float y', 'float z', '?float w'])
	gen.end_class(vector4)

	# Come back here if we need arithmetical stuff
	vector3 = gen.begin_class('hg::Vec3')
	vector3._inline = True
	#gen.bind_static_members(vector3, ['const hg::Vec3 Zero', 'const hg::Vec3 One', 'const hg::Vec3 Left', 'const hg::Vec3 Right', 'const hg::Vec3 Up', 'const hg::Vec3 Down', 'const hg::Vec3 Front', 'const hg::Vec3 Back'])
	gen.bind_members(vector3, ['float x', 'float y', 'float z'])
	gen.bind_constructor(vector3, ['float x', 'float y', 'float z']) # Will need to change line 126 of example to avoid other constructor overload
	gen.end_class(vector3)

	# Come back here if we need arithmetical stuff
	# This isn't actually created anywhere in the example, its just returned by other functions/methods
	matrix3 = gen.begin_class('hg::Mat3')
	#gen.bind_static_members(matrix3, ['const hg::Mat3 Zero', 'const hg::Mat3 Identity'])
	gen.bind_constructor(matrix3, [])
	gen.end_class(matrix3)

	matrix4 = gen.begin_class('hg::Mat4')
	#gen.bind_static_members(matrix4, ['const hg::Mat4 Zero', 'const hg::Mat4 Identity'])
	gen.insert_binding_code('static hg::Mat4 *_Mat4_Copy(const hg::Mat4 &m) { return new hg::Mat4(m); }')
	gen.bind_constructor(matrix4, [])
	gen.end_class(matrix4)

	gen.bind_function('hg::Vec4I', 'hg::Vec4', ['int x', 'int y', 'int z', '?int w'])

	gen.add_include('foundation/rect.h')	# Not sure if we need this
	gen.add_include('foundation/math.h')
	gen.add_include('foundation/vector2.h')

	gen.bind_function('hg::TranslationMat4', 'hg::Mat4', ['const hg::Vec3 &t'])
	gen.bind_function('hg::TransformationMat4', 'hg::Mat4', ['const hg::Vec3 &pos', 'const hg::Vec3 &rot', '?const hg::Vec3 &scale'])
	gen.bind_function('hg::GetZ', 'hg::Vec3', ['const hg::Mat3 &m'])

	# This one got a ton of overloads but I think we only use this one
	gen.bind_function('hg::Clamp', 'float', ['float v', 'float min', 'float max'])
	gen.bind_function('hg::ToEuler', 'hg::Vec3', ['const hg::Mat3 &m'])
	gen.bind_function('hg::Mat3LookAt', 'hg::Mat3', ['const hg::Vec3 &front', '?const hg::Vec3 &up'])

	gen.bind_function('hg::Normalize', 'hg::Vec3', ['const hg::Vec3 &v'])

	vector2 = gen.begin_class('hg::tVec2<float>', bound_name='Vec2')
	vector2._inline = True
	# gen.bind_static_members(vector2, ['const hg::tVec2<float> Zero', 'const hg::tVec2<float> One'])
	# gen.bind_members(vector2, ['float x', 'float y'])
	gen.bind_constructor(vector2, [])
	gen.insert_binding_code('static void _Vector2_float_Set(hg::tVec2<float> *v, float x, float y) { v->x = x; v->y = y; }')
	gen.bind_method(vector2, 'Set', 'void', ['float x', 'float y'], {'route': route_lambda('_Vector2_float_Set')})
	gen.end_class(vector2)

	rect = gen.begin_class('hg::Rect<int>', bound_name='IntRect')
	rect._inline = True
	gen.bind_members(rect, ['int sx', 'int sy', 'int ex', 'int ey'])
	gen.bind_constructor(rect, [])
	gen.end_class(rect)

def bind_bullet3_physics(gen):
	gen.add_include('engine/scene_bullet3_physics.h')

	bullet = gen.begin_class('hg::SceneBullet3Physics', noncopyable=True)
	gen.bind_constructor(bullet, ['?int thread_count'])
	gen.bind_method(bullet, 'SceneCreatePhysicsFromAssets', 'void', ['const hg::Scene &scene'])
	gen.bind_method(bullet, 'NodeCreatePhysicsFromAssets', 'void', ['const hg::Node &node'])
	gen.bind_method(bullet, 'NodeAddImpulse', 'void', ['const hg::Node &node', 'const hg::Vec3 &dt_velocity', '?const hg::Vec3 &world_pos'])
	gen.end_class(bullet)

def bind_scene_systems(gen):
	gen.add_include('engine/scene_systems.h')

	scene_clocks = gen.begin_class('hg::SceneClocks')
	gen.bind_constructor(scene_clocks, [])
	gen.end_class(scene_clocks)

	gen.bind_function_overloads('hg::SceneUpdateSystems', 'void', ['hg::Scene &scene', 'hg::SceneClocks &clocks', 'hg::time_ns dt', 'hg::SceneBullet3Physics &physics', 'hg::time_ns step', 'int max_physics_step'])

def bind_time(gen):
	gen.add_include('foundation/time.h')
	gen.typedef('hg::time_ns', 'int64_t')

	gen.bind_function('hg::time_from_sec_f', 'hg::time_ns', ['float sec'])

def bind_projection(gen):
	gen.add_include('foundation/projection.h')

	gen.bind_function('hg::ComputeAspectRatioX', 'hg::tVec2<float>', ['float width', 'float height'])

def bind_color(gen):
	gen.add_include('foundation/color.h')

	color = gen.begin_class('hg::Color')
	color._inline = True  # use inline alloc where possible
	gen.bind_static_members(color, ['const hg::Color White', 'const hg::Color Black'])
	gen.bind_constructor(color, ['const hg::Color &color'])
	gen.end_class(color)

######## main ########
def bind(gen):
	gen.start('harfang')

	lib.bind_defaults(gen)

	gen.add_include('foundation/cext.h')

	if not gen.embedded:
		insert_non_embedded_setup_free_code(gen)

	void_ptr = gen.bind_ptr('void *', bound_name='VoidPointer')
	gen.insert_binding_code('static void * _int_to_VoidPointer(intptr_t ptr) { return reinterpret_cast<void *>(ptr); }')
	gen.bind_function('int_to_VoidPointer', 'void *', ['intptr_t ptr'], {'route': route_lambda('_int_to_VoidPointer')})
		
	gen.typedef('bgfx::ViewId', 'uint16_t')

	bind_std_vector(gen, gen.get_conv('int'))
	bind_std_vector(gen, gen.get_conv('uint16_t'))
	bind_std_vector(gen, gen.get_conv('uint32_t'))
	bind_std_vector(gen, gen.get_conv('std::string'), 'StringList')

	bind_time(gen)
	bind_assets(gen)
	bind_math(gen)
	bind_projection(gen)
	bind_window_system(gen)
	bind_color(gen)
	bind_render(gen)
	bind_forward_pipeline(gen)
	bind_scene(gen)
	if gen.defined('HG_ENABLE_BULLET3_SCENE_PHYSICS'):
		bind_bullet3_physics(gen)
	bind_scene_systems(gen)
	bind_input(gen)
	bind_audio(gen)

	gen.finalize()