---
audio: false
generated: true
lang: en
layout: post
title: Complete Weather Conditions in iOS Shortcuts
translated: false
type: note
---

Here's a comprehensive breakdown of all weather condition value ranges available in iOS Shortcuts:

## UV Index
- **Range**: 0-11+
- **Scale**:
  - 0-2: Low
  - 3-5: Moderate
  - 6-7: High
  - 8-10: Very high
  - 11+: Extreme

## Temperature
- **Range**: Varies by location
- **Units**: Celsius (°C) or Fahrenheit (°F)
- **Typical range**: -50°C to 50°C (-58°F to 122°F)

## Feels Like Temperature
- **Range**: Similar to actual temperature
- **Units**: Celsius (°C) or Fahrenheit (°F)
- **Factors**: Combines temperature, humidity, wind chill

## Humidity
- **Range**: 0-100%

## Visibility
- **Range**: 0-10+ miles or 0-16+ kilometers

## Wind Speed
- **Range**: 0-100+ mph or 0-160+ kph
- **Units**: mph, kph, m/s, or knots

## Wind Direction
- **Range**: 0-359 degrees
- **Cardinal directions**: N (0°), E (90°), S (180°), W (270°)

## Air Quality Index (AQI)
- **Range**: 0-500+
- **Scale**: Good (0-50) to Hazardous (301+)

## Precipitation Chance
- **Range**: 0-100%
- **Interpretation**: Probability of precipitation in the forecast period

## Precipitation Amount
- **Range**: 0 to 100+ mm or inches
- **Units**: mm or inches
- **Time period**: Usually measured per hour or per day

## Precipitation Intensity
- **Range**:
  - None: 0 mm/h
  - Light: 0.1-2.5 mm/h
  - Moderate: 2.5-10 mm/h
  - Heavy: 10-50 mm/h
  - Violent: 50+ mm/h

## Pressure
- **Range**: Typically 950-1050 hPa/mb
- **Units**: hPa, mb, or inHg
- **Standard pressure**: 1013.25 hPa at sea level

## Dew Point
- **Range**: Similar to temperature range
- **Units**: Celsius (°C) or Fahrenheit (°F)
- **Comfort levels**:
  - <55°F (<13°C): Dry and comfortable
  - 55-65°F (13-18°C): Comfortable
  - >65°F (>18°C): Increasingly humid and uncomfortable

## Cloud Cover
- **Range**: 0-100%

## Weather Condition
- **Values**: Text descriptions (Clear, Partly Cloudy, Rain, Snow, etc.)

## Sunrise/Sunset Times
- **Range**: Time values in local time zone

## Moon Phase
- **Range**: 0-1 (0 = New Moon, 0.5 = Full Moon, 1 = New Moon)
- **Text values**: New Moon, Waxing Crescent, First Quarter, etc.

## Pollen Count
- **Range**: Usually 0-12
- **Scale**: Low, Moderate, High, Very High

## Heat Index
- **Range**: Temperature range, but only calculated when temp is above 80°F (27°C)
- **Units**: Same as temperature

## Snowfall Amount
- **Range**: 0 to 100+ cm or inches
- **Units**: cm or inches
- **Time period**: Usually per hour or per day

These weather condition values can be used in conditional statements within Shortcuts to create sophisticated weather-based automations tailored to specific conditions.
