#version 420 core

in vec3 v_normal;
in vec2 v_uv;

layout (binding = 0) uniform sampler2D u_baseColorTexture;
layout (binding = 1) uniform sampler2D u_normalTexture;
layout (binding = 2) uniform sampler2D u_metallicRoughnessTexture;

layout (location = 0) out vec4 fragColor;

void main() {
    vec3 lightDir = vec3(0.270229, 0.94311, -0.1937);

    fragColor = (vec4(v_uv.x, v_uv.y, 0.0, 0.0) + vec4(v_normal, 0.0));
    fragColor = (vec4(texture(u_normalTexture, v_uv)) * mix(0.3, 1.0, dot(lightDir, v_normal)));
}