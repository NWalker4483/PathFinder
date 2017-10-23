# Pathfinder
<table>
<tr><td>
<img src="View_Screenshot_10_12_30.png" width="300" height="300" align="center"> 
<img src="Area_Screenshot_10_12_30.png" width="300" height="300" align="left"> 
<img src="Mask_Screenshot_10_12_30.png" width="300" height="300" align="right"> 

</td>
</tr>
</table>
## Introduction
This project is to create a vehicle capable of navigate sidewalks and other similiar pathway autonomously.
## Controls
|Pose|Action|
|------|------|
|Finger Spread|Takeoff|
|Fist|Land|
|Wave Out|Roll Right|
|Wave In|Roll Left|
|Double Tap |Barrel Roll|
## Prereqs
Before attempting to run this project make sure that [Myo Connect Software](https://www.myo.com/start) is installed and setup.

## Dependencies 
This project utilizes:
* macOS Sierra v10.12.6
* Raspberry Pi 2 
* Homebrew v1.3.2
* node.js v6.11.3
* myo v3.0.0
* ar-drone v0.0.3
``` 
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
$ brew update
$ brew install node
$ npm install myo keypress ar-drone
```
## Start-up
Once your drone is on connect to the ardrone wireless network in your wifi menu. Then, if all of the neccesary modules are installed and a Myo is connected launch the program by running.
```
$ node Wright.js 
``` 
>The Console should then display "begin" and "I'm Alive". Once these are displayed double tap your fingers in order to unlock the Myo and issue commands. 
### Future Developments
* Video Streaming from the Drone
* Using the GyroScope for motion controls
* Control the autonomous vehicle using the Intel Joule 570X

### Commonly Experienced Errors
* TBA

### Additional Documentation
- [Myo.js Docs](https://github.com/thalmiclabs/myo.js)
- [Ar-Drone Docs](https://github.com/felixge/node-ar-drone)