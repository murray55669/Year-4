#version 130

//Vector to light source
in vec4 lightVec;
//Vector to eye
in vec4 eyeVec;
//Transformed normal vector
in vec4 normOut;

//A texture you might want to use (optional)
uniform sampler2D tex;

//Output colour
out vec4 outColour;

/* Standard operations work on vectors, e.g.
	light + eye
	light - eye
   Single components can be accessed (light.x, light.y, light.z, light.w)
   C style program flow, e.g. for loops, if statements
   Can define new variables, vec2, vec3, vec4, float
   No recursion
   Example function calls you might find useful:
	max(x,y) - maximum of x and y
	dot(u,v) - dot product of u and v
	normalize(x) - normalise a vector
	pow(a,b) - raise a to power b
	texture(t,p) - read texture t at coordinates p (vec2 between 0 and 1)
	mix(a,b,c) - linear interpolation between a and b, by c. (You do not need to use this to interpolate vertex attributes, OpenGL will take care of interpolation between vertices before calling the fragment shader)
   outColour is a vec4 containing the RGBA colour as floating point values between 0 and 1. outColour.r, outColour.g, outColour.b and outColour.a can be used to access the components of a vec4 (as well as .x .y .z .w)
*/

void main() {	
	//Modify this code to calculate Phong illumination based on the inputs
	//General
	float lightIntensity = 0.6; //Ip
	
	//Diffuse
	float diffuseReflectivity = 0.8; //kd
	float cosTheta = max(0.0, dot(lightVec, normOut)); //cos(theta)
	float diff = lightIntensity * diffuseReflectivity * cosTheta; //Idiff
	//diff = 0.0;
	
	//Specular
	float specularReflectivity = 0.8; //ks
	float specularIntensity = 50; //n - range from e.g. 1 to 100
 	float cosAlpha = max(0.0, dot((2 * normOut * (dot(lightVec, normOut)) - lightVec), eyeVec)); //cos(alpha)
	float spec = lightIntensity * specularReflectivity * pow(cosAlpha, specularIntensity); //Ispec
	//spec = 0.0;
	
	float ambient = 0.0;
	outColour = vec4(spec+ambient, spec+diff+ambient, spec+ambient, 1.0);
}