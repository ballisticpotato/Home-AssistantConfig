logger.warning(datetime.datetime.strptime(hass.states.get("input_datetime.daylight_start_override").state,"%H:%M:%S").time())
