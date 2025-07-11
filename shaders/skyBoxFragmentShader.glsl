#version 420 core

in vec3 v_position;
  
layout (binding = 0) uniform samplerCube u_environmentTexture;

layout (location = 0) out vec4 fragColor;

const float exposure = 0.8;

void main()
{
    vec3 envColor = texture(u_environmentTexture, v_position).rgb;
    
    envColor = vec3(1.0) - exp(-envColor * exposure);
    envColor = pow(envColor, vec3(1.0 / 2.2));

    fragColor = vec4(envColor, 1.0);
}