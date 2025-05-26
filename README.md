### donut.c but in python!
![donut.gif](./readme_media/donut.gif)
- This project is inspired by the famous <a style="font-family:cursive; color:lime" href="https://www.a1k0n.net/2011/07/20/donut-math.html">donut.c</a> program and intends to produce similar, but different renders in python.
- Instead of rendering ASCII characters in terminal, it renders points in open-cv window which enables anyone to save the renders in the form of image/gif/video.
- You can simply reduce the `theta_spacing` and `phi_spacing` in `donut.py` to increase the number of points and thereby making the donut more "solid". I find the default render much more pleasing even though we can see through it sometimes 😅

### Wait there's more!
![cube.gif](./readme_media/cube.gif)
- Along with rendering a simple donut, there is also a file to render 9x9 cube. Don't run `cube_hollow_fast.py` to render cube, it was a failed vectorized attempt to make the slow for-loop implementation fast. Instead, run `cython_implementation/cube_hollow_fast_cython_run.py`, which is cythonized code and runs 4-5 times faster than for-loop implementation.
- With the default arguments in `cython_implementation/cube_hollow_fast_cython_run.py`, the program renders just over a million points! you can tweek the arguments to make the render faster by rendering less points while maintaining close to a cube structure.
- python `3.10.11` is used in the project