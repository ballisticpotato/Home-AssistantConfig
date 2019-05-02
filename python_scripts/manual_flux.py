LIGHTS = [
        "light.jerry_s_floor_lamp",
        "light.jerry_s_bathroom_lights",
        "light.jerry_bedside"]

WARM_GLOW_EVENING = datetime.time(22,00,00)
WARM_GLOW_MORNING = datetime.time(5,00,00)
ELEVATION = 6

now = datetime.datetime.now().time()

sun_elevation = hass.states.get("sun.sun").attributes['elevation']

if (sun_elevation > ELEVATION):
    temp = 4000
elif(now < WARM_GLOW_MORNING or WARM_GLOW_EVENING < now):
    temp = 2200
else:
    temp = 2700

for light in LIGHTS:
    if (hass.states.is_state(light, "on")):
        service_data = {
                "entity_id": light,
                "kelvin": temp
                }
        hass.services.call("light", "turn_on", service_data, False)

