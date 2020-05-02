## Constants
ON_LIGHT = "light.jerry_floor_2"
OFF_LIGHTS = [
    "light.jerry_floor_1",
    "light.jerry_floor_3",
    "light.jerry_floor_4",
    "light.jerry_floor_5"
]

# Turn off the manual_flux automation first
hass.services.call("automation", "turn_off", {"entity_id": "automation.manual_flux"}, False)

# If we're already in light night mode, then turn off the lights
if (hass.states.is_state(ON_LIGHT, "on") and hass.states.is_state(OFF_LIGHTS[0], "off")):
    hass.services.call("light", "turn_off", {"entity_id": "light.bedroom_lamp"}, False)
else:
    hass.services.call("light", "turn_off", {"entity_id": OFF_LIGHTS}, False)
    service_data = {
        "entity_id": ON_LIGHT,
        "kelvin": 2200,
        "brightness_pct": 5
    }
    hass.services.call("light", "turn_on", service_data, False)
    time.sleep(1)

# Turn back on the manual_flux automation first
hass.services.call("automation", "turn_on", {"entity_id": "automation.manual_flux"}, False)