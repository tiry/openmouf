// MG90S mount
include <motor-gears.scad>

MG_MOUNT_W = 4;
MG_MOUNT_D = 0.2;
MG_MOUNT_HOLE_D = MG90S_MOUNT_HOLE_D - 1;
MG_MOUNT_SIZE=[
    MG90S_BLOCK_SIZE.x + 2 * (MG_MOUNT_W + MG_MOUNT_D)
    , MG90S_BLOCK_SIZE.y
    , MG90S_MOUNT_OFFSET + MG_MOUNT_W
];


module gear_mount()
{
    $fn=60;
    dx = MG_MOUNT_SIZE.x / 2;
    dy = MG_MOUNT_SIZE.y / 2;
    dz = MG_MOUNT_W;
    
    difference()
    {
        union()
        {
            difference()
            {
                cube([MG_MOUNT_SIZE.x, MG_MOUNT_SIZE.y, MG_MOUNT_W], center=true);
                //translate([(MG90S_BLOCK_SIZE.x - MG90S_GEAR_D1) / 2, 0, 0])
                //cylinder(h = MG_MOUNT_W * 2, d = MG90S_MOUNT_HOLE_D, center = true);
            }
            
            translate([0, 0, (MG_MOUNT_SIZE.z - MG_MOUNT_W) / 2])
            {
                translate([-(dx - MG_MOUNT_W / 2), 0, 0])
                {
                    cube([MG_MOUNT_W, MG_MOUNT_SIZE.y, MG_MOUNT_SIZE.z], center=true);
                }
                
                translate([+(dx - MG_MOUNT_W / 2), 0, 0])
                {
                    cube([MG_MOUNT_W, MG_MOUNT_SIZE.y, MG_MOUNT_SIZE.z], center=true);
                }
            }
        }
        translate([0, 0, (MG_MOUNT_SIZE.z - MG_MOUNT_W) / 2])
        {
            translate([-(dx - MG_MOUNT_W / 2), 0, 10])
            {
                cylinder(h = MG_MOUNT_SIZE.z/2 , d = MG_MOUNT_HOLE_D, center = true);
            }
            
            translate([+(dx - MG_MOUNT_W / 2), 0, 10])
            {
                cylinder(h = MG_MOUNT_SIZE.z/2 , d = MG_MOUNT_HOLE_D, center = true);
            }
        }
        
        translate([-(dx - MG_MOUNT_W / 2), 0, MG_MOUNT_W / 2])
        {
             cube([MG_MOUNT_W * 2, 4, MG_MOUNT_W * 2], center=true);
        }
        translate([+(dx - MG_MOUNT_W / 2), 0, MG_MOUNT_W / 2])
        {
             cube([MG_MOUNT_W * 2, 4, MG_MOUNT_W * 2], center=true);
        }
    }
}

//gear_mount();

