// MG90S 3-Axis Joint - Zero Hardcoded Values
// Designed for a 3-segment line with Yaw, Pitch, and Roll capability

/* [Joint Controls] */
Yaw_Angle     = 20; 
Pitch_Angle   = 30; 
Roll_Angle    = 45;

/* [Servo Constants (MG90S Spec)] */
S_Width       = 12.2; // Width of the servo body
S_Length      = 22.8; // Length of the main rectangular body block
S_Body_H      = 22.5; // Total height of the main plastic housing
S_Shaft_Off   = 6.0;  // Offset from front edge to gear center (critical for alignment)
S_Flange_L    = 32.5; // Total length including mounting "ears"
S_Flange_H    = 2.2;  // Thickness of the mounting flanges
S_Flange_Z    = 16.0; // Distance from bottom of body to bottom of flange
S_Shaft_D     = 4.8;  // Diameter of the output gear/shaft
S_Shaft_H     = 5.0;  // Height of the shaft above the body
S_Horn_L      = 15.0; // Length of the plastic horn/arm
S_Horn_T      = 2.5;  // Thickness of the servo horn

/* [Bracket Constants] */
thick         = 3.0;   // Structural wall thickness
clearance     = 0.1;   // Precision tolerance
pivot_z       = 25.0;  // Center of rotation for Pitch axis
base_gap      = 5.0;   // Vertical space above Yaw horn
yoke_arm_w    = 20.0;  // Width of the bracket arms
pin_d         = 5.0;   // Passive pivot pin diameter

// Calculated widths to ensure perfect nesting
inner_w       = S_Body_H; 
outer_w       = inner_w + (thick * 2) + (clearance * 2) + (thick * 2);

$fn = 50;

module mg90s_core(rotation=0) {
    // 1. Static Body
    color("DimGray") {
        translate([-S_Shaft_Off, -S_Width/2, -S_Body_H])
            cube([S_Length, S_Width, S_Body_H]);
    }
    color("Gray") {
        translate([-(S_Flange_L-S_Length)/2 - S_Shaft_Off, -S_Width/2, -S_Body_H + S_Flange_Z])
            cube([S_Flange_L, S_Width, S_Flange_H]);
    }
    // 2. Rotating Output
    rotate([0, 0, rotation]) {
        color("Gold") cylinder(d=S_Shaft_D, h=S_Shaft_H);
        color("White") translate([-2, -S_Width/2, S_Shaft_H - 1]) 
            cube([S_Horn_L, S_Width, S_Horn_T]);
    }
}

module inner_yoke_blue(w, h, t) {
    color("RoyalBlue", 0.6) {
        translate([-yoke_arm_w/2, -w/2 - t, 0]) cube([yoke_arm_w, w + (t * 2), t]);
        for(side = [-1, 1]) {
            translate([-yoke_arm_w/2, (w/2 + t) * side - (side==1 ? t : 0), 0])
                difference() {
                    cube([yoke_arm_w, t, h]);
                    if(side == 1) // Passive Hole
                        translate([yoke_arm_w/2, t/2, h - 10]) 
                            rotate([90, 0, 0]) cylinder(d=pin_d + 0.2, h=t+2, center=true);
                }
        }
    }
}

module head(w, h, d, t) {
    color("Red", 0.6) {
        translate([-d/2, -w/2 - t, 0]) cube([d, w + (t * 2), t]);
        rotate([90, 0, 0]) cylinder(d=8, h=40, center=true);
        for(side = [-1, 1]) {
            translate([-d/2, (w/2 + t) * side - (side==1 ? t : 0), 0])
                 cube([d, t, h]);
        }
    }
}

module feet(w, h, d, t) {
    color("Green", 0.6) {
        rotate([0,0,90]) {
            translate([-d/2, -w/2 - t, 0]) cube([d, w + (t * 2), t]);
            for(side = [-1, 1]) {
                translate([-d/2, (w/2 + t) * side - (side==1 ? t : 0), 0])
                        cube([d, t, h]);
            }
        }
    }
}

module outer_yoke_purple(w, h, t) {
    color("Purple", 0.7) {

        translate([yoke_arm_w/2, -yoke_arm_w/2, h]) rotate([90, 0, 90]) cube([yoke_arm_w, w, t]);
        
        translate([-yoke_arm_w/2, -w/2, h]) cube([yoke_arm_w, w, t]);

        for(side = [-1, 1]) {
            translate([-yoke_arm_w/2, (w/2) * side - (side==1 ? t : 0), 0]) {
                cube([yoke_arm_w, t, h + t]);
                if(side == 1) // Passive Pin
                    translate([yoke_arm_w/2, 0, h - 10]) 
                        rotate([90, 0, 0]) cylinder(d=pin_d, h=t + clearance + 1);
            }
        }
    }
}

module joint_assembly() {
    // 1. YAW (Servo 1)
    mg90s_core(Yaw_Angle);
    translate([S_Shaft_Off , 0,-(S_Body_H+thick)]) feet(S_Length,20,S_Width,thick);

    rotate([0, 0, Yaw_Angle]) 
    translate([0, 0, S_Shaft_H ]) {
        
        inner_yoke_blue(inner_w, pivot_z + 10, thick);
        
        // 2. PITCH (Servo 2)
        translate([0, 0, pivot_z])
        rotate([90, 0, 0]) rotate([0, 0, 90]) {
            
            translate([-S_Horn_L, 0, inner_w/2])
                mg90s_core(Pitch_Angle);
            
            // 3. ROLL (Servo 3 & Outer Yoke)
            rotate([0, 0, Pitch_Angle])
            translate([0, 0, inner_w/2 + (thick * 3) - clearance]) {
                
                // Align purple yoke to wrap over blue
                rotate([-90, 0, -90])
                translate([-pivot_z/4, 20, -outer_w/2])
                    outer_yoke_purple(outer_w, pivot_z + 10, thick);
                
                // 4. THE ROLL SERVO
                // Mounted to the top of the Purple Yoke
                translate([35, 0, -20])
                rotate([90, Roll_Angle, 0]) {
                    mg90s_core(Roll_Angle);
                    
                    rotate([0, -90, 0]) translate([-(thick + 2/2) , 0, -20]) head(S_Width, 15, 20, thick)
                    // Final End Effector
                    rotate([0, 0, Roll_Angle])
                    color("Red") translate([0, 0, S_Shaft_H + 5]) 
                        cylinder(d1=2, d2=0, h=25);
                }
            }
        }
    }
}

joint_assembly();
%translate([0,0,-30]) cylinder(d=0.5, h=160);