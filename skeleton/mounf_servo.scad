include <motor-gears.scad>
include <motor-gear-mount.scad>
include <arm.scad>
include <roundedcube.scad>

MARGIN = 0.2;
$fn = 60;

/* [Joint Controls] */
//Yaw_Angle     = 20; 
//Pitch_Angle   = 45; 
//Roll_Angle    = 25;

Pitch_Angle = 25 * sin($t * 360);
Yaw_Angle   = 45 * cos($t * 360); 
Roll_Angle  = 20 * cos($t * 360 + 90); 

module servo(angle=0, double_arm=false) {
    mg90s();
    translate([0, 0, -2]) gear_mount();
    translate([-(MG90S_BLOCK_SIZE.x/2 - MG90S_FULL_SIZE.y/2), 0, MG90S_FULL_SIZE.z]) 
        rotate([0, 0, angle]) 
            if (double_arm) { 
                servo_arm_dual(); 
            } else { 
                servo_arm(); 
            };
}

module feet_box() {
    gear_mount();
    translate([MG90S_FULL_SIZE.x/2 - 1, -MG90S_FULL_SIZE.y/2, 7]) 
        cube([5, MG90S_FULL_SIZE.y, 13]);
    
    translate([19.5, 2, 5]) rotate([20, -20, 0]) union() {
        cylinder(h=20, d=8, center=true);
        translate([0, 0, -10]) sphere(d=8);
    }
    
    translate([-MG90S_FULL_SIZE.x/2 - 14, -MG90S_FULL_SIZE.y/2, 7]) 
        cube([15, MG90S_FULL_SIZE.y, 13]);
    
    translate([-29.5, 2, 5]) rotate([20, 20, 0]) union() {
        cylinder(h=20, d=8, center=true);
        translate([0, 0, -10]) sphere(d=8);
    }
}

module head() {
    union() {
        rounded_cube([4, MG90S_FULL_SIZE.y, 35], center=true, r=2);
        rotate([0, 90, 0]) translate([13, 0, 0]) cylinder(h=25, r=4);
        rotate([90, 0, 0]) translate([25, -13, -15]) cylinder(h=30, r=4);
        
        rotate([135, 0, 0]) translate([25, -19, -19]) union() {
            cylinder(h=20, r=4);
            translate([0, 0, 0]) sphere(d=8);
        };
        
        rotate([-135, 0, 0]) translate([25, 19, -19]) union() {
            cylinder(h=20, r=4);
            translate([0, 0, 0]) sphere(d=8);
        };
    }
}

module t_up() {
    color("blue") union() {    
        translate([0, 0, -48]) cylinder(h=8, r=3, center=false);
        translate([5, 0, -23]) rotate([0, -90, 0]) union() {
            translate([-24, 0, 15]) 
                rounded_cube([4, MG90S_FULL_SIZE.y, 30], center=true, r=2);
            translate([0.5, 0, 28]) 
                rounded_cube([53, MG90S_FULL_SIZE.y, 4], center=true, r=2);
            translate([25, 0, 15]) 
                rounded_cube([4, MG90S_FULL_SIZE.y, 30], center=true, r=2);
        }
    }        
    rotate([90, 0, 0]) translate([-40, -22, -10]) {
        translate([0, 0, -2]) gear_mount();
    }
}

module t_bottom() {
    difference() {
        union() {
            translate([-0, 0, -20]) 
                rounded_cube([50, MG90S_FULL_SIZE.y, 5], center=true, r=2);
            translate([-20, 0, 0]) 
                cube([4, MG90S_FULL_SIZE.y, 40], center=true);
        }
        rotate([0, 90, 0]) translate([-4.8, 0, -48]) 
            cylinder(h=80, r=3 + MARGIN, center=false);
    }
    translate([-10, 0, 0]) {
        translate([7, 0, -16]) 
            cube([22, MG90S_FULL_SIZE.y, 3], center=true);
        rotate([0, 90, 0]) translate([0, 0, -2]) gear_mount();
    }
}

module mouf_sk(pitch=0, yaw=0, roll=0, double_arm=false) {
    // Feet Servo : Roll
    union() {
        mg90s();
        translate([0, 0, -2]) color("green") feet_box();
        // arm
        translate([-(MG90S_BLOCK_SIZE.x/2 - MG90S_FULL_SIZE.y/2), 0, MG90S_FULL_SIZE.z]) 
            rotate([0, 0, roll]) servo_arm_dual();
    }

    rotate([0, 0, Roll_Angle]) 
    translate([-4, 2, 55]) union() {
        // Middle Body : Pitch    
        color("red") t_bottom();
        translate([-10, 0, 0]) rotate([0, 90, 0]) mg90s();
        
        translate([-10, 0, 0]) rotate([0, 90, 0]) {
            translate([-(MG90S_BLOCK_SIZE.x/2 - MG90S_FULL_SIZE.y/2), 0, MG90S_FULL_SIZE.z]) 
            rotate([0, 0, pitch]) union() {
                servo_arm();
                color("blue") t_up();
                
                // Head : yaw        
                rotate([90, 0, 0]) translate([-40, -22, -10]) {
                    mg90s();
                    translate([-(MG90S_BLOCK_SIZE.x/2 - MG90S_FULL_SIZE.y/2), 0, MG90S_FULL_SIZE.z]) 
                    rotate([0, 0, yaw]) union() {
                        servo_arm();    
                        rotate([0, 90, 0]) translate([-2, 0, -14]) color("pink") head();
                    }
                }
            }
        }
    }
}

mouf_sk(pitch=Pitch_Angle, yaw=Yaw_Angle, roll=Roll_Angle);