include <motor-gears.scad>
include <motor-gear-mount.scad>
include <arm.scad>
include <mouf_parts.scad>
include <BOSL2/std.scad>



module hull_head() {
    head();

    difference() {
        difference() {
            difference() {
                union() {
                    rotate([90,0,90]) translate([0,12,25]) scale([1, 1, 2.2]) torus(r_maj=25, r_min=8);
                    rotate([90,0,90]) translate([0,12,3])  torus(r_maj=20, r_min=8);
                }
                translate([30,0,40]) cube([80,80,50], center=true);
            }
            translate([-4.5,0,0]) cube([5,80,50], center=true);
        }
        translate([7,0,0]) cube([10,6,20], center=true);
    }
    
}

hull_head();