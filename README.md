# Custom Supports Reborn
A Cura plugin which lets you add several custom types of support instead so you can hold your print up *just* the way you like it.  

Based on [Custom Support Cylinder](https://github.com/5axes/CustomSupportCylinder) by [5axes](https://github.com/5axes) and updated so that I can keep this awesome plugin available to everyone.  
Originaly based on the Support Eraser plugin built into Cura and develoed by UltiMaker.

## Features

- Able to create cylindrical, squared / custom by 2 points / tube / abutment support style / Freeform Support
- Set support size
- Conical support is possible by defining an angle
- Can limit the size of the bottom of the support in case of tapered support

## Version History
### v1.1.0
- **Supports can now taper inwards as well as outwards.**
- Tube supports now have a consistent wall width as they taper.
- New icons for abutment and model support types.
- Model selection combo box now remembers what you had selected.
### v1.0.1
- Made control panel input validation less strict instead of getting inn the way.
- Fixed control panel so it works in Cura versions < 5.7.
### v1.0.0
- **Based on version 2.8.0 of Custom Support Cylinder by [5axes](https://github.com/5axes).**
- *Removed support for Qt 5 and Cura versions below 5.0 to reduce maintenance workload.*
- Tweaked tool icon so that it's obvious it doesn't just do cylinders. Now it looks like it does rockets. It doesn't. *Yet*.
- Renamed "Freeform" support to "Model" and "Custom" to "Line" and  swapped their order in the control panel.
- Added input validation to the text fields in the control panel to prevent unwanted behaviour from conflicting settings.
- Renamed everything to suit new branding (and internally so it doesn't break 5axes' versionif you also have that installed).
- Tweaked how the translation system works. That broke the existing translations. If you want to help out by translating it, get in touch!
- Cleaned up a lot of the internal code, made it easier to read, pruned some dead code. Usual spring cleaning.

## Pre-Emptively Answered Questions
- **Why do some settings change themselves when I change other settings?**  
This is to prevent invalid combinations of settings. Testing shows people often don't notice if I just give a subtle hint (like the background of a text box changing colour).

## Known Issues
- The combo box for selecting a particular model of support may show blank in older versions of Cura. Don't worry, it's still selecting and saving your choice.