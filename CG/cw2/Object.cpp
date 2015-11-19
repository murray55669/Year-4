#include "Object.h"
#include <typeinfo>

float depthMin = 0.01f;

Material::Material():
    ambient(1.0f),
    diffuse(1.0f),
    specular(1.0f),
    glossiness(10.0f),
    reflection(0.0f),
    refraction(0.0f),
    refractiveIndex(0.0f)
  {}

Object::Object(const glm::mat4 &transform, const Material &material):
    transform(transform),
    material(material)
  {}

bool Sphere::Intersect(const Ray &ray, IntersectInfo &info) const { 
    glm::vec3 d = ray.direction;
    glm::vec3 e = ray.origin;
    glm::vec3 s = Position();
    float r = radius;
    
    glm::vec3 e_min_s = e-s;
    float d_dot_d = glm::dot(d, d);
    
    float discriminant = pow( (glm::dot((2.0f*ray.direction), (e_min_s))) , 2.0f) - 
                        4.0f*(d_dot_d)*(glm::dot((e_min_s), (e_min_s))-pow(r, 2.0f));

    float front = -2.0f*glm::dot(d, (e_min_s));
    float discriminant_sqrt = sqrt(discriminant);
    
    // The time along the ray that the intersection occurs 
    float t1 = (front + discriminant_sqrt) / (2.0f*d_dot_d);
    float t2 = (front - discriminant_sqrt) / (2.0f*d_dot_d);
    
    bool intersected = false;
    
    if (t1 >= 0.0f) {
        if ((t1 < t2)) {
            info.time = t1;
            intersected = true;
        }
        else if (t2 >= 0.0f) {
            info.time = t2;
            intersected = true;
        } 
    }
    
    if (intersected) {
        info.material = MaterialPtr();
        info.hitPoint = ray(info.time);
        
        //N = ((x - cx)/R, (y - cy)/R, (z - cz)/R) ** skip the /R as we normalize anyway
        info.normal = glm::normalize(info.hitPoint - s);
        
        info.objectHit = thisObject();
        info.objectHitId = OjbectID();
        
        return true;
    }
    return false;

}
// Function glm::dot(x,y) will return the dot product of parameters. (It's the inner product of vectors)

bool Plane::Intersect(const Ray &ray, IntersectInfo &info) const { 
    glm::vec3 d = ray.direction;
    glm::vec3 e = ray.origin;
    glm::vec3 s = Position();
    glm::vec3 n = Normal();
    
    float d_dot_n = glm::dot(d, n);
    
    //if plane is not parallel to ray
    if (!(d_dot_n == 0.0f)) {
        
        float time = (glm::dot((s-e), n)) / (d_dot_n);
        
        if (time > 0.0f) {
        
            info.time = time;
            
            info.material = MaterialPtr();
            info.hitPoint = ray(info.time);
            
            info.normal = n;
            
            info.objectHit = thisObject();
            info.objectHitId = OjbectID();
            
            return true;
        }
    } 
    
    return false; 
    
}

bool Triangle::Intersect(const Ray &ray, IntersectInfo &info) const { 
   
    glm::vec3 d = ray.direction;
    glm::vec3 e = ray.origin;
    glm::vec3 n = Normal();
    
    float d_dot_n = glm::dot(d, n);
    
    glm::vec2 hP; //(x, y)
    glm::vec2 points2D [3];//(x0, y0), (x1, y1), (x2, y2)

    
    //if triangle is not parallel to ray
    if (!(d_dot_n == 0.0f)) {
        
        float time = (glm::dot((points[0]-e), n)) / (d_dot_n);
        
        if (time > 0.0f) {
        
            glm::vec3 hitPoint = ray(time);
            
            //project onto a plane
            int maxN = MaxNormalIndex();
            if (maxN == 0) {
                hP = glm::vec2(hitPoint.y, hitPoint.z);
                for (int i = 0; i < 3; ++i) {
                    points2D[i] = glm::vec2(points[i].y, points[i].z);
                }
            } else if (maxN == 1) {
                hP = glm::vec2(hitPoint.x, hitPoint.z);
                for (int i = 0; i < 3; ++i) {
                    points2D[i] = glm::vec2(points[i].x, points[i].z);
                }
            } else {
                hP = glm::vec2(hitPoint.x, hitPoint.y);
                for (int i = 0; i < 3; ++i) {
                    points2D[i] = glm::vec2(points[i].x, points[i].y);
                }
            }
            
            float a1 = BaryF(points2D[1], points2D[2], hP);
            float a2 = BaryF(points2D[1], points2D[2], points2D[0]);
            float b1 = BaryF(points2D[2], points2D[0], hP);
            float b2 = BaryF(points2D[2], points2D[0], points2D[1]);
            float g1 = BaryF(points2D[0], points2D[1], hP);
            float g2 = BaryF(points2D[0], points2D[1], points2D[2]);
            float alpha = a1/a2; 
            float beta =  b1/b2; 
            float gamma = g1/g2 ;

            
            //test for point being within triangle using barycentric coordinates
            if ((alpha >= 0 && alpha <= 1) && (beta >= 0 && beta <= 1) && (gamma >= 0 && gamma <= 1)) {
                info.time = time;
                
                info.material = MaterialPtr();
                info.hitPoint = hitPoint;
                
                info.normal = n;
                
                info.objectHit = thisObject();
                info.objectHitId = OjbectID();
                
                return true;    
            }
        }
        
    } 
    
    return false;
    
}

float Triangle::BaryF(glm::vec2 p, glm::vec2 q, glm::vec2 z) const {
    float f;
    
    f = (q.y-p.y)*z.x - (q.x-p.x)*z.y + q.x*p.y - q.y*p.x;
    
    return f;
}
int Triangle::MaxNormalIndex() const {
    glm::vec3 n = Normal();
    n = glm::vec3(abs(n.x), abs(n.y), abs(n.z));
    
    //x is the largest
    if ((n.x >= n.y) && (n.y >= n.z)) {
        return 0;
    }
    //y is the largest
    else if ((n.y >= n.x) && (n.x >= n.z)) {
        return 1;
    }
    //z is the largest
    else {
        return 2;
    }
        
}