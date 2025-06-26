#version 330 core

uniform mat4 viewTransform;
uniform mat4 perspectiveTransform;

in vec3 in_position;
//in vec2 in_uv;
in vec3 in_normal;

//out vec2 vert_uv;
//out vec3 vert_normal;

void main() {
    //vert_uv = in_uv;
    vec3 vert_normal = in_normal;

    gl_Position = perspectiveTransform * viewTransform * vec4(in_position, 1.0);
}