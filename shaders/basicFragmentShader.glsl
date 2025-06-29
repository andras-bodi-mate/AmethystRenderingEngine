#version 330 core

layout (location = 0) out vec4 out_color;

in vec3 v_normal;
in vec2 v_uv;

//uniform sampler2D baseColorTexture;

void main() {
    vec3 lightDir = vec3(-0.270229, 0.94311, 0.1937);

    //out_color = vec4(1.0, 1.0, 1.0, 1.0) * mix(0.1, 1.0, clamp(dot(v_normal, lightDir), 0.0, 1.0));
    out_color = vec4(v_uv, 0.0, 1.0) + 0.00001 * (vec4(v_uv.x, v_uv.y, 0.0, 0.0) + vec4(v_normal, 0.0));
}