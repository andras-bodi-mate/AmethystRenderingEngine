#version 420 core

in vec3 v_position;

layout (binding = 0) uniform sampler2D u_equirectangularTexture;
uniform vec3 u_cameraPosition;

layout (location = 0) out vec4 fragColor;


const vec2 invAtan = vec2(0.1591, 0.3183);

vec2 SampleSphericalMap(vec3 v)
{
    vec2 uv = vec2(atan(v.z, v.x), asin(v.y));
    uv *= invAtan;
    uv += 0.5;
    return uv;
}

void main()
{	
    vec2 uv = SampleSphericalMap(normalize(v_position)) * vec2(1.0, 0.5); // make sure to normalize localPos
    vec3 color = texture(u_equirectangularTexture, uv).rgb;
    
    fragColor = vec4(u_cameraPosition, 1.0);
    fragColor = vec4(color, 1.0);
}