#version 420 core

in vec3 v_position;
  
layout (binding = 0) uniform samplerCube u_environmentTexture;

layout (location = 0) out vec4 fragColor;
  
void main()
{
    vec3 envColor = textureLod(u_environmentTexture, v_position, 4.0).rgb;
    
    envColor = envColor / (envColor + vec3(1.0));
    envColor = pow(envColor, vec3(1.0/2.2)); 
  
    fragColor = vec4(envColor, 1.0);
}