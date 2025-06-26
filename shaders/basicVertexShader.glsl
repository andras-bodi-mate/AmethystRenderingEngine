#version 330 core

uniform mat4 viewTransform;
uniform mat4 perspectiveTransform;

in vec3 in_position;
in vec3 in_normal;

out vec3 frag_normal;

void main() {
    frag_normal = in_normal;

    gl_Position = perspectiveTransform * viewTransform * vec4(in_position, 1.0);
}