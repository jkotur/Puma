#version 330                                 
 
layout(triangles_adjacency) in;
//layout(triangles) in;
layout(triangle_strip , max_vertices = 32 ) out;
 
uniform mat4 modelview;
uniform mat4 projection;

uniform vec3 lpos; // light position

in vec3 normals[];

out vec3 color;

vec4 move( vec4 vec , vec3 lpos )
{
	return vec+(vec-vec4(lpos,1))*3;
}

void main()
{
	vec4 p0 = modelview * gl_in[0].gl_Position;
	vec4 p1 = modelview * gl_in[2].gl_Position;
	vec4 p2 = modelview * gl_in[4].gl_Position;

	vec3 dp1 = lpos - p0.xyz;
	vec3 dp2 = lpos - p1.xyz;
	vec3 dp3 = lpos - p2.xyz;

	vec3 nb = (modelview * vec4((normals[0] + normals[2] + normals[4])/3.0,0)).xyz;
	vec3 n1 = (modelview * vec4( normals[1] , 0 )).xyz;
	vec3 n2 = (modelview * vec4( normals[3] , 0 )).xyz;
	vec3 n3 = (modelview * vec4( normals[5] , 0 )).xyz;

	float d0 = dot(nb,dp1);
	float d1 = dot(n1,dp1);
	float d2 = dot(n2,dp2);
	float d3 = dot(n3,dp3);

	mat4 PMV = projection * modelview;

	if( d0 > 0 ) {
		color = nb;
		gl_Position = projection * p0 ; EmitVertex();
		gl_Position = projection * p1 ; EmitVertex();
		gl_Position = projection * p2 ; EmitVertex();
		EndPrimitive();
	} else {
		color = nb;
		gl_Position = projection * move( p0 , lpos ); EmitVertex();
		gl_Position = projection * move( p1 , lpos ); EmitVertex();
		gl_Position = projection * move( p2 , lpos ); EmitVertex();
		EndPrimitive();

		if( d1 > 0 ) {
			color = n1;
//			color = vec3(1,0,0);
			gl_Position = projection *       p0         ; EmitVertex();
			gl_Position = projection *       p1         ; EmitVertex();
			gl_Position = projection * move( p0 , lpos ); EmitVertex();
			gl_Position = projection * move( p1 , lpos ); EmitVertex();
			EndPrimitive();
		}

		if( d2 > 0 ) {
			color = n2;
//			color = vec3(0,1,0);
			gl_Position = projection *       p1         ; EmitVertex();
			gl_Position = projection *       p2         ; EmitVertex();
			gl_Position = projection * move( p1 , lpos ); EmitVertex();
			gl_Position = projection * move( p2 , lpos ); EmitVertex();
			EndPrimitive();
		}

		if( d3 > 0 ) {
			color = n3;
//			color = vec3(0,0,1);
			gl_Position = projection *       p2         ; EmitVertex();
			gl_Position = projection *       p0         ; EmitVertex();
			gl_Position = projection * move( p2 , lpos ); EmitVertex();
			gl_Position = projection * move( p0 , lpos ); EmitVertex();
			EndPrimitive();
		}
	}
}

