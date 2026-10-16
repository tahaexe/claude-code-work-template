---
paths:
  - "**/*.shader"
  - "**/*.hlsl"
  - "**/*.cginc"
  - "**/*.shadergraph"
  - "**/*.shadersubgraph"
---
# Unity shader rules
<!-- unity add-on v1.14 · paths fitted to the project at install -->

- **Skills:** custom Shader Graph node → `unity:shader-graph-create-custom-node`; post-processing → `unity:urp-postprocessing`; URP renderer feature → `unity:validate-urp-render-graph-renderer-feature`.
- **Naming:** Shader Graph `SG_<Category>_<Name>` (e.g. `SG_Env_Water`); code shaders use the menu path `Shader "Game/<Category>/<Name>"`. The name states the purpose.
- **Code quality:** descriptive parameter names grouped with `[Header]`; no magic numbers (named constants or documented parameters); comments on math-heavy parts; a purpose comment at the top of the file.
- **Performance:** each shader states its target platform and complexity budget. `half` precision on mobile unless more is needed. Fewer texture samples in fragment shaders; `step()`, `lerp()`, `smoothstep()` instead of dynamic branching; no texture samples inside loops; blur in two passes (horizontal + vertical).
- **URP:** material properties inside `CBUFFER_START(UnityPerMaterial)` for SRP Batcher compatibility. Don't mix shaders of different render pipelines in one folder; document the target pipeline.
- **Variants:** keep the variant count minimal; `shader_feature` instead of `multi_compile` for material-only features; document each keyword's purpose; strip unused variants in builds and track the total variant count.
- **Platforms:** test on the lowest target hardware; provide a simple fallback for low quality levels → device checks go to manual tests.
