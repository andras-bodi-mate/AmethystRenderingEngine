#version 330 core

uniform mat4 viewTransform;
uniform mat4 perspectiveTransform;

layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;
layout(location = 2) in vec2 in_uv;

out vec3 v_normal;
out vec2 v_uv;

void main() {
    v_normal = in_normal;
    v_uv = in_uv;

    gl_Position = perspectiveTransform * viewTransform * vec4(in_position, 1.0);
}