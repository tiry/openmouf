include <motor-gears.scad>
include <motor-gear-mount.scad>
include <arm.scad>
include <mouf_parts.scad>


rotate([-90,0,0]) translate([0,-10,0])  feet_box();


rotate([0,90,0]) translate([-32,60,0])  head();


rotate([-90,0,0]) translate([10,-15,-40])  color("red") t_up();


rotate([-90,0,0]) translate([50,-8,-40])   t_bottom();


color("Blue") square(200, center = true);