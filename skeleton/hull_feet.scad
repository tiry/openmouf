include <motor-gears.scad>
include <motor-gear-mount.scad>
include <arm.scad>
include <mouf_parts.scad>
include <BOSL2/std.scad>



module hull_feet() {
    feet_box();
    
    difference() {
    
        difference() {
            difference() {
                difference() {
                    union() {
                        hull() feet_box();
                        translate([-5,0,19]) scale([1.3, 0.75, 1.4]) sphere(20);
                        translate([10,-2,3]) scale([1, 1, 1]) sphere(10);
                        translate([-18,-2,3]) scale([1, 1, 1]) sphere(10);
                    
                    }
                    translate([-40,-20,20]) cube([80,40,40]);
                }
                translate([-MG90S_FULL_SIZE.x/2,-MG90S_FULL_SIZE.y/2,-3]) cube([MG90S_FULL_SIZE.x,MG90S_FULL_SIZE.y,40]);
           }
       
       translate([-10.5,0,-30]) cylinder(h=40, r=2);
       translate([10.5,0,-30]) cylinder(h=40, r=2);
       }
   
    translate([-45,9,-10]) cube([80,20,50]);
    }
}    

hull_feet();