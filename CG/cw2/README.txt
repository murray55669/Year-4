IMPLEMENTED:
-RayTracer.cpp:
--CheckIntersection(Ray, IntersectInfo)
    This function, as suggested, simply runs the "Intersect" function (detailed below) on each object in the scene, to check if the given ray intersects with it. If an intersection is found, the function returns "true," otherwise it returns "false." It also ensures that the IntersectInfo object (updated by each "Intersect" call) retains the information of the nearest intersection found. This ensures, among other things, that objects are rendered in the correct order, depending on depth.
--CastRay(Ray, Payload)
    This function calculates the colour of a pixel, taking into account:
        -whether or not a point is in shadow
        -whether or not a point has reflected light hitting it
        -whether or not a point has refracted light hitting it
    The "initial" colour value for a point is calculated here, using Phong illumination. If the point is in shadow, only ambient light is used. This initial value is then combined with any reflected/refracted light, by recursively casting rays into the scene to a pre-defined depth, to generate a final colour value.

-Object.cpp:
--Intersect(Ray, IntersectInfo)
    This function checks to see if a given "Ray" intersects with the object being tested. It has three implementations, one each for speheres, planes, and triangles.[1]
    -Sphere intersection: based on checking the discriminant, then calculating time value(s) for when the sphere was hit, and other values based off this.
    -Plane intersection: based on ensuring the plane is not parallel to the ray, then calculating time values for when the plane was hit
    -Triangle intersection: an extention of plane intersection testing, using barycentric co-ordinates to check if the point hit was within a triangle. The technique involves stripping one axis from the coordinates (the axis corresponding to the coordinate of the normal with the largest magnitude), to project the triangle onto a 2d plane, and then checking the barycentric coordinates are within the appropriate area.
    

    In each case, the "IntersectionInfo" is updated with the time of intersection, material of the object being hit, point at which the intersection occurred, surface normal at the point, and the object itself that was hit (used later in refraction to decide if a ray is entering/exiting an object)

EXTRA FEATURES:
-Refraction: [2]
To decide if we're entering/exiting an object, we need to keep track of the last object hit, and check what object we hit on any intersection of ray and object. To do so "IntersectInfo" is updated with the object hit, when an intersection occurs, and this can be compared against a record of the last object hit/it's refractive index. This allows a refractive index ratio to be created ("r"), then used to determine if refraction occurs, or if total internal reflection takes place instead. The refracted ray's direction can then be calculated as needed, and recursive ray casting can take place.

NB:
To my understanding, material reflection/refraction should sum to 1 at the most, as an object shouldn't be able to amplify light (transmission + reflection + refraction should total to 100% of the original light).

TO RUN:
Simply "make run" from main directory.

REFERENCES:
[1] - http://www.inf.ed.ac.uk/teaching/courses/cg/lectures/slides9-2015.pdf (Slides 30-39)
[2] - https://en.wikipedia.org/wiki/Snell%27s_law#Vector_form
