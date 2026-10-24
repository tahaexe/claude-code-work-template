// Stand-ins for the URP core library names a game's code shaders use, for `shader-kontrol.py`'s editor-free syntax and
// type check only (never compiled into a game). Precision as on desktop: half is float. A name a shader uses that is
// missing here fails as undeclared: add it (a project's copy keeps its own lines on a template update).
#define half float
#define half2 float2
#define half3 float3
#define half4 float4
#define TWO_PI 6.28318530718
#define PI 3.14159265359
#define UNITY_RAW_FAR_CLIP_VALUE (0.0)
#define TEXTURE2D(name) Texture2D name
#define SAMPLER(name) SamplerState name
#define LOAD_TEXTURE2D_LOD(tex, coord, lod) tex.Load(int3(coord, lod))
#define LOAD_TEXTURE2D(tex, coord) tex.Load(int3(coord, 0))
#define SAMPLE_TEXTURE2D(tex, samp, uv) tex.Sample(samp, uv)
#define CBUFFER_START(name) cbuffer name {
#define CBUFFER_END };

float4 _Time;
float4 _ProjectionParams;
float4 _ScreenParams;
float3 _WorldSpaceCameraPos;
float4x4 unity_ObjectToWorld;
float4x4 unity_WorldToObject;
float4x4 unity_MatrixVP;

float3 TransformObjectToWorld(float3 p) { return mul(unity_ObjectToWorld, float4(p, 1.0)).xyz; }
float3 TransformWorldToObject(float3 p) { return mul(unity_WorldToObject, float4(p, 1.0)).xyz; }
float4 TransformWorldToHClip(float3 p) { return mul(unity_MatrixVP, float4(p, 1.0)); }
float4 TransformObjectToHClip(float3 p) { return TransformWorldToHClip(TransformObjectToWorld(p)); }
float3 TransformObjectToWorldNormal(float3 n) { return normalize(mul(n, (float3x3)unity_WorldToObject)); }
float3 TransformWorldToObjectDir(float3 d) { return normalize(mul((float3x3)unity_WorldToObject, d)); }
float3 GetCameraPositionWS() { return _WorldSpaceCameraPos; }
float3 GetWorldSpaceNormalizeViewDir(float3 p) { return normalize(_WorldSpaceCameraPos - p); }

// Common URP names beyond the first game's (signatures as URP 17 declares them; added 2026-10-24 from three more games).
#define real float
#define real2 float2
#define real3 float3
#define real4 float4
#define TEXTURE2D_X(name) Texture2D name
#define SAMPLE_TEXTURE2D_X(tex, samp, uv) tex.Sample(samp, uv)
#define SAMPLE_TEXTURE2D_LOD(tex, samp, uv, lod) tex.SampleLevel(samp, uv, lod)
#define SAMPLE_TEXTURE2D_X_LOD(tex, samp, uv, lod) tex.SampleLevel(samp, uv, lod)
#define TRANSFORM_TEX(tex, name) ((tex.xy) * name##_ST.xy + name##_ST.zw)
#define UNITY_VERTEX_INPUT_INSTANCE_ID
#define UNITY_VERTEX_OUTPUT_STEREO
#define UNITY_SETUP_INSTANCE_ID(input)
#define UNITY_TRANSFER_INSTANCE_ID(input, output)
#define UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(output)
#define UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX(input)

float4x4 unity_MatrixV;
float4x4 unity_MatrixInvVP;
float4x4 glstate_matrix_projection;
#define UNITY_MATRIX_M unity_ObjectToWorld
#define UNITY_MATRIX_I_M unity_WorldToObject
#define UNITY_MATRIX_V unity_MatrixV
#define UNITY_MATRIX_P glstate_matrix_projection
#define UNITY_MATRIX_VP unity_MatrixVP
#define UNITY_MATRIX_I_VP unity_MatrixInvVP
float4 _ZBufferParams;
float4 unity_OrthoParams;
float4 _MainLightPosition;
half4 _MainLightColor;
TEXTURE2D_X(_BlitTexture);
float4 _BlitTexture_TexelSize;
float4 _BlitScaleBias;
SAMPLER(sampler_LinearClamp);
SAMPLER(sampler_PointClamp);
SAMPLER(sampler_LinearRepeat);
SAMPLER(sampler_PointRepeat);

struct VertexPositionInputs { float3 positionWS; float3 positionVS; float4 positionCS; float4 positionNDC; };
struct VertexNormalInputs { real3 tangentWS; real3 bitangentWS; float3 normalWS; };
struct Light { half3 direction; half3 color; float distanceAttenuation; half shadowAttenuation; uint layerMask; };

float3 TransformWorldToView(float3 p) { return mul(unity_MatrixV, float4(p, 1.0)).xyz; }
float3 TransformObjectToWorldDir(float3 d, bool doNormalize = true) { float3 w = mul((float3x3)unity_ObjectToWorld, d); return doNormalize ? normalize(w) : w; }
float3 GetWorldSpaceViewDir(float3 p) { return _WorldSpaceCameraPos - p; }
VertexPositionInputs GetVertexPositionInputs(float3 p) { VertexPositionInputs o; o.positionWS = TransformObjectToWorld(p); o.positionVS = TransformWorldToView(o.positionWS); o.positionCS = TransformWorldToHClip(o.positionWS); o.positionNDC = o.positionCS; return o; }
VertexNormalInputs GetVertexNormalInputs(float3 n) { VertexNormalInputs o; o.normalWS = TransformObjectToWorldNormal(n); o.tangentWS = float3(1, 0, 0); o.bitangentWS = float3(0, 1, 0); return o; }
VertexNormalInputs GetVertexNormalInputs(float3 n, float4 t) { VertexNormalInputs o = GetVertexNormalInputs(n); o.tangentWS = TransformObjectToWorldDir(t.xyz); o.bitangentWS = cross(o.normalWS, o.tangentWS) * t.w; return o; }
Light GetMainLight() { Light l; l.direction = _MainLightPosition.xyz; l.color = _MainLightColor.rgb; l.distanceAttenuation = 1.0; l.shadowAttenuation = 1.0; l.layerMask = 0xFFFFFFFF; return l; }
Light GetMainLight(float4 shadowCoord) { return GetMainLight(); }
Light GetMainLight(float4 shadowCoord, float3 positionWS, half4 shadowMask) { return GetMainLight(); }
int GetAdditionalLightsCount() { return 0; }
Light GetAdditionalLight(uint i, float3 positionWS) { return GetMainLight(); }
Light GetAdditionalLight(uint i, float3 positionWS, half4 shadowMask) { return GetMainLight(); }
float4 TransformWorldToShadowCoord(float3 positionWS) { return float4(positionWS, 1.0); }
half3 SampleSH(half3 normalWS) { return half3(0.5, 0.5, 0.5); }
half ComputeFogFactor(float z) { return z; }
half3 MixFog(half3 color, half fogFactor) { return color; }
half3 SRGBToLinear(half3 c) { return pow(abs(c), 2.2); }
half4 SRGBToLinear(half4 c) { return half4(SRGBToLinear(c.rgb), c.a); }
half3 LinearToSRGB(half3 c) { return pow(abs(c), 1.0 / 2.2); }
half4 LinearToSRGB(half4 c) { return half4(LinearToSRGB(c.rgb), c.a); }
float Linear01Depth(float depth, float4 zBufferParam) { return 1.0 / (zBufferParam.x * depth + zBufferParam.y); }
float LinearEyeDepth(float depth, float4 zBufferParam) { return 1.0 / (zBufferParam.z * depth + zBufferParam.w); }
float2 GetNormalizedScreenSpaceUV(float4 positionCS) { return positionCS.xy * _ScreenParams.zw - positionCS.xy; }
float4 ComputeScreenPos(float4 positionCS) { return positionCS * 0.5; }
float SampleSceneDepth(float2 uv) { return uv.x; }
#define UNITY_NEAR_CLIP_VALUE (1.0)
float4 unity_RendererUserValue;
float3 SafeNormalize(float3 v) { return v * rsqrt(max(1e-12, dot(v, v))); }
float3 ComputeWorldSpacePosition(float2 positionNDC, float deviceDepth, float4x4 invViewProjMatrix) { float4 p = mul(invViewProjMatrix, float4(positionNDC * 2.0 - 1.0, deviceDepth, 1.0)); return p.xyz / p.w; }
float3 GetAbsolutePositionWS(float3 positionRWS) { return positionRWS; }
float GetCurrentExposureMultiplier() { return 1.0; }
