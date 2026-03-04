include <motor-gears.scad>
include <motor-gear-mount.scad>
include <arm.scad>
include <mouf_parts.scad>


module hull_t_up() {
    {
     //color("green") translate([-51.2,-10,-45]) cube([MG_MOUNT_SIZE.x-2*MG_MOUNT_W,20,50]);
     t_up(); 
     difference() {
         difference() {   
           difference() {
                hull()t_up();
                translate([-51.2,-10,-48]) cube([MG_MOUNT_SIZE.x-2*MG_MOUNT_W,20,50]);
            }
            translate([-21.2,-10,-46.5]) cube([40,30,48]);
        }
        //#translate([-55,-10,-28.2]) cube([MG_MOUNT_SIZE.x,10,MG_MOUNT_SIZE.y]);
        rotate([90,0,0]) translate([-51,-22,-20]) cylinder(30, r=4);
        rotate([90,0,0]) translate([-29.2,-22,-20]) cylinder(30, r=4);
        rotate([90,0,0]) translate([-35.2,-22,-20]) cylinder(30, r=4);
        }
    }
}

//hull_t_up();