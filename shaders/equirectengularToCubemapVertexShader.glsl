#version 420 core

layout (location = 0) in vec3 a_position;

uniform mat4 u_viewTransform;
uniform mat4 u_projectionTransform;

out vec3 v_position;

void main()
{
    v_position = a_position;  
    gl_Position =  u_projectionTransform * u_viewTransform * vec4(a_position, 1.0);
}