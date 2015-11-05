The payload tracks what the last object hit was. Upon a ray hitting a face of a refractive sphere, if the last object hit was the same sphere, we know we are re-enting air, and can clear the last object hit, and use the refractive index of air to re-direct the ray. Otherwise, if we hit a refractive object that was not hit last, we use the refractive index of that object to calculate refraction. 

Material reflection/refraction should sum to 1 at the most, as an object shouldn't be able to amplify light (transmission + reflection + refraction should total to 100% of the original light).
