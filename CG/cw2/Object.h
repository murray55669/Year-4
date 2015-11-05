#pragma once

#include "Ray.h"

class Material {
  public:
    Material();
    glm::vec3 ambient; //Reflectivity in r/g/b channels
    glm::vec3 diffuse;   
    glm::vec3 specular;	
    float glossiness; //Specular intensity
    float reflection;
};

// The father class of all the objects displayed. Some features would be shared between objects, others will be overloaded.
class Object {
  public:
    Object(const glm::mat4 &transform = glm::mat4(1.0f), const Material &material = Material());
    //  The keyword const here will check the type of the parameters and make sure no changes are made
    //  to them in the function. It's not necessary but better for robustness
    int SetMaterial(Material &mat) {
        this->material = mat;
    }
    int SetPosition(glm::vec3 pos) {
        transform[3][0] = pos[0];
        transform[3][1] = pos[1];
        transform[3][2] = pos[2];
    }

    virtual bool Intersect(const Ray &ray, IntersectInfo &info) const { return true; }
    glm::vec3 Position() const { return glm::vec3(transform[3][0], transform[3][1], transform[3][2]); }
    const Material *MaterialPtr() const { return &material; }

  protected:  //  The difference between protected and private is that the protected members will still be available in subclasses.
    glm::mat4 transform;  // Usually a transformation matrix is used to decribe the position from the origin.
    Material material;
};

//  For all those objects added into the scene. Describing them in proper ways and the implement of function Intersect() is what needs to be done.
//  Actually, it's also possible to use some other objects, but those geometries are easy to describe and the intersects are easier to calculate.
//  Try something else if you like, for instance, a box?

// IMPLEMENTED IN Object.cpp ??
/* TODO: Implement */
class Sphere : public Object {
  public:
    float radius;
    float Radius() const { return radius; }
      
    virtual bool Intersect(const Ray &ray, IntersectInfo &info) const; //  To figure out if the Ray hit this object.
    
};

/* TODO: Implement */
class Plane : public Object {
    public:
        glm::vec3 normal;
        glm::vec3 Normal() const { return normal; }
        
        virtual bool Intersect(const Ray &ray, IntersectInfo &info) const;
};

/* TODO: Implement */
class Triangle : public Object {
    public:
        glm::vec3 Normal() const { 
            return glm::normalize(glm::cross((points[0] - points[1]), (points[2] - points[0])));
        }
        
        glm::vec3 points [3];
      
        glm::vec3 P(int i) const { return points[i]; }

        int SetPoints(glm::vec3 pos1, glm::vec3 pos2, glm::vec3 pos3) {
            points[0] = pos1;
            points[1] = pos2;
            points[2] = pos3;
        }
    
        virtual bool Intersect(const Ray &ray, IntersectInfo &info) const;
        float BaryF(glm::vec2 p, glm::vec2 q, glm::vec2 z) const;
        int MaxNormalIndex() const;
};
