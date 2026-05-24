A few months ago I got a **Beelink GTR9 Pro AMD Ryzen™ AI Max+ 395**.
Besides the ability to have much more muscle to do powerful things, my main objective was to use it as a local lab to experiment with several technologies, especially in the field of AI. 
I am quite happy with the product. 

The mini PC came with Windows 11 pre-installed, but I never use it. My first action was to erase the whole disk and install a Fedora distro to try some ComfyUI workflows. 
I wasn't successful, so I tried to do the same thing with an Ubuntu distro. In this case, I thought I was really close to getting the functional workflow I wanted to work with, but again I couldn't make it work.
So, I reinstalled Windows 11 to verify that the hardware was good enough to do what I was looking for. Once I found something I was pleased with, I decided to come back to Linux, this time trying an openSUSE distro. Finally, I nailed it, and since then, the PC runs with an openSUSE distro, so all my text is based on this openSUSE Tumbleweed distro.

By the way, I found an architectural flaw in the PC regarding its CMOS battery. I wasn't lucky enough, and the BIOS doesn't save the changes when it is disconnected from the power supply. The obvious way to solve the problem was to change the CMOS battery. Unfortunately, there was no easy way to remove it. You have to break the CMOS holder and then try to glue it again with a new battery, or you need to change the whole piece, which is really hard to find. I tried the first option, but it was a bad idea. Later, they sent me a spare part, but it didn't fit within the device. 

The great attraction for me was the field of diffusion models, and I've been trying several workflows on ComfyUI, but lately I've been quite busy trying several local LLM models. 
The aim of this project is to put together all my different tests with AI running on this mini PC, and have a reference guide to come back to a working state if I break something in the process.   

Here are the links to the articles:
- [openSUSE Setup and ComfyUI workflows](https://github.com/Comfy-Org/ComfyUI/discussions/11500)
- [OpenClaw Installation Guide for Linux](https://github.com/donlaiq/minipc/discussions/1)
- [OpenClaw Use Cases](https://github.com/donlaiq/minipc/discussions/2)
- [Huge, monster guy over a tiny, little lady](https://github.com/donlaiq/minipc/discussions/3)
