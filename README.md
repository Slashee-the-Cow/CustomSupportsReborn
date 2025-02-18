# Custom Supports Reborn
A Cura plugin which lets you add several custom types of support instead of the default so you can hold your print up *just* the way you like it.  

Based on [Custom Support Cylinder](https://github.com/5axes/CustomSupportCylinder) by [5axes](https://github.com/5axes) and updated so that I can keep this awesome plugin available to everyone.  
Originaly based on the Support Eraser plugin built into Cura and develoed by UltiMaker.

## Features

- Able to create cylindrical, squared, line (between two points you choose), tube and abutment support style *plus* some models which may or may not be more effective. I'm not a structural engineer. But they add some pizazz!
- Outwards or inwards tapered support with a maximum/minimum size!
- Not something I can take credit for, but you can use the *Per Model Settings* tool to turn them into regular models.

## Version History
### v1.2.0
- Supercharged input validation!
  - Now gives you both "information" and "this is bad" levels of alerts.
  - Invalid settings now have a "Fix it!" button.
- Cleaned up the layout for the control panel while I was in there. Mostly noticeable by a significant lack of gaps between settings.
- Dusted more cobwebs and such.
### v1.1.0
- **Supports can now taper inwards as well as outwards!**
- Tube supports now have a consistent wall width as they taper. This has replaced the previous "inner size" setting.
- New icons for abutment and model support types.
- Model selection combo box now remembers what you had selected.
### v1.0.1
- Made control panel input validation less strict instead of getting in the way.
- Fixed control panel so it works in Cura versions < 5.7.
### v1.0.0
- **Based on version 2.8.0 of Custom Support Cylinder by [5axes](https://github.com/5axes).**
- *Removed support for Qt 5 and Cura versions below 5.0 to reduce maintenance workload.*
- Tweaked tool icon so that it's obvious it doesn't just do cylinders. Now it looks like it does rockets. It doesn't. *Yet*.
- Renamed "Freeform" support to "Model" and "Custom" to "Line" and  swapped their order in the control panel.
- Added input validation to the text fields in the control panel to prevent unwanted behaviour from conflicting settings.
- Renamed everything to suit new branding (and internally so it doesn't break 5axes' version if you also have that installed).
- Tweaked how the translation system works. That broke the existing translations. If you want to help out by translating it, get in touch!
- Cleaned up a lot of the internal code, made it easier to read, pruned some dead code. Usual spring cleaning.

## Known Issues
- Text fields may reset to the previous valid or a failsafe default value if any fields have invalid values when the tool is deselected.
  - This is due to how it handles input validation and UI events.
  - Intended to be fixed in a future release.
- The combo box for selecting a particular model may show blank in older versions of Cura. Don't worry, it's still selecting and saving your choice.
  - Workaround: An info icon appears which you can hover your mouse over to see the currently selecting model.