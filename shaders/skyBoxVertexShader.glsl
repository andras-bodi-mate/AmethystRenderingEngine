#version 420 core
layout (location = 0) in vec3 a_position;

uniform mat4 u_projectionTransform;
uniform mat4 u_viewTransform;

out vec3 v_position;

void main()
{
    v_position = a_position;

    mat4 viewRotation = mat4(mat3(u_viewTransform)); // remove translation from the view matrix
    vec4 clipPos = u_projectionTransform * viewRotation * vec4(a_position, 1.0);

    gl_Position = clipPos.xyww;
}