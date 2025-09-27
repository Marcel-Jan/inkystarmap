import logging
from datetime import datetime
from pytz import timezone
import time
import argparse
from starplot import MapPlot, Star, Moon, Observer, HorizonPlot, _
from starplot.styles import PlotStyle, extensions
from inky.auto import auto
from resize_to_inky import resize_to_inky


# Inky display
INKY_DISPLAY = auto()
INKY_DISPLAY.set_border(INKY_DISPLAY.BLACK)
DISPLAY_WIDTH = INKY_DISPLAY.WIDTH
DISPLAY_HEIGHT = INKY_DISPLAY.HEIGHT


# Location: Gouda, The Netherlands
LAT = 52.0141616
LON = 4.7158104


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Send logging to file
file_handler = logging.FileHandler("inkystarmap.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


def main():
    # Get timezone from system.
    tz = timezone(time.tzname[0])
    logger.info(f"Timezone from system: {time.tzname[0]}")

    # Tonight at 22:00 at current timezone.
    dt = datetime.now(tz).replace(hour=22, minute=0, second=0, microsecond=0)
    logger.info(f"Time in timezone: {dt}")

    logger.info("Creating style")
    style = PlotStyle().extend(
        extensions.BLUE_GOLD,
        extensions.MAP,
        extensions.GRADIENT_PRE_DAWN,
    )

    # Argument parser for latitude, longitude and direction
    parser = argparse.ArgumentParser(description="Create a starplot")
    parser.add_argument("--lat", type=float, default=LAT, help="Latitude")
    parser.add_argument("--lon", type=float, default=LON, help="Longitude")
    parser.add_argument("--direction", type=int, default=180, help="Direction")
    args = parser.parse_args()

    logger.info(f"Location: lat={args.lat}, lon={args.lon}")

    logger.info("Creating observer")
    observer = Observer(
        lat=args.lat,
        lon=args.lon,
        dt=dt,
    )

    # Field of view
    min_azimuth = args.direction - 90
    max_azimuth = args.direction + 90
    if max_azimuth > 360:
        max_azimuth -= 360
    logger.info(f"Field of view: {min_azimuth}° to {max_azimuth}°")

    logger.info("Creating horizon plot")
    p = HorizonPlot(
        altitude=(0, 90),
        azimuth=(min_azimuth, max_azimuth),
        observer=observer,
        style=style,
        resolution=3200,
        scale=0.9,
    )

    logger.info("Adding celestial objects to horizon plot")
    p.constellations()

    logger.info("Adding stars to horizon plot")
    p.stars(
        where=[_.magnitude < 4.6],
        where_labels=[_.magnitude < 2.1],
        style__marker__symbol="star_4",
    )
    logger.info("Adding horizon to plot")
    p.horizon()

    logger.info("Adding ecliptic to plot")
    p.ecliptic()

    logger.info("Adding planets to plot")
    p.planets()

    # logger.info("Adding milky way to plot")
    # p.milky_way()

    logger.info("Adding moon to plot")
    p.moon(
        true_size=True,
        show_phase=True,
    )

    logger.info("Exporting plot")
    p.export("horizon_gradientmap.png", transparent=True, padding=0.1)

    # Resize image to fit Inky display
    logger.info("Resizing image to fit Inky display")
    resized_image_name = resize_to_inky("horizon_gradientmap.png", DISPLAY_WIDTH, DISPLAY_HEIGHT)

    # Write resized image to png file
    logger.info("Saving resized image")
    resized_image_name.save("horizon_gradientmap_resized.png")

    INKY_DISPLAY.set_image(resized_image_name)
    INKY_DISPLAY.show()


if __name__ == "__main__":
    main()
