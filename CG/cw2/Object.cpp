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
    //Ray has origin + direction
    //Assuming the sphere is radius 0.2, centred at Position()
    //b^2 - 4*a*c
    glm::vec3 d = ray.origin;
    glm::vec3 e = ray.direction;
    glm::vec3 s = Position();
    float r = 0.2f;
    
    glm::vec3 e_min_s = e-s;
    float d_dot_d = glm::dot(d, d);
    
    float discriminant = pow( (glm::dot((2.0f*d), (e_min_s))) , 2.0f) - 4.0f*(d_dot_d)*(glm::dot((e_min_s), (e_min_s))-pow(r, 2.0f));

    /* The time along the ray that the intersection occurs */
    float front = glm::dot((-2.0f*d), (e_min_s));
    float discriminant_sqrt = sqrt(discriminant);
    
    float t1 = (front + discriminant_sqrt) / 2.0f*d_dot_d;
    
    if (t1 >= 0.0f) {
        if (discriminant != 0.0f) {
            float t2 = (front - discriminant_sqrt) / 2.0f*d_dot_d;
            //Take the smallest t value; discard results less than zero
            if (t1 < t2) {
                info.time = t1;
            } else if (t2 >= 0.0f) {
                info.time = t2;
            }
        } else {
            info.time = t1;
        }
    }
    if (info.time >= 0.0f) {
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
        
        if (discriminant >= 0) {
            return true;
        } else {
            return false;
        }
    }
    return false;

}
// Function glm::dot(x,y) will return the dot product of parameters. (It's the inner product of vectors)

/* TODO: Implement */
bool Plane::Intersect(const Ray &ray, IntersectInfo &info) const { return -1.0f; }

/* TODO: Implement */
bool Triangle::Intersect(const Ray &ray, IntersectInfo &info) const { return -1.0f; }
