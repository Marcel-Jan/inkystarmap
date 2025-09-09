# inkystarmap
Making a map of the night sky on an Inky Impressions e-ink display

![Alt text](inkystarmap2025.jpg?raw=true "Photo of a star map on an Inky Impressions 13.3.")

## What you need
- A Raspberry Pi (tested with Zero 2W)
- An Inky Impression e-ink display from Pimoroni.
- A micro SD card that's not too slow (I have used a SanDisk 64GB High Endurance MircoSD XC I3 V30.)

## Hardware
Attach the Raspberry Pi to the GPIO port
![Alt text](inky133_back.jpg?raw=true "Photo of backside of the Inky Impressions 13.3 with Raspberry Pi Zoro 2W attached.")

## Usage
    python3 gradientmap_inky.py --lat <your_latitude> --lon <your_longitude> --direction <direction to look at in degrees>

Example:
To have a map of the southern night sky from Gouda, the Netherlands, you can run this:  
    python3 gradientmap_inky.py --lat -52.0141616 --lon -4.7158104 --direction 180

