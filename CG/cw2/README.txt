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
-Refraction: 
By tracking the type of object last hit, and tracing rays through spheres, obeying Snell's laws, basic refraction can be added. The system implemented here is extremely simplified, just tracking an integer for the type of object hit, and does not support, for instance, sphere instersected with one another. The ratio of reflected to refracted light is simplified to: totalLight = (1-refractionCoeff)*reflectedLight + refractionCoeff*refractedLight, which may well be entirely wrong, but at least produces something vaguely resembling refraction. Unfortunately, I ran into issues implementing a more robust method for refraction, and eneded up not having the time to fully complete it. The implementation here is rather sloppy, and goes roughly as follows:

-if a ray hits a refractive surface (jusdged by checking the refraction coefficient of tha material hit)
    -check if the "lastObjectHitID" is 1 - the integer code for a sphere
        -if it is, this means we are currently exiting a sphere, so the ratio of refractive indices is set to 1/sphereIndex
        -if not, we are entering an object, so set the ratio of refractive indices to objectIndex/1
        --This is where the limitation comes into play, as we are assuming here that a refractive sphere must be entered/exited without anything other intersections occurring

    -calculate refraction by "bending" rays according to Snell's law (the vector form)[2] and continuing ray casting recursively (there is likely a bug here, as there is no limit imposed on the number of refractions that can take place - this could result in unbounded rafraction, again, not something I had time to fully explore) and remember if refraction did in fact take place (total internal reflection could occur, removing the need for refracted light in the final pixel value)
-if refraction occurred, use the above (likely incorrect) equation to give the final light value of the pixel, otherwise just use reflected light

-the "lastObjectHitID" is reset to 0 (air) ready for the next ray to be cast


TO RUN:
Simply "make run" from main directory.

REFERENCES:
[1] - http://www.inf.ed.ac.uk/teaching/courses/cg/lectures/slides9-2015.pdf (Slides 30-39)
[2] - https://en.wikipedia.org/wiki/Snell%27s_law#Vector_form
