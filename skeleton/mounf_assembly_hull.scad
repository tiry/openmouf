include <motor-gears.scad>
include <motor-gear-mount.scad>
include <arm.scad>

include <hull_head2.scad>
include <hull_t_up.scad>
include <hull_t_bottom.scad>
include <hull_feet.scad>


MARGIN = 0.2;
$fn = 60;

/* [Joint Controls] */
//Yaw_Angle     = 20; 
//Pitch_Angle   = 45; 
//Roll_Angle    = 25;

Pitch_Angle = 25 * sin($t * 360);
Yaw_Angle   = 45 * cos($t * 360); 
Roll_Angle  = 20 * cos($t * 360 + 90); 


module mouf_sk(pitch=0, yaw=0, roll=0, double_arm=false) {
    // Feet Servo : Roll
    union() {
        mg90s();
        translate([0, 0, -2]) color("green") hull_feet();
        // arm
        translate([-(MG90S_BLOCK_SIZE.x/2 - MG90S_FULL_SIZE.y/2), 0, MG90S_FULL_SIZE.z]) 
            rotate([0, 0, roll]) servo_arm_dual();
    }

    translate([-(MG90S_BLOCK_SIZE.x/2 - MG90S_FULL_SIZE.y/2), 0, 0]) rotate([0, 0, roll]) 
    translate([0, 0, 55]) union() {
        // Middle Body : Pitch    
        color("red") hull_t_bottom();
        translate([-10, 0, 0]) rotate([0, 90, 0]) mg90s();
        
        translate([-10, 0, 0]) rotate([0, 90, 0]) {
            translate([-(MG90S_BLOCK_SIZE.x/2 - MG90S_FULL_SIZE.y/2), 0, MG90S_FULL_SIZE.z]) 
            rotate([0, 0, pitch]) union() {
                servo_arm();
                color("blue") hull_t_up();
                
                // Head : yaw        
                rotate([90, 0, 0]) translate([-40, -22, -10]) {
                    mg90s();
                    translate([-(MG90S_BLOCK_SIZE.x/2 - MG90S_FULL_SIZE.y/2), 0, MG90S_FULL_SIZE.z]) 
                    rotate([0, 0, yaw]) union() {
                        servo_arm();    
                        rotate([0, 90, 0]) translate([-2, 0, -14]) color("pink") hull_head();
                    }
                }
            }
        }
    }
}

mouf_sk(pitch=Pitch_Angle, yaw=Yaw_Angle, roll=Roll_Angle);