include <motor-gears.scad>
include <motor-gear-mount.scad>
include <arm.scad>
include <mouf_parts.scad>
include <BOSL2/std.scad>



module hull_head() {
    head();

    difference() {
        intersection() {
            difference() {
                difference() {
                    difference() {
                        union() {
                            rotate([90,0,90]) translate([0,18,20]) scale([1, 1.5, 2.9]) torus(r_maj=25, r_min=8);
                        }
                        translate([30,0,45]) cube([80,80,50], center=true);
                    }
                    translate([-4.5,0,0]) cube([5,80,50], center=true);
                }
                translate([7,0,0]) cube([10,6,20], center=true);
            }
            
            translate([15,0,-30]) color("red", 0.2) sphere(50);
        }
        translate([15,0,20]) color("red", 0.2) sphere(30);
   }
}    

hull_head();