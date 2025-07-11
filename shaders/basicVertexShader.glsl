#version 420 core

uniform mat4 u_viewTransform;
uniform mat4 u_projectionTransform;
uniform mat4 u_objectTransform;

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_normal;
layout(location = 2) in vec2 a_uv;
layout(location = 3) in vec3 a_tangent;

out vec3 v_position;
out vec3 v_normal;
out vec2 v_uv;
out mat3 v_tangentBitangentNormal;

void main() {
    v_position = (mat3(u_objectTransform) * a_position).xyz; 
    v_normal = a_normal;
    v_uv = a_uv;

    vec3 tangent = normalize(mat3(u_objectTransform) * a_tangent);
    vec3 normal = normalize(mat3(u_objectTransform) * a_normal);
    vec3 bitangent = normalize(cross(normalize(a_normal + vec3(0.0001, 0.0, 0.0)), tangent));

    v_tangentBitangentNormal = mat3(tangent, bitangent, normal);

    gl_Position = u_projectionTransform * u_viewTransform * u_objectTransform * vec4(a_position, 1.0);
}