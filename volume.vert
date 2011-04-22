#version 130
//#version 330                          

out vec3 normals;
 
void main()
{
    gl_Position = gl_Vertex;
    normals     = gl_Normal;
}

