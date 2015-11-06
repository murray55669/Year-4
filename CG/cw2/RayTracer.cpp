#include "RayTracer.h"
using namespace std;

int windowX = 640;
int windowY = 480;

glm::vec3 lightPos = glm::vec3(-6, 4, 2);
glm::vec3 lightIntensity = glm::vec3(1.0f);
int bounceLimit = 10;
float epsilon = 0.01f;
glm::vec3 eyePos = glm::vec3(-10, 10, 10);

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
    
    bool objectHit = false;
    
    for(unsigned int i = 0; i < objects.size(); i++) {
        //ensure objects appear in the correct order - set info intersection with the minimum time (light has constant speed, so time essentially = distance)
        IntersectInfo tempInfo;
        
        if (objects[i]->Intersect(ray, tempInfo)) {
            objectHit = true;
            
            if (tempInfo.time < info.time) {
                info.time = tempInfo.time;
                info.hitPoint = tempInfo.hitPoint;
                info.normal = tempInfo.normal;
                info.material = tempInfo.material;
            }
        }

    }
    return objectHit;
}

bool CheckShadow(const Ray &shadowRay) {
    bool inShadow = false;
    
    IntersectInfo shadowInfo;
    
    for(unsigned int i = 0; i < objects.size(); i++) {
        
        if (objects[i]->Intersect(shadowRay, shadowInfo)) {
            //prevent objects behind the light from casting shadows
            if (shadowInfo.time < glm::length(lightPos - shadowRay.origin)) {
                inShadow = true;
                break;
            }
        }
        
    }
    
    return inShadow;
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
                // In this case, it's just because we want to show something and we do not want to show the same color for every pixel.
                // Usually payload.color will be decided by the bounces.
                
                payload.numBounces += 1;
                
                //At every intersection, send a shadow ray from the intersection to the light source, to check if the light is blocked
                //create a ray from hitpoint -> lightsource; if it intersects with an object the hitpoint is in shadow
                glm::vec3 shadowDir = glm::normalize(lightPos - info.hitPoint);
                Ray shadowRay(info.hitPoint, shadowDir);
                //ensure object doesn't self-shadow due to floating point innaccuracies
                glm::vec3 floatOffsetShadow = shadowRay(epsilon);
                shadowRay = Ray(floatOffsetShadow, shadowDir);
                bool inShadow = false;
                inShadow = CheckShadow(shadowRay);
                
                //Reflection
                //reflected vector = d - 2(d.n)*n
                glm::vec3 reflectDir = glm::normalize(ray.direction - 2.0f*(glm::dot(ray.direction, info.normal))*info.normal);
                Ray reflectRay(info.hitPoint, reflectDir);
                glm::vec3 floatOffsetReflection = reflectRay(epsilon);
                reflectRay = Ray(floatOffsetReflection, reflectDir);
                if (payload.numBounces < bounceLimit) {
                    CastRay(reflectRay, payload);
                }
                
                
                
                glm::vec3 initColour;
                if (not(inShadow)) {
                    //Phong illumination
                    //Ambient
                    glm::vec3 ambient = info.material->ambient;
                    
                    //Diffuse
                    glm::vec3 lightVec = glm::normalize(glm::vec3(lightPos - info.hitPoint));
                    float cosTheta = max(0.0f, glm::dot(lightVec, info.normal));
                    glm::vec3 diff = glm::vec3((lightIntensity[0]*info.material->diffuse[0]*cosTheta), 
                                            (lightIntensity[1]*info.material->diffuse[1]*cosTheta), 
                                            (lightIntensity[2]*info.material->diffuse[2]*cosTheta));

                    //Specular                
                    glm::vec3 eyeVec = glm::normalize(glm::vec3(eyePos - info.hitPoint));
                    float cosAlpha = max(0.0f, glm::dot((2.0f * info.normal * (glm::dot(lightVec, info.normal)) - lightVec), eyeVec));
                    glm::vec3 specular = glm::vec3((lightIntensity[0]*info.material->specular[0]*pow(cosAlpha, info.material->glossiness)), 
                                                (lightIntensity[1]*info.material->specular[1]*pow(cosAlpha, info.material->glossiness)), 
                                                (lightIntensity[2]*info.material->specular[2]*pow(cosAlpha, info.material->glossiness))
                                                );
                    
                    initColour = ambient + diff + specular;                
                } else {
                    initColour = info.material->ambient;
                }      
                   
                //Refraction
                if (info.material->refraction > 0) {
                    float r;
                    //leaving an object (sphere)
                    if (payload.lastObjectHit == info.objectHit) {
                        r = payload.refractiveIndex; //should be payload.index/air.index, but air.index is 1
                        
                        payload.lastObjectHit = NULL;
                        payload.refractiveIndex = 1;
                    } 
                    //entering an object
                    else {
                        r = payload.refractiveIndex / info.material->refractiveIndex;
                        
                        payload.lastObjectHit = info.objectHit;
                        payload.refractiveIndex = info.material->refractiveIndex;
                    }
                    
                    //check for total internal reflection
                    //"Total internal reflection is indicated by a negative radicand" ** radicand = 1-r^2(1-c^2); c = -n.l; l = (normalized) incident ray
                    glm::vec3 l = glm::normalize(ray.direction);
                    float c = -1.0f * glm::dot(info.normal, l);
                    float radicand = 1.0f - (pow(r, 2) * (1.0f - pow(c, 2)));
                    float refractionFactor;
                    
                    if (radicand >= 0.0f) {
                        glm::vec3 refractionDir = (r*l) + (((r*c) - sqrt(radicand))*info.normal);

                        Ray refractionRay = Ray(info.hitPoint, refractionDir);
                        Ray refractionRayOffset = Ray(refractionRay(epsilon), refractionDir);

                        payload.refractiveIndex = info.material->refractiveIndex;
                        refractionFactor = info.material->refraction;

                        CastRay(refractionRayOffset, payload);

                    } else {
                        refractionFactor = 0;
                    }
                    payload.color = info.material->reflection * payload.color + (1-info.material->reflection) * initColour + refractionFactor * payload.color;
                     
                } else {
                    payload.color = info.material->reflection * payload.color + (1-info.material->reflection) * initColour;
                }
                
                
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
				glColor3f(0.0f, 0.0f, 0.0f);
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
        
        Material yellow;
        yellow.diffuse = glm::vec3(0.8f, 0.8f, 0.0f);
        yellow.specular = glm::vec3(0.6f);
        yellow.ambient = glm::vec3(0.2f);
        yellow.glossiness = 10.0f;
        yellow.reflection = 0.5f;
        
        Material red;
        red.diffuse = glm::vec3(0.8f, 0.0f, 0.0f);
        red.specular = glm::vec3(0.6f);
        red.ambient = glm::vec3(0.2f);
        red.glossiness = 10.0f;
        red.reflection = 0.0f;
        red.refraction = 1.0f;
        red.refractiveIndex = 1.5f;
        
        Material blue;
        blue.diffuse = glm::vec3(0.57f, 0.76f, 0.83f);
        blue.specular = glm::vec3(0.6f);
        blue.ambient = glm::vec3(0.2f);
        blue.glossiness = 10.0f;
        blue.reflection = 0.2f;
        
        Plane* plane = new Plane();
        plane->SetMaterial(yellow);
        plane->SetPosition(glm::vec3(0.0f, 0.0f, 0.0f));
        plane->normal = (glm::vec3(0.0f, 1.0f, 0.0f));
        
        Plane* plane2 = new Plane();
        plane2->SetMaterial(blue);
        plane2->SetPosition(glm::vec3(0.0f, 0.0f, 0.0f));
        plane2->normal = (glm::vec3(-1.0f, 0.0f, 0.0f));
        
        Plane* plane3 = new Plane();
        plane3->SetMaterial(blue);
        plane3->SetPosition(glm::vec3(0.0f, 0.0f, 0.0f));
        plane3->normal = (glm::vec3(0.0f, 0.0f, 1.0f));
        
        Sphere* sphere = new Sphere();
        sphere->SetMaterial(yellow);
        sphere->SetPosition(glm::vec3(-3.0f,0.5f,1.0f));
        sphere->radius = 1.0f;
        
        Sphere* sphere2 = new Sphere();
        sphere2->SetMaterial(red);
        sphere2->SetPosition(glm::vec3(-5.0f,3.0f,3.0f));
        sphere2->radius = 0.8f;
        
        Triangle* triangle = new Triangle();
        triangle->SetMaterial(yellow);
        triangle->SetPoints(glm::vec3(-1, 3, 4), glm::vec3(-1, 0, 4), glm::vec3(-1, 0, 0));
        
        objects.push_back(plane);        
        objects.push_back(plane2);
        objects.push_back(plane3);
        objects.push_back(sphere);
        objects.push_back(sphere2);
        objects.push_back(triangle);
        

	atexit(cleanup);
	glutMainLoop();
}
