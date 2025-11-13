# inkystarmap
Making a map of the night sky on an Inky Impressions e-ink display

![Alt text](inkystarmap2025.jpg?raw=true "Photo of a star map on an Inky Impressions 13.3.")

## What you need
- A Raspberry Pi (tested with Zero 2WH)
- An Inky Impression e-ink display from Pimoroni.
- A micro SD card that's not too slow (I have used a SanDisk 64GB High Endurance MircoSD XC I3 V30.)
- A power cable

## Hardware
Attach the Raspberry Pi to the GPIO port
![Alt text](inky133_back.jpg?raw=true "Photo of backside of the Inky Impressions 13.3 with Raspberry Pi Zoro 2W attached.")

## Installation
### Preparing for install
1. Use Raspberry Pi Imager (available from here [https://www.raspberrypi.com/software/]) to install the OS on a micro SD card. (On a Windows/MacOS/Linux system)
2. Insert the Micro SD card in your Raspberry Pi.
3. Log in on your Raspberry Pi with SSH (can be with Putty or iTerm2).

### Installation, the easier way
4. Download inkystarmap_0.4.0.deb

       wget https://github.com/Marcel-Jan/inkystarmap/blob/main/inkystarmap_0.4.0.deb
6. Run the .deb file

        sudo dpkg -i inkystarmap_0.4.0.deb
7. Run inkystarmap (see Usage below)

       inkystarmap --lat 52.0141616 --lon 4.7158104 --direction 180


### Installation, the harder way
4. Enlarge the swap space of your Raspberry Pi (new version creates a 4G swapfile). (I found that installing the necessary Python packages for inkystarmap, specifically cartopy, will hang if you don't have enough swap space.)
5. In your $HOME, create a PythonProjects directory (or wherever you want to install inkystarmap).
6. Install uv (instructions here: [https://docs.astral.sh/uv/getting-started/installation/]).
7. Download this repository on your Raspberry Pi (I would do this in the PythonProjects directory).

        git clone https://github.com/Marcel-Jan/inkystarmap.git
   
9. Go in the new inkystarmap directory.
10. Run uv sync. This will create a virtual environment, install Python 3.13 there and install all necessary Python packages. (If it hangs during installation of the Python packages, check step 4.)

        uv sync
11. Activate the virtual environment.

        source .venv/bin/activate
12. Run inkystarmap (see Usage below)

       inkystarmap --lat 52.0141616 --lon 4.7158104 --direction 180

## Usage
    python3 inkystarmap.py --lat <your_latitude> --lon <your_longitude> --direction <direction to look at in degrees>

Example:
To have a map of the southern night sky from Gouda, the Netherlands, you can run this:  

    python3 inkystarmap.py --lat 52.0141616 --lon 4.7158104 --direction 180

If you don't enter the latitude and longitude, an attempt is made to get your location via IP.

## Scheduling
There now is an inkystarmap service and a timer that will run the Python code every hour (with default lat/lon and direction 180). Based on your location it will determine if the sun is up or down. If the sun is down, the starmap will be refreshed.
