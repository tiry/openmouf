// motor-gear MG90S

MG90S_LAT_WIDTH=22.4;

// Total  , Width, Total Height
MG90S_FULL_SIZE = [31.8, 12, 32.5];
MG90S_BLOCK_SIZE = [MG90S_LAT_WIDTH, MG90S_FULL_SIZE.y, 22.0];
MG90S_MOUNT_SIZE = [MG90S_FULL_SIZE.x, MG90S_BLOCK_SIZE.y, 2];
MG90S_MOUNT_OFFSET = 18; // from bottom to mount height
MG90S_MOUNT_HOLE_POS = 27.7;
MG90S_MOUNT_HOLE_D = 2.5;

MG90S_GEAR_D1 = MG90S_FULL_SIZE.y;
MG90S_GEAR_D2 = MG90S_GEAR_D1 / 2;
MG90S_GEAR_D3 = 4.8; // terminal gear diameter
MG90S_GEAR_H1 = 29;
MG90S_GEAR_H2 = MG90S_FULL_SIZE.z;

module mg90s_gear()
{
    $fn=60;
    dt = MG90S_GEAR_D1 / 2;
    translate([dt, dt, 0])
    union()
    {
        color("Grey", 1) cylinder(h = MG90S_GEAR_H1, d = MG90S_GEAR_D1);
        translate([dt, 0, 0])
        {
            color("Grey", 1) cylinder(h = MG90S_GEAR_H1, d = MG90S_GEAR_D2);
        }
        color("Gold", 1) cylinder(h = MG90S_GEAR_H2, d = MG90S_GEAR_D3);
    }
}

// mount holes
module mg90s_mount(hole_d)
{
    dy = MG90S_MOUNT_SIZE.y / 2;
    dx = MG90S_MOUNT_SIZE.x / 2;
    translate([dx, dy, 0])
    {
        dt = MG90S_MOUNT_HOLE_POS / 2;
        h = MG90S_MOUNT_SIZE.z * 2+0.2;
        translate([-dt, 0, 0])
            cylinder(h = h, d = hole_d, center=true, $fn=60);
        translate([+dt, 0, 0])
            cylinder(h = h, d = hole_d, center=true, $fn=60);
    }
}



module mg90s()
{
    dy = MG90S_BLOCK_SIZE.y / 2;
    dx = MG90S_BLOCK_SIZE.x / 2;
    translate([-dx, -dy, 0])
    union()
    {
        // main block
        color("DimGrey", 1) cube(MG90S_BLOCK_SIZE);
        mg90s_gear();
        x_diff = MG90S_BLOCK_SIZE.x - MG90S_MOUNT_SIZE.x;
        // mount plane
        translate([x_diff/2, 0, MG90S_MOUNT_OFFSET])
        color("DarkGrey") 
        difference()
        {
            cube(MG90S_MOUNT_SIZE);
            mg90s_mount(MG90S_MOUNT_HOLE_D);
        }
    }
}

//mg90s();
