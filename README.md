# Custom Supports Reborn
A Cura plugin which lets you add several custom types of support instead of just a boring cube.  

Based on [Custom Support Cylinder](https://github.com/5axes/CustomSupportCylinder) by 5@xes and reborn so that I can keep this awesome plugin available to everyone.  
Originaly based on the Support Eraser plugin built into Cura and develoed by UltiMaker.

## Features

- Able to create cylindrical, squared / custom by 2 points / tube / abutment support style / Freeform Support
- Set support size
- Conical support is possible by defining an angle
- Can limit the size of the bottom of the support in case of tapered support

**New 2.4.0**

- Possibility to define a max size for the base of the support

**New 2.5.X**

- Possibility to define freeform support via STL File


**New 2.6.X**

Updated for Cura 5.0

The initial version was tested on Cura 4.5 but last release tested from 4.5 to 5.0

![View plugin](./images/plugin.jpg)

## Installation

### Manual Installation

Download the latest release from this [repository](https://github.com/5axes/CustomSupportCylinder/releases)

Drop the curapackage according to your Cura release in the 3d viewport in Cura as if you were opening a 3d model. You will then be prompted to restart Cura.

![Manual Install](./images/Restart.JPG)

### Automatic installation for Cura 4.X and Cura 5.X

First, make sure your Cura version is 4.5 or newer. This plugin is now avalaible in the Cura marketplace. So you can install it automaticaly from this place:

![Automatic Install](./images/MarketPlace.png)

[Cylindric Custom Support on Ultimaker Market place](https://marketplace.ultimaker.com/app/cura/plugins/5axes/CustomSupportCylinder)


## How to use

* Load a model in Cura and select it

* Click on the "Custom Supports Cylinder" button on the left toolbar
* With the 6 buttons in the plugin windows, it's possible to switch the geometry between a cylinder, a tube, a cubic, an abutment, a freeform or a custom support.
* Change the value for the support *Size* in numeric input field in the tool panel if necessary
* Change the value for the support *Angle* in numeric input field in the tool panel if necessary **(Version 1.0.03)**
* You can limit the size of the tappered support by fixing a Max Size Value if necessary **(Version 2.4.0)**
* Change the value for the support *Interior size* in numeric input field in the tool panel if necessary **(Version 2.2.0 for Tube support)**

![Numeric input field in the tool panel](./images/option_n.jpg)

Select the type of support to create with the buttons in the support plugin interface :

![Support type selection](./images/button.jpg)

- Click anywhere on the model to place support cylinder there
* The length of the support is automaticaly set from the pick point to the construction plate.

- **Clicking existing support deletes it**

- **Clicking existing support + Ctrl** switch automaticaly to the Translate Tool to modify the position of the support.

- **Clicking existing support + Alt** this shorcut allow to add a support on a existing support.

- Before to slice your model, uncheck the "Generate Support" checkbox in the right panel **(if you want to use ONLY custom supports)**

>Note: it's easier to add/remove supports when you are in the "Prepare" stage.


## Modifications

- Version 1.03 : Possibility to define conical support

![Conical Support](./images/conical_support.jpg)
	
- Version 2.0.0 : Possibility to define custom support

![Custom Support](./images/custom_support.jpg)

To create custom support you need to clic 2 points on the model.

- Version 2.1.0 : Possibility to define Abutment support

![Abutment Support](./images/Abutment.jpg)

- Version 2.2.0 : Possibility to define a Tube as support

![Tube Support](./images/Tube.jpg)

- Version 2.3.0 : For Abutment support possibility to create directly the Support on the Y direction and possibility to unify the supports heights

![Abutment Support](./images/AbutmentSupport.jpg)

- Version 2.4.0 : Add Max Size Option in oder to limite the base size.

![Conical Support with max base size](./images/cone.jpg)

- Version 2.4.1 : By default Support Mesh are not define as Drop Down Support Mesh. This option will offer the possibility to define new shape for the mesh. But this modification must be validated by the users before going further in the development.

- Version 2.5.X : New option for Freeform Support : Can add a support with a form freely defined by an STL file ( Model must have the size 1x1x1 bo be modified according to the Size value and the height ) :

- Version 2.6.X : Update for Cura 5.0

- Version 2.7.0 : Add possibility to translate the plugin. Add French translation
- Version 2.7.1 add auto-orientation on freeform support.

- Version 2.8.0 Add Define As Model For Cylindrical Model.
- Version 2.8.1 Change Code for automatic orientation.