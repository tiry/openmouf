
$fn=16;

module rounded_cube(size=[1, 1, 1], r=0.1, center=false) {
    // Determine the offset based on the center parameter
    // If center is false, we shift everything by [r, r, r] so the 
    // outer edge starts at [0, 0, 0].
    shift = center ? [0, 0, 0] : [r, r, r];
    
    // We must subtract the diameter (2*r) from the requested size
    // to ensure the spheres' outer edges hit the requested dimensions.
    inner_size = [
        size[0] - 2*r, 
        size[1] - 2*r, 
        size[2] - 2*r
    ];

    // If center is true, we need to center the 'inner' volume 
    // relative to the origin.
    inner_shift = center ? [-inner_size[0]/2, -inner_size[1]/2, -inner_size[2]/2] : [0, 0, 0];

    translate(shift + inner_shift)
    hull() {
        for (x = [0, inner_size[0]])
        for (y = [0, inner_size[1]])
        for (z = [0, inner_size[2]]) {
            translate([x, y, z])
            sphere(r=r);
        }
    }
}

//rounded_cube([10,5,2], r=0.5, center=true);
//translate([0,0,10]) cube([10,5,2], center=true);
