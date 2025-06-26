#version 330 core

layout (location = 0) out vec4 out_color;

in vec3 frag_normal;

void main() {
    vec3 lightDir = vec3(-1, 0, 0);

    out_color = vec4(frag_normal, 1.0) * mix(0.1, 1.0, clamp(dot(frag_normal, lightDir), 0.0, 1.0));
}