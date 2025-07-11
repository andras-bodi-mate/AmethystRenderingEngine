#version 420 core
layout (location = 0) in vec3 a_position;

out vec3 v_position;

void main()
{
    v_position = a_position;

    gl_Position = vec4(v_position.xy, 0.0, 1.0);
}