#include "Object.h"

//debug
#include <iostream>
using namespace std;
//cout << "whatever";

Material::Material():
    ambient(1.0f),
    diffuse(1.0f),
    specular(1.0f),
    glossiness(10.0f)
  {}

Object::Object(const glm::mat4 &transform, const Material &material):
    transform(transform),
    material(material)
  {}

/* TODO: Implement */
bool Sphere::Intersect(const Ray &ray, IntersectInfo &info) const { 
    glm::vec3 d = ray.origin;
    glm::vec3 e = ray.direction;
    glm::vec3 s = Position();
    float r = Radius();
    
    glm::vec3 e_min_s = e-s;
    float d_dot_d = glm::dot(d, d);
    
    float discriminant = pow( (glm::dot((2.0f*d), (e_min_s))) , 2.0f) - 4.0f*(d_dot_d)*(glm::dot((e_min_s), (e_min_s))-pow(r, 2.0f));

    float front = -2.0f*glm::dot(d, (e_min_s));
    float discriminant_sqrt = sqrt(discriminant);
    
    /* The time along the ray that the intersection occurs */
    float t1 = (front + discriminant_sqrt) / (2.0f*d_dot_d);
    float t2 = (front - discriminant_sqrt) / (2.0f*d_dot_d);
    
    bool intersected = false;
    
    if (t1 >= 0.0f) {
        if (t1 < t2) {
            info.time = t1;
            intersected = true;
        }
        else if (t2 >= 0.0f) {
            info.time = t2;
            intersected = true;
        } else {
            info.time = t1;
            intersected = true;
        }
    }
    
    /*
        printf("d: [%f, %f, %f]\n",d[0], d[1], d[2]);
        printf("e: [%f, %f, %f]\n",e[0], e[1], e[2]);
        printf("s: [%f, %f, %f]\n",s[0], s[1], s[2]);
        printf("r: %f\n", r);
        printf("Discriminant: %f \n", discriminant);
        
        printf("sqrt dis: %f\n", discriminant_sqrt);
        printf("front: %f\n", front);
        printf("d dot d: %f\n", d_dot_d);
        printf("time: %f\n", info.time);
        printf("t1: %f\n", t1);
        printf("t2: %f\n", t2);
    */
    
    if (intersected) {
        /* The material of the object that was intersected */
        info.material = MaterialPtr();
        /* The position of the intersection in 3D coordinates */
        info.hitPoint = ray(info.time);
        
        /* The normal vector of the surface at the point of the intersection */
        //N = ((x - cx)/R, (y - cy)/R, (z - cz)/R)
        float n_x = (info.hitPoint[0] - s[0])/r;
        float n_y = (info.hitPoint[1] - s[1])/r;
        float n_z = (info.hitPoint[2] - s[2])/r;
        info.normal = glm::normalize(glm::vec3(n_x, n_y, n_z));
        
        return true;
    }
    return false;

}
// Function glm::dot(x,y) will return the dot product of parameters. (It's the inner product of vectors)

/* TODO: Implement */
bool Plane::Intersect(const Ray &ray, IntersectInfo &info) const { return -1.0f; }

/* TODO: Implement */
bool Triangle::Intersect(const Ray &ray, IntersectInfo &info) const { return -1.0f; }
