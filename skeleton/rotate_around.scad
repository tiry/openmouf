// --- Configuration ---
$fn = 32;
s1_len = 40;
s2_len = 30;
s3_len = 20;

// Joint angles (change these to move the arm)
angle1 = [0, 0, 45]; 
angle2 = [0, 0, -30];

// --- Utilities ---
module rotate_around(pivot, angles) {
    translate(pivot)
    rotate(angles)
    translate(-pivot)
    children();
}

module rounded_cube(size=[1, 1, 1], r=1, center=false) {
    shift = center ? [0, 0, 0] : [r, r, r];
    inner_size = [size[0]-2*r, size[1]-2*r, size[2]-2*r];
    inner_shift = center ? [-inner_size[0]/2, -inner_size[1]/2, -inner_size[2]/2] : [0, 0, 0];

    translate(shift + inner_shift)
    hull() {
        for (x = [0, inner_size[0]], y = [0, inner_size[1]], z = [0, inner_size[2]]) {
            translate([x, y, z]) sphere(r=r);
        }
    }
}

// --- The Assembly ---

// SEGMENT 1 (Static Base)
color("Gold") 
    rounded_cube(size=[s1_len, 5, 5], r=1);

// JOINT 1 & SEGMENT 2
// Pivot point is at the end of Segment 1
rotate_around(pivot=[s1_len - 2.5, 2.5, 2.5], angles=angle1) {
    
    // Segment 2
    color("FireBrick")
    translate([s1_len - 2.5, 0, 0])
    rounded_cube(size=[s2_len, 5, 5], r=1);
    
    // JOINT 2 & SEGMENT 3
    // Pivot point is at the end of Segment 2 
    // (Relative to the start of Segment 2)
    translate([s1_len - 2.5, 0, 0]) // Move to the start of Segment 2
    rotate_around(pivot=[s2_len - 2.5, 2.5, 2.5], angles=angle2) {
        
        // Segment 3
        color("RoyalBlue")
        translate([s2_len - 2.5, 0, 0])
        rounded_cube(size=[s3_len, 5, 5], r=1);
    }
}