from datetime import datetime
from pytz import timezone
from starplot import MapPlot, Projection, Star, Moon
from starplot.styles import PlotStyle, extensions
from inky.auto import auto
from resize_to_inky import resize_to_inky


# Inky display
INKY_DISPLAY = auto()
INKY_DISPLAY.set_border(INKY_DISPLAY.BLACK)
DISPLAY_WIDTH = INKY_DISPLAY.WIDTH
DISPLAY_HEIGHT = INKY_DISPLAY.HEIGHT

tz = timezone("Europe/Amsterdam")
# dt = datetime(2024, 10, 14, 21, 0, tzinfo=tz)
# Tonight at 22:00 Europe/Amsterdam time
dt = datetime.now(tz).replace(hour=22, minute=0, second=0, microsecond=0)

# Location: Gouda, The Netherlands
LAT = 52.0141616
LON = 4.7158104

m = Moon.get(dt, LAT, LON)
p = MapPlot(
    projection=Projection.ZENITH,
    lat=LAT,
    lon=LON,
    dt=dt,
    style=PlotStyle().extend(
        extensions.BLUE_DARK,
    ),
    resolution=3600,
)
p.constellations()
p.stars(mag=4.6, where_labels=[Star.magnitude < 2.1])
p.horizon()
p.ecliptic()
p.planets()
p.moon(
    true_size=True,
    show_phase=True,
)
p.export("star_chart_basic.png", transparent=True, padding=0.1)

# Resize image to fit Inky display
resized_image_name = resize_to_inky("star_chart_basic.png", 800, 480)

# Write resized image to png file
resized_image_name.save("star_chart_basic_resized.png")

INKY_DISPLAY.set_image(resized_image_name)
INKY_DISPLAY.show()
