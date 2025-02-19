# uv_visibilities
An useful routine to visualise visibilities.
This code allows to extract the uv pointings of an ms file and see how its visibilities look like channel by channel.

The visibilities are the raw data (regridded if needed) produced by a radio-interferometer, like ALMA for example. 

If you are used to radio-astronomy data, you will know that the lovely images (**IMG**) that you see - which are produced through an algorithm called _tclean_ - are related to the visibilities (**VIS**) through a Fourier Transform. Specifically, **VIS** -- FFT-1 --> **IMG**. Therefore, what you will see using this tool is equivalent to what you would see after computing a 2D-FFT of a channel map. Of course, you should plot the resulting FFT on the original uv-plane produced by your interferometer, but that's a detail.

If you didn't know about what written above, now you know.

**# uv_visibilities** works with a three-step approach. 

**#1. TO BE RUN INSIDE OF CASA**

First, make sure you know how many channels your ms file actually has. My suggestion is to **always** work on the full ms file which contains **only the desired spectral line** (e.g., 12CO).

Once you have your msfile.ms ready to be processed, just type ```casa``` inside of your terminal. If you don't have CASA installed, then install it first (https://casa.nrao.edu/casa_obtaining.shtml).

Once you are inside of CASA, run the following commands:

```
import shutil
from uvplot import export_uvtable
for i in range(0, 960):
    mstransform(vis='msfile.ms', outputvis='./msfile_'+str(i)+'.ms', datacolumn='DATA', spw='*:'+str(i))
    export_uvtable('./msfile'+str(i)+'.txt', tb, './msfile_'+str(i)+'.ms', datacolumn='DATA')
    shutil.rmtree('./msfile_'+str(i)+'.ms')
```

Of course, you should change "960" to the number of channels your ms file is composed of.

Note that you will need to have the packages ```shutil``` and ```uvplot``` installed. Acutally, you can remove the command ```shutil.rmtree('./msfile_'+str(i)+'.ms')```, but you should check how much storage you have on your laptop first.

**STEP #1 WILL TAKE A WHILE, DEPENDING ON THE SIZES OF MSFILE.MS.** Don't get mad at CASA, let it work and go for a walk in the meanwhile.

**#2. VISUALISE YOU VISIBILITIES**

Once step #1 has finished you will be left with the collection of .txt files containing your data. It's now time to do the magic.

Open ```binning_V_github.py```. 

Here, you have all the functions you need, and everything is ready. The only function you need to run is ```run```.

This is the syntax: ```run(path, name='msfile_name', n_chan=960, n_bins=150, to_keep=['u[m]', 'v[m]', 'Re(V)[Jy]', 'weight'])```

As clearly visible, you **must** specify the path in which you have the .txt files, and the name of the msfile (following step #1, "msfile"), and possibly the number of channels you have in your msfile.

Then, you **can** specify the number of bins (usually 150->300 is ok).

Finally, you **shouldn't** modify the ```to_keep``` parameter, unless you know what you're doing. For example you could choose to visualise the Imaginary part of your visibilities: it's actually cool.

So, just run ```run``` after you chose your parameters and you will be left with a beautiful collection of .png images, one per channel.

**#3. Store your images into a .pdf**

This is the step where your awesome python coding skills might need to arise.

Once we have all the .png files, we want to store them into a single .pdf for displaying them. Open the ```combine_png_into_pdf_github.py``` file and, after specifying your path, just run it. 

If it does not work, the error resides either in line 43 (```png_files = ...```) or in line 46 (```sorted_files = ...```). Ask ChatGPT or DeepSeek to fix your problem depending on the msfile name and path you specified.

**#4: BONUS!**

You might want a video instead of a .pdf. In that case, open the file ```gif_writer.py``` and run it after specifying the path and the output name for your gif.

Again, if you get any errors, it's because of your msfile name. Ask ChatGPT or DeepSeek to fix it.


**YOU'RE READY TO DO SCIENCE NOW! CONGRATS :)**


**If you use this code for any science projects, please make sure to cite it by reporting the github link to this folder.**

Thanks to Giovanni Rosotti and Richard Booth for their precious help in developing this small but useful project.


