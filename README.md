A few months ago I got a **Beelink GTR9 Pro AMD Ryzen™ AI Max+ 395**.
Besides the ability to have much more muscle to do powerful things, my main objective was to use it as a local lab to experiment with several technologies, especially in the field of AI. 
I am quite happy with the product. They sell it as supporting the local deployment of 70B-parameter AI models. In my local setup, tweaking some hyperparameters in llama.cpp, I was able to run Qwen 3.5 397B-A17B, which is quite impressive. Of course, in these cases, the inference is really slow and sometimes the device runs out of memory and the PC restarts, throwing away several hours of processing with no results at all. I have faith that in the near future, there will be several improvements to run more powerful local models in a more stable fashion.

The mini PC came with Windows 11 pre-installed, but I never use it. My first action was to erase the whole disk and install a Fedora distro to try some ComfyUI workflows. 
I wasn't successful, so I tried to do the same thing with an Ubuntu distro. In this case, I thought I was really close to getting the functional workflow I wanted to work with, but again I couldn't make it work.
So, I reinstalled Windows 11 to verify that the hardware was good enough to do what I was looking for. Once I found something I was pleased with, I decided to come back to Linux, this time trying an openSUSE distro. Finally, I nailed it, and since then, the PC runs with an openSUSE distro, so all my text is based on this openSUSE Tumbleweed distro.

By the way, I found an architectural flaw in the PC regarding its CMOS battery. I wasn't lucky enough, and the BIOS doesn't save the changes when it is disconnected from the power supply. The obvious way to solve the problem was to change the CMOS battery. Unfortunately, there was no easy way to remove it. You have to break the CMOS holder and then try to glue it again with a new battery, or you need to change the whole piece, which is really hard to find. I tried the first option, but it was a bad idea. Later, they sent me a spare part, but it didn't fit within the device. So, currently, every time I turn the PC on, I need to go to the BIOS and change the option

```Advanced -> AMD CBS -> CPU Common Options Global C-state Control```

to **_Disable_**; otherwise, the OS gets frozen in every single session. You are doing regular, lightweight stuff and suddenly you can't move the mouse, the keyboard is unresponsive, and there's no movement on the screen. After a while, I figured out that by pressing some keys on the keyboard, it came back to life as if nothing had happened. Which key combination did I use?! Every key! I was playing like a novice pianist, making random noise. Once in a while, it's kind of annoying, but if it happens in every new session... 😤... So, disabling this option in the BIOS was a blessing, and it rarely happens now.

The great attraction for me was the field of diffusion models, and I've been trying several workflows on ComfyUI, but lately I've been quite busy trying several local LLM models. My main interest is in their coding skills and, to be honest, I haven't written anything about it yet, because even though it's funny to see their train of thought and, depending on the size of the model, the speed at which they write solutions, unfortunately they are wrong most of the time. Hopefully, I'll write some of my thoughts about it in the future.
The aim of this project is to put together all my different tests with AI running on this mini PC, and have a reference guide to come back to a working state if I break something in the process.   

Besides the links to the articles I'm writing, this site also seems to be a good place to put some code... GitHub <-> source code... you know... For the time being, I'm just adding this tiny script that makes my life much, much easier when I need to write a prompt for an LLM model. Perhaps I'll add something else in the future.

When I write something, the _Enter_ key is of priceless value to let me read the text with more clarity. Unfortunately, within an LLM interface, it sends a command before I can finish my request. So, the approach I'm using right now is to write the prompt in a regular text editor, save the file as _prompt.txt_, and run the command **_python3 slash.py_**. It will generate a file called _output.txt_, which basically adds a slash and a white space ("/ ").
The LLM model interprets that the prompt continues on the next line after the slash ("/"). 
The whitespace was added because some models were merging tokens from two lines. For example:

10 11
12 13

could be interpreted as the numbers 10, 11, 12, and 13


Here are the links to the articles:
- [openSUSE Setup and ComfyUI workflows](https://github.com/Comfy-Org/ComfyUI/discussions/11500)
- [OpenClaw Installation Guide for Linux]()
