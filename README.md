# Video Super Resolution

This branch uses [this repo](https://github.com/kweisamx/TensorFlow-ESPCN) and applys it to a video.

### Dependencies

To run this code you need to have the [orginal repo](https://github.com/kweisamx/TensorFlow-ESPCN) installed and working first then add these files to it and replace the already exiting files.

### Training

The training will be done the same way as the [orginal repo](https://github.com/kweisamx/TensorFlow-ESPCN).

### Testing

For testing you will need a vide with `.mp4` extention named `test.mp4`, then type this in the command window:

'''python All.py'''

The video will be downscaled then upscaled again and the output video will be named `output.mp4`.

