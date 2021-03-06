#version 330                                 
 
layout(triangles_adjacency) in;
//layout(triangles) in;
layout(triangle_strip , max_vertices = 32 ) out;
 
uniform mat4 modelview;
uniform mat4 projection;

uniform vec3 lpos; // light position

uniform float culling;

in vec3 normals[];

out vec3 color;

vec4 move( vec4 vec , vec3 lpos )
{
	return vec+(vec-vec4(lpos,1))*4;
}

void main()
{
	vec4 p0 = modelview * gl_in[0].gl_Position;
	vec4 p1 = modelview * gl_in[2].gl_Position;
	vec4 p2 = modelview * gl_in[4].gl_Position;

	vec3 dp0 = lpos - ((p0+p1+p2)/3.0).xyz;
	vec3 dp1 = lpos - (modelview * gl_in[1].gl_Position).xyz;
	vec3 dp2 = lpos - (modelview * gl_in[3].gl_Position).xyz;
	vec3 dp3 = lpos - (modelview * gl_in[5].gl_Position).xyz;

	vec3 nb = (modelview * vec4((normals[0] + normals[2] + normals[4])/3.0,0)).xyz;
	vec3 n1 = (modelview * vec4( normals[1] , 0 )).xyz;
	vec3 n2 = (modelview * vec4( normals[3] , 0 )).xyz;
	vec3 n3 = (modelview * vec4( normals[5] , 0 )).xyz;

	float d0 = dot(nb,dp0);
	float d1 = dot(n1,dp1);
	float d2 = dot(n2,dp2);
	float d3 = dot(n3,dp3);

//	if( culling < 0 )
//		color = vec3(1,0,0);
//	else	color = vec3(0,1,0);

	if( d0 > 0 ) {
		if( dot(nb,p0.xyz) * culling <= 0.0 ) {
			color = nb;
			// prevent self shadownig
			gl_Position = projection * p0 + vec4(0,0,.01,0) ; EmitVertex();
			gl_Position = projection * p1 + vec4(0,0,.01,0) ; EmitVertex();
			gl_Position = projection * p2 + vec4(0,0,.01,0) ; EmitVertex();
			EndPrimitive();
		}
	} else {
		vec4 mp0 = move( p0 , lpos );
		if( dot(nb,mp0.xyz) * culling <= 0 ) {
			color = nb;
			gl_Position = projection *      mp0         ; EmitVertex();
			gl_Position = projection * move( p1 , lpos ); EmitVertex();
			gl_Position = projection * move( p2 , lpos ); EmitVertex();
			EndPrimitive();
		}

		vec3 n = vec3(0);

		if( d1 > 0 ) {
			n = normalize( cross( lpos - p0.xyz , p1.xyz-p0.xyz ) );
			if( dot(n ,nb) < 0 ) n = -n;
		//	if( dot(n1,nb) > 0 ) n = -n;

			if( dot(n,p1.xyz) * culling <= 0 ) {
				color = n;
				gl_Position = projection *       p0         ; EmitVertex();
				gl_Position = projection *       p1         ; EmitVertex();
				gl_Position = projection * move( p0 , lpos ); EmitVertex();
				gl_Position = projection * move( p1 , lpos ); EmitVertex();
				EndPrimitive();
			}
		}

		if( d2 > 0 ) {
			n = normalize( cross( lpos - p1.xyz , p2.xyz-p1.xyz ) );
			if( dot(n ,nb) < 0 ) n = -n;
		//	if( dot(n2,nb) > 0 ) n = -n;

			if( dot(n,p2.xyz) * culling <= 0 ) {
				color = n;
				gl_Position = projection *       p1         ; EmitVertex();
				gl_Position = projection *       p2         ; EmitVertex();
				gl_Position = projection * move( p1 , lpos ); EmitVertex();
				gl_Position = projection * move( p2 , lpos ); EmitVertex();
				EndPrimitive();
			}
		}

		if( d3 > 0 ) {
			n = normalize( cross( lpos - p2.xyz , p0.xyz-p2.xyz ) );
			if( dot(n ,nb) < 0 ) n = -n;
		//	if( dot(n3,nb) > 0 ) n = -n;

			if( dot(n,p0.xyz) * culling <= 0 ) {
				color = n;
				gl_Position = projection *       p2         ; EmitVertex();
				gl_Position = projection *       p0         ; EmitVertex();
				gl_Position = projection * move( p2 , lpos ); EmitVertex();
				gl_Position = projection * move( p0 , lpos ); EmitVertex();
				EndPrimitive();
			}
		}
	}
}

