#version 330                                 
 
layout(triangles_adjacency) in;
//layout(triangles) in;
layout(triangle_strip , max_vertices = 8 ) out;
 
uniform mat4 modelview;
uniform mat4 projection;

uniform vec3 lpos; // light position

in vec3 normals[];

//out vec3 color;

void main()
{
	vec3 dp = lpos - gl_in[0].gl_Position.xyz;

	vec3 nb = (normals[0] + normals[2] + normals[4])/3.0;
	vec3 n1 = (normals[0] + normals[1] + normals[2])/3.0;
	vec3 n2 = (normals[2] + normals[3] + normals[4])/3.0;
	vec3 n3 = (normals[4] + normals[5] + normals[0])/3.0;

	float d0 = dot(nb,dp);
	float d1 = dot(n1,dp);
	float d2 = dot(n2,dp);
	float d3 = dot(n3,dp);

	if( d0 > 0 ) {
		gl_Position = projection * modelview * gl_in[0].gl_Position;
		EmitVertex();
		gl_Position = projection * modelview * gl_in[2].gl_Position;
		EmitVertex();
		gl_Position = projection * modelview * gl_in[4].gl_Position;
		EmitVertex();
		EndPrimitive();
	} else {
		vec4 v;
		v = gl_in[0].gl_Position+(gl_in[0].gl_Position-vec4(lpos,1))*2;
		gl_Position = projection * modelview * v;
		EmitVertex();
		v = gl_in[2].gl_Position+(gl_in[2].gl_Position-vec4(lpos,1))*2;
		gl_Position = projection * modelview * v;
		EmitVertex();
		v = gl_in[4].gl_Position+(gl_in[4].gl_Position-vec4(lpos,1))*2;
		gl_Position = projection * modelview * v;
		EmitVertex();
		EndPrimitive();
	}
}

