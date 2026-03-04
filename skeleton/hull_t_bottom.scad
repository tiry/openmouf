include <motor-gears.scad>
include <motor-gear-mount.scad>
include <arm.scad>
include <mouf_parts.scad>
include <BOSL2/std.scad>



module hull_t_bottom() {
    t_bottom();
    
    difference() {
    
        difference() {
            hull() t_bottom();
            
            translate([-14,-10,-MG90S_FULL_SIZE.x/2-1]) cube([40,30,MG90S_FULL_SIZE.x]);
            
            translate([-27,-10,-24]) cube([5,30,45]);
        }
        
        rotate([0,90,0]) translate([-4,0,-28]) cylinder(h=10, r=5);
        rotate([0,0,0]) translate([-12,0,10]) cylinder(h=10, r=3);
        rotate([90,0,0]) translate([-14,-12,-20]) cylinder(h=40, r=3);
    }
    
    rotate([90,90,0]) translate([-20,-10,6]) base();
}    

//hull_t_bottom();