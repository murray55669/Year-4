#version 130

//Input position (coordinates within texture)
in vec2 pos;

//Texture maps for the image drawn on the screen, and the Z-buffer
uniform sampler2D tex;
uniform sampler2D depth;

//Final output colour
out vec4 outColour;

void main() {
        //Depth
        vec4 depthMap = texture(depth, vec2(pos.x, pos.y));
        float depthScaled = pow(10 * depthMap.x, 2);
        float dSReduced = depthScaled / 20000;

        //Chromatic abberation based on depth
        float abbDist = dSReduced;
        
        vec4 red = texture(tex, vec2(pos.x+abbDist, pos.y));
        vec4 green = texture(tex, vec2(pos.x, pos.y));
        vec4 blue = texture(tex, vec2(pos.x-abbDist, pos.y));
        
        outColour = vec4(red.x, green.y, blue.z, 1.0); 
        
        //Modify this code to read from the texture and add extra effects!
        //Read the colour from the texture and output it directly to the screen
//      vec4 col=texture(tex,vec2(pos.x,pos.y));
//      outColour=col;
}
