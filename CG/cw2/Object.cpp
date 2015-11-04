#include "Object.h"

float timeMin = 0.1f;

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
        if ((t1 < t2) && (t1 >= timeMin)) {
            info.time = t1;
            intersected = true;
        }
        else if (t2 >= timeMin) {
            info.time = t2;
            intersected = true;
        } else if (t1 >= timeMin) {
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
bool Plane::Intersect(const Ray &ray, IntersectInfo &info) const { 
    //check d.n
    glm::vec3 d = ray.origin;
    glm::vec3 e = ray.direction;
    glm::vec3 s = Position();
    glm::vec3 n = Normal();
    
    //printf("[%f, %f, %f]\n", n[0], n[1], n[2]);
    
    float d_dot_n = glm::dot(d, n);
    
    //if plane is not parallel to ray
    if (!(d_dot_n == 0.0f)) {
        
        info.time = (glm::dot((s-e), n)) / (d_dot_n);
        
        info.material = MaterialPtr();
        info.hitPoint = ray(info.time);
        
        info.normal = n;
        
        return true;
    } 
    
    return false; 
    
}

/* TODO: Implement */
bool Triangle::Intersect(const Ray &ray, IntersectInfo &info) const { 
//check d.n
    glm::vec3 d = ray.origin;
    glm::vec3 e = ray.direction;
    glm::vec3 p1 = P1();
    glm::vec3 p2 = P2();
    glm::vec3 p3 = P3();
    
    glm::vec2 hP; //(x, y)
    glm::vec2 points2D [3];//(x0, y0), (x1, y1), (x2, y2)
    
    glm::vec3 n = Normal();
    
    float d_dot_n = glm::dot(d, n);
    
    //if triangle is not parallel to ray
    if (!(d_dot_n == 0.0f)) {
        float time = (glm::dot((p1-e), n)) / (d_dot_n); //time ray hits plane extension of triangle
        glm::vec3 hitPoint = ray(time); //point where "plane" is hit
        
        //remove one co-ordinate and check if hitpoint is within triangle using barycentric co-ords
        if ((n[0] >= n[1]) && (n[1] >= n[2])) {
            hP = glm::vec2(hitPoint[1], hitPoint[2]);
            points2D[0] = glm::vec2(p1[1], p1[2]);
            points2D[1] = glm::vec2(p2[1], p2[2]);
            points2D[2] = glm::vec2(p3[1], p3[2]);
        } else if ((n[2] >= n[1]) && (n[1] >= n[0])) {
            hP = glm::vec2(hitPoint[0], hitPoint[1]);
            points2D[0] = glm::vec2(p1[0], p1[1]);
            points2D[1] = glm::vec2(p2[0], p2[1]);
            points2D[2] = glm::vec2(p3[0], p3[1]);
        } else {
            hP = glm::vec2(hitPoint[0], hitPoint[2]);
            points2D[0] = glm::vec2(p1[0], p1[2]);
            points2D[1] = glm::vec2(p2[0], p2[2]);
            points2D[2] = glm::vec2(p3[0], p3[2]);
        }
        
        float alpha = BaryF(1, 2, points2D, hP) / BaryF(1, 2, points2D, points2D[0]);
        float beta = BaryF(2, 0, points2D, hP) / BaryF(1, 2, points2D, points2D[1]);
        float gamma = BaryF(0, 1, points2D, hP) / BaryF(1, 2, points2D, points2D[2]);
        
        if ((alpha >=0 && alpha <= 1) && (beta >= 0 && beta <= 1) && (gamma >= 0 && gamma <= 1)) {
            info.time = time;
            
            info.material = MaterialPtr();
            info.hitPoint = hitPoint;
            
            info.normal = n;
            
            return true;    
        }
        
    } 
    
    return false; 
}

float Triangle::BaryF(int a, int b, glm::vec2 points2D[], glm::vec2 hP) const {
    float fab;
    
    fab = ((points2D[a][1] - points2D[b][1])*hP[0]) + ((points2D[b][0] - points2D[a][0])*hP[1]) + (points2D[a][0] * points2D[b][1]) - (points2D[b][0] * points2D[a][1]);
    
    return fab;
}
