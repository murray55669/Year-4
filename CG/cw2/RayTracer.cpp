#include "RayTracer.h"
using namespace std;

int windowX = 640;
int windowY = 480;

//light at (0, 15, 0)
glm::vec3 lightPos = glm::vec3(-20.0f, 20.0f, 20.0f);
float lightIntensity = 1.0f;
float ambientIntensity = 0.2f;

/*
** std::vector is a data format similar with list in most of  script language, which allows users to change its size after claiming.
* 
** The difference is that std::vector is based on array rather than list, so it is not so effective when you try to insert a new element, 
* but faster while calling for values randomly or add elements by order.
*/
std::vector<Object*> objects;

void cleanup() {
	for(unsigned int i = 0; i < objects.size(); ++i){
		if(objects[i]){
			delete objects[i];
		}
	}
}

/*
** TODO: Function for testing intersection against all the objects in the scene
**
** If an object is hit then the IntersectionInfo object should contain
** the information about the intersection. Returns true if any object is hit, 
** false otherwise
** 
*/
bool CheckIntersection(const Ray &ray, IntersectInfo &info) {
	//You need to add your own solution for this funtion, to replace the 'return true'.	
	//Runing the function Intersect() of each of the objects would be one of the options.
	//Each time when intersect happens, the payload of ray will need to be updated, but that's no business of this function.
	//To make it clear, keyword const prevents the function from changing parameter ray.
    for(unsigned int i = 0; i < objects.size(); ++i) {
        if(objects[i]) {
            return objects[i]->Intersect(ray, info);
        }
    }
    return false;
}

/*
** TODO: Recursive ray-casting function. It might be the most important Function in this demo cause it's the one decides the color of pixels.
**
** This function is called for each pixel, and each time a ray is reflected/used 
** for shadow testing. The Payload object can be used to record information about
** the ray trace such as the current color and the number of bounces performed.
** This function should return either the time of intersection with an object
** or minus one to indicate no intersection.
*/
//	The function CastRay() will have to deal with light(), shadow() and reflection(). The impement of them would also be important.
float CastRay(Ray &ray, Payload &payload) {

	IntersectInfo info;

	if (CheckIntersection(ray,info)) {
		/* TODO: Set payload color based on object materials, not direction */
                //payload.color = ray.direction;
                // In this case, it's just because we want to show something and we do not want to show the same color for every pixel.
                // Usually payload.color will be decided by the bounces.
                
                //TODO: lighting calculations
                //unit vector from point -> lightsource (lightsource - point)
                glm::vec3 lightVec = glm::normalize(glm::vec3(lightPos - info.hitPoint));
                //normal . lightvec = cos theta
                float cosTheta = max(0.0f, glm::dot(lightVec, info.normal));
                
                
                //float diffuseReflectivity = 0.5; //kd
                //float cosTheta = max(0.0, dot(lightVec, normOut)); //cos(theta)
                //float diff = lightIntensity * diffuseReflectivity * cosTheta; //Idiff
                
                glm::vec3 diff = glm::vec3((lightIntensity*info.material->diffuse[0]*cosTheta), (lightIntensity*info.material->diffuse[1]*cosTheta), (lightIntensity*info.material->diffuse[2]*cosTheta));
                
                glm::vec3 ambient = ambientIntensity * info.material->ambient;
                
                glm::vec3 specular = glm::vec3(0.0f);
                
		payload.color = ambient + diff + specular;
                
		return info.time;
	}
	else{
		payload.color = glm::vec3(0.0f);
		// The Ray from camera hits nothing so nothing will be seen. In this case, the pixel should be totally black.
		return -1.0f;	
	}	
}


// Render Function

// This is the main render function, it draws pixels onto the display
// using GL_POINTS. It is called every time an update is required.

// This function transforms each pixel into the space of the virtual
// scene and casts a ray from the camera in that direction using CastRay
// And for rendering,
// 1)Clear the screen so we can draw a new frame
// 2)Cast a ray into the scene for each pixel on the screen and use the returned color to render the pixel
// 3)Flush the pipeline so that the instructions we gave are performed.

void Render()
{
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);// Clear OpenGL Window

	//	Three parameters of lookat(vec3 eye, vec3 center, vec3 up).	
	glm::mat4 viewMatrix = glm::lookAt(glm::vec3(-10.0f,10.0f,10.0f), glm::vec3(0.0f,0.0f,0.0f), glm::vec3(0.0f,1.0f,0.0f));
	glm::mat4 projMatrix = glm::perspective(45.0f, (float)windowX / (float)windowY, 1.0f, 10000.0f);

	glBegin(GL_POINTS);	//Using GL_POINTS mode. In this mode, every vertex specified is a point.
	//	Reference https://en.wikibooks.org/wiki/OpenGL_Programming/GLStart/Tut3 if interested.
  
	for(int x = 0; x < windowX; ++x)
		for(int y = 0; y < windowY; ++y){//Cover the entire display zone pixel by pixel, but without showing.
			float pixelX =  2*((x+0.5f)/windowX)-1;	//Actually, (pixelX, pixelY) are the relative position of the point(x, y).
			float pixelY = -2*((y+0.5f)/windowY)+1;	//The displayzone will be decribed as a 2.0f x 2.0f platform and coordinate origin is the center of the display zone.

			//	Decide the direction of each of the ray.
			glm::vec4 worldNear = glm::inverse(viewMatrix) * glm::inverse(projMatrix) * glm::vec4(pixelX, pixelY, -1, 1);
			glm::vec4 worldFar  = glm::inverse(viewMatrix) * glm::inverse(projMatrix) * glm::vec4(pixelX, pixelY,  1, 1);
			glm::vec3 worldNearPos = glm::vec3(worldNear.x, worldNear.y, worldNear.z) / worldNear.w;
			glm::vec3 worldFarPos  = glm::vec3(worldFar.x, worldFar.y, worldFar.z) / worldFar.w;

			Payload payload;
			Ray ray(worldNearPos, glm::normalize(glm::vec3(worldFarPos - worldNearPos))); //Ray(const glm::vec3 &origin, const glm::vec3 &direction)

			if(CastRay(ray,payload) > 0.0f){
				glColor3f(payload.color.x,payload.color.y,payload.color.z);
			} 
			else {
				glColor3f(0.4,0.4,0.4);
			}

			glVertex3f(pixelX,pixelY,0.0f);
		}
  
	glEnd();
	glFlush();
}

int main(int argc, char **argv) {

  	//initialise OpenGL
	glutInit(&argc, argv);
	//Define the window size with the size specifed at the top of this file
	glutInitWindowSize(windowX, windowY);

	//Create the window for drawing
	glutCreateWindow("RayTracer");
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH);	

	//Set the function demoDisplay (defined above) as the function that
	//is called when the window must display.
	glutDisplayFunc(Render);
  
	//	TODO: Add Objects to scene
	//	This part is related to function CheckIntersection().
	//	Being added into scene means that the object will take part in the intersection checking, so try to make these two connected to each other.
        
        Material mat1;
        mat1.diffuse = glm::vec3(0.6f, 0.0f, 0.0f);
        mat1.specular = glm::vec3(0.5f);
        mat1.glossiness = 13.0f;
        
        //Plane* plane = new Plane();
        Sphere* sphere = new Sphere();
        sphere->SetMaterial(mat1);
        //Triangle* triangle = new Triangle()
        
        //objects.push_back(plane);
        objects.push_back(sphere);
        //objects.push_back(triangle);
        

	atexit(cleanup);
	glutMainLoop();
}
