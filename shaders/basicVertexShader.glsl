#version 420 core

uniform mat4 u_viewTransform;
uniform mat4 u_projectionTransform;
uniform mat4 u_objectTransform;

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_normal;
layout(location = 2) in vec2 a_uv;

out vec3 v_position;
out vec3 v_normal;
out vec2 v_uv;

void main() {
    v_position = a_position;
    v_normal = a_normal;
    v_uv = a_uv;

    gl_Position = u_projectionTransform * u_viewTransform * u_objectTransform * vec4(a_position, 1.0);
}