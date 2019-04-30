# Using Object detection to train 2d PC games.

This code attempts to use object detection to train a model that will play simple 2d PC games.

For initial cases I use a Nintendo emulator to produce games to a Desktop.

Using the given system's graphical windows handler, we grab the correct window and make sure we only record the size of that window.

Alongside the window scraping, we also collect keystrokes.  Initially, we are only interested in a basic Nintendo controller, which has 4 directional buttons(up, down, left, right), and two action buttons (B, A).   Assuming we are all gamers, who also don't have a dPad hooked up to the PC, we will use the traditional WASD for direction, and J,K for B and A respectively.

Initially, the model will be multi-label classification, with each input being a screenshot, and each output is one of many possible key presses.

The three steps are "collect.py", "train.py", and "inference.py", with each step gathering input data, training the model and playing back the game respectively.


Acknowledgments
I want to give a special shoutout to Sentdex and his pygta5 tutorial/videos (https://github.com/Sentdex/pygta5, https://www.youtube.com/user/sentdex).
They began the groundwork for this adventure. I would've forked directly from the pygta5 repo, but too much was changing from the original code that I felt the need to create a separate code space moving forward.  If you have time please check out the links above as they are a fun intro to machine/deep learning and python.

For the Tensorflow and other backends, I'm using the PowerAI toolkit provided by IBM.  These are a great set of tools, all bundled up in nice Anaconda packages, already
built and tuned for both x86 and POWER architectures.  PowerAI includes Tensorflow, Pytorch, Caffe, and many other frameworks, all ready to go from a single conda channel.

PowerAI Conda Channel: https://public.dhe.ibm.com/ibmdl/export/pub/software/server/ibm-ai/conda/
PowerAI Dockerhub Page: https://hub.docker.com/r/ibmcom/powerai/
