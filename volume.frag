#version 330              
 
in vec3 color;

out vec4 out_color;
 
void main() {
//	out_color = vec4(.1,.3,.8,.3);
	out_color = vec4(color,1);
}

