# CONSTANTS
LIGHTS = [
    "light.office_lights",
    "light.family_room_lights",
    "light.breakfast_area_lights",
    "light.bedroom_lamp",
    "light.dining_area_lights",
    "light.color_1",
    "light.closet_light",
    "light.entryway_light"]

WARM_GLOW_EVENING = datetime.time(21, 30, 00)
WARM_GLOW_MORNING = datetime.time(5, 00, 00)
WAKEUP_TIME = datetime.time(6, 00, 00)
ELEVATION = -3

# Manual adjustments for the Winter to extend daylight indoors
DAYLIGHT_START_OVERRIDE= datetime.datetime.strptime(hass.states.get("input_datetime.daylight_start_override").state,"%H:%M:%S").time()
DAYLIGHT_END_OVERRIDE = datetime.datetime.strptime(hass.states.get("input_datetime.daylight_end_override").state,"%H:%M:%S").time()

# Get the time and sun attributes
now = datetime.datetime.now().time()
sun_elevation = hass.states.get("sun.sun").attributes['elevation']
sun_is_rising = hass.states.get("sun.sun").attributes['rising']

# Get the trigger information
light = data.get('light')

# If the script wasn't triggered manually and the trigger is a single light,
# then adjust just that light. Othwerise, adjust all of them.
if ((light is not None) and (light[:5] == 'light')):
    lights_to_adjust = [light]
# Ignore when the sun's elevation triggers this script at night. It seems like this triggers
# happens periodically at all hours of the day
elif (str(light) == "sun.sun" and WARM_GLOW_EVENING < now):
    lights_to_adjust = []
else:
    lights_to_adjust = LIGHTS

# Logging for debuggings triggers
logger.warning('Triggered by ' + str(light) + ' at ' + str(now))

# Calculate the desired temperature and brightness based on the time of day, sun elevation, and overrides
if (sun_elevation > ELEVATION or (DAYLIGHT_START_OVERRIDE < now < DAYLIGHT_END_OVERRIDE)):
    temp = 4000
    brightness_pct = 100
elif(WAKEUP_TIME < now and sun_is_rising):
    temp = 4000
    brightness_pct = 50
elif(now < WARM_GLOW_MORNING or WARM_GLOW_EVENING < now):
    temp = 2200
    brightness_pct = 50
else:
    temp = 2700
    brightness_pct = 75

# Loop through all the lights to adjust
for light in lights_to_adjust:
    # Adjust a light if it's on or always adjust the light if there's only one light to adjust.
    if (hass.states.is_state(light, "on") or len(lights_to_adjust) == 1):
        # if it was provided to the script, use the override
        brightness_pct = data.get('brightness_pct', brightness_pct)

        # custom logic for color lamp
        if (light == "light.color_1" and (now < WARM_GLOW_MORNING or WARM_GLOW_EVENING < now)):
            hass.services.call("light", "turn_on", {"entity_id": light, "brightness_pct": 5 }, False)
            time.sleep(1)
            hass.services.call("light", "turn_on", {"entity_id": light, "rgb_color": [255, 0, 0] }, False)
        # Dim the dining area lights if the TV is on and it's after 5PM
        elif (light == "light.dining_area_lights" and hass.states.get("media_player.lg_tv") == 'on' and datetime.time(17, 0, 0) < now):
            hass.services.call("light", "turn_on", {"entity_id": light, "brightness_pct": 10 }, False)
            time.sleep(1)
            hass.services.call("light", "turn_on", {"entity_id": light,  "kelvin": temp }, False)
        else:
            hass.services.call("light", "turn_on", {"entity_id": light, "brightness_pct": brightness_pct }, False)
            time.sleep(1)
            hass.services.call("light", "turn_on", {"entity_id": light,  "kelvin": temp }, False)
