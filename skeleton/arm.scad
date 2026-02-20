/* [Servo Horn Parameters] */
horn_length    = 21.0; // Total length from center
double_horn_length    = 18.9; // Total length from center
horn_height    = 1.4;  // Thickness of the arm plate
hole_count     = 7;   // Number of mounting holes
double_hole_count     = 6;   // Number of mounting holes

hole_diameter  = 1.5;  // Diameter of mounting holes
hub_height     = 3.8;  // Total height of the center hub

// Use the constants from your MG90S definition
S_Shaft_D      = 4.8;  // Shaft diameter
S_Shaft_H      = 5.0;  // Shaft height

module servo_arm(length=horn_length, h_plate=horn_height, num_holes=hole_count, d_hole=hole_diameter) {
    $fn = 60;
    
    // Calculate spacing based on length and number of holes
    // Starting 4mm from center to avoid the hub
    hole_start = 5; 
    hole_spacing = (length - hole_start - 2) / max(1, num_holes - 1);
    rotate([0,180,0])
    difference() {
        union() {
            // Main Arm Plate
            linear_extrude(height=h_plate)
                difference() {
                    hull() {
                        circle(d=7); // Base circle around hub
                        translate([length, 0]) circle(d=4); // Tip circle
                    }

                    // Parameterized holes
                    if (num_holes > 0) {
                        for (i=[0 : num_holes-1]) {
                            translate([hole_start + (i * hole_spacing), 0]) 
                                circle(d=d_hole);
                        }
                    }
                }
            
            // Central Hub
            cylinder(d=7, h=hub_height);
        }
        
        // Internal shaft bore (MG90S specific)
        translate([0, 0, -1]) 
            cylinder(d=S_Shaft_D - 0.1, h=hub_height + 2); // Snug fit for gears
            
        // Screw head countersink
        translate([0, 0, hub_height - 1.5]) 
            cylinder(d=S_Shaft_D + 1, h=2);
    }
}

module servo_arm_dual(length=horn_length, h_plate=horn_height, num_holes=double_hole_count, d_hole=hole_diameter) {
    $fn = 60;
    
    union() {servo_arm(length,h_plate,num_holes,d_hole);
             rotate ([0,0,180]) servo_arm(length,h_plate,num_holes,d_hole);
    }
}


// Example usage
//servo_arm_dual();