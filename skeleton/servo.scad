include <motor-gears.scad>
include <motor-gear-mount.scad>

mg90s();

// Total Width
color("red") translate([-16,6,18])cube([MG90S_FULL_SIZE.x,1,1]);

// Total height
color("green")  translate([-10,0,0])cube([1,1,MG90S_FULL_SIZE.z]);

// Total height
color("green")  translate([-12,0,0])cube([1,1,MG90S_GEAR_H1]);

// LAT WIDTH
color("blue")  translate([-11.2,6,8])cube([MG90S_LAT_WIDTH,1,1]);

// 
color("cyan") rotate([0,0,90])translate([-6,-12,12])cube([MG90S_FULL_SIZE.y,1,1]);

// block height
rotate([0,90,0])translate([-22,-5,-12])cube([MG90S_BLOCK_SIZE.z,1,1]);

translate([0,0,-5]) gear_mount();