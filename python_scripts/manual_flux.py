LIGHTS = [
    "light.bathroom_lights",
    "light.bedroom_lamp",
    "light.dining_area_lights",
    "light.color_1"]

light = data.get('light')

# Let's us handle the case when the script is triggered manually and if the trigger
# is something like the sun, then we want to adjust all lights that are on.
if ((light is not None) and (light[:5] == 'light')):
    LIGHTS = [light]

WARM_GLOW_EVENING = datetime.time(21, 30, 00)
WARM_GLOW_MORNING = datetime.time(5, 00, 00)

# Manual adjustments for the Winter to extend daylight indoors
DAYLIGHT_START_OVERRIDE= datetime.datetime.strptime(hass.states.get("input_datetime.daylight_start_override").state,"%H:%M:%S").time()
DAYLIGHT_END_OVERRIDE = datetime.datetime.strptime(hass.states.get("input_datetime.daylight_end_override").state,"%H:%M:%S").time()

WAKEUP_TIME = datetime.time(6, 00, 00)
ELEVATION = -3

now = datetime.datetime.now().time()
sun_elevation = hass.states.get("sun.sun").attributes['elevation']
sun_is_rising = hass.states.get("sun.sun").attributes['rising']

# logger.warning('Triggered by ' + str(light) + ' at ' + str(now))

if (sun_elevation > ELEVATION or (DAYLIGHT_START_OVERRIDE < now < DAYLIGHT_END_OVERRIDE)):
    temp = 4000
    brightness_pct = 100
elif(WAKEUP_TIME < now and sun_is_rising):
    temp = 4000
    brightness_pct = 50
elif(now < WARM_GLOW_MORNING or WARM_GLOW_EVENING < now):
    temp = 2200
    brightness_pct = 25
else:
    temp = 2700
    brightness_pct = 50

for light in LIGHTS:
    if (hass.states.is_state(light, "on") or len(LIGHTS) == 1):
        # if it was provided to the script, use the override
        brightness_pct = data.get('brightness_pct', brightness_pct)
        
        # custom logic for color lamp
        if (light == "light.color_1" and (now < WARM_GLOW_MORNING or WARM_GLOW_EVENING < now)):
            service_data = {
                "entity_id": light,
                "rgb_color": [255, 0, 0],
                "brightness_pct": 5
            }
            hass.services.call("light", "turn_on", {"entity_id": light, "brightness_pct": 5 }, False)
            time.sleep(1)
            hass.services.call("light", "turn_on", {"entity_id": light, "rgb_color": [255, 0, 0] }, False)
        else:
            service_data = {
                "entity_id": light,
                "kelvin": temp,
                "brightness_pct": brightness_pct
            }
            hass.services.call("light", "turn_on", {"entity_id": light, "brightness_pct": brightness_pct }, False)
            time.sleep(1)
            hass.services.call("light", "turn_on", {"entity_id": light,  "kelvin": temp }, False)
            time.sleep(1)
