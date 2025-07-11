#version 420 core

in vec3 v_position;
in vec3 v_normal;
in vec2 v_uv;
in mat3 v_tangentBitangentNormal;

uniform vec3 u_cameraPosition;

layout (binding = 0) uniform sampler2D u_baseColorTexture;
layout (binding = 1) uniform sampler2D u_normalTexture;
layout (binding = 2) uniform sampler2D u_metallicRoughnessTexture;
layout (binding = 3) uniform sampler2D u_ambientOcclusionTexture;
layout (binding = 4) uniform sampler2D u_emissiveTexture;
layout (binding = 5) uniform samplerCube u_diffuseIrradianceMap;
layout (binding = 6) uniform samplerCube u_specularPrefilterMap;
layout (binding = 7) uniform sampler2D u_brdfLookupTable;

layout (location = 0) out vec4 fragColor;

const float PI = 3.14159265359;

vec3 fresnelSchlick(float cosTheta, vec3 F0) {
    return F0 + (1.0 - F0) * pow(clamp(1.0 - cosTheta, 0.0, 1.0), 5.0);
}

vec3 fresnelSchlickRoughness(float cosTheta, vec3 F0, float roughness) {
    return F0 + (max(vec3(1.0 - roughness), F0) - F0) * pow(clamp(1.0 - cosTheta, 0.0, 1.0), 5.0);
} 

float distributionGGX(vec3 N, vec3 H, float roughness) {
    float a = roughness*roughness;
    float a2 = a*a;
    float NdotH = max(dot(N, H), 0.0);
    float NdotH2 = NdotH*NdotH;
	
    float num = a2;
    float denom = (NdotH2 * (a2 - 1.0) + 1.0);
    denom = PI * denom * denom;
	
    return num / denom;
}

float geometrySchlickGGX(float NdotV, float roughness) {
    float r = (roughness + 1.0);
    float k = (r*r) / 8.0;

    float num = NdotV;
    float denom = NdotV * (1.0 - k) + k;
	
    return num / denom;
}

float geometrySmith(vec3 N, vec3 V, vec3 L, float roughness) {
    float NdotV = max(dot(N, V), 0.0);
    float NdotL = max(dot(N, L), 0.0);
    float ggx2 = geometrySchlickGGX(NdotV, roughness);
    float ggx1 = geometrySchlickGGX(NdotL, roughness);
	
    return ggx1 * ggx2;
}

vec3[5] lightPositions = vec3[](
    vec3(1, 2, 0.5),
    vec3(-4, 0.5, 1.5),
    vec3(4, -0.5, -1.5),
    vec3(4, 1.0, 1.0),
    vec3(6, -1.0, 0.0)
);

const vec3 lightColor = vec3(1.0, 1.0, 1.0);
const float numPrefilterLods = 5.0;

void main() {
    vec3 tangentNormal = texture(u_normalTexture, v_uv).xyz;
    tangentNormal = tangentNormal * 2.0 - 1.0; // Convert from [0,1] to [-1,1]

    vec3 N = normalize(v_tangentBitangentNormal * tangentNormal);
    vec3 V = normalize(u_cameraPosition - v_position);
    vec3 R = reflect(-V, N);

    vec3 baseColor = texture(u_baseColorTexture, v_uv).xyz;
    vec3 metallicRoughness = texture(u_metallicRoughnessTexture, v_uv).xyz;
    float roughness = metallicRoughness.y;
    float metallic = metallicRoughness.z;
    float ambientOcclusion = texture(u_ambientOcclusionTexture, v_uv).r;
    vec3 emissiveColor = texture(u_emissiveTexture, v_uv).rgb;

    vec3 F0 = vec3(0.04);
    F0 = mix(F0, baseColor, clamp(metallic, 0.0, 1.0));

    //F0 = mix(F0, baseColor, metallic);

    vec3 F = fresnelSchlickRoughness(max(dot(N, V), 0.0), F0, roughness);

    vec3 kS = F;
    vec3 kD = 1.0 - kS;
    kD *= 1.0 - metallic;

    vec3 irradiance = texture(u_diffuseIrradianceMap, N).rgb;
    vec3 diffuse = irradiance * baseColor;

    vec3 prefilteredColor = textureLod(u_specularPrefilterMap, R,  roughness * (numPrefilterLods - 1)).rgb;
    vec2 envBRDF = texture(u_brdfLookupTable, vec2(max(dot(N, V), 0.0), roughness)).rg;
    vec3 specular = prefilteredColor * (F * envBRDF.x + envBRDF.y);
    
    vec3 ambient = (kD * diffuse + specular) * ambientOcclusion;
    vec3 color = ambient;

    float emissiveIntensity = 1.0; // You define this — can be per-material or uniform
    vec3 emissive = emissiveColor * emissiveIntensity;
	
    color = color / (color + vec3(1.0));
    color = pow(color, vec3(1.0/2.2));

    color += emissive;
   
    fragColor = vec4(color, 1.0);
    //fragColor = mix(vec4(ambientOcclusion, 0.0, 0.0, 1.0), vec4(color, 1.0), 0.00001);
}