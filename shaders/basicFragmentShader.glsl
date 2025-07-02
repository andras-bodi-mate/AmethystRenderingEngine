#version 330 core

in vec3 v_normal;
in vec2 v_uv;

uniform sampler2D baseColorTexture;

layout (location = 0) out vec4 out_color;

void main() {
    vec3 lightDir = vec3(-0.270229, 0.94311, 0.1937);

    out_color = (vec4(v_uv.x, v_uv.y, 0.0, 0.0) + vec4(v_normal, 0.0));
    out_color = (vec4(texture(baseColorTexture, v_uv)) * mix(0.3, 1.0, dot(lightDir, v_normal)));
}