# Jupyter Notebook - Anaconda Installation

This tutorial will show how to install Jupyter Notebook via Anaconda on your machine (assuming that you have Python 3 or higher installed). The installation process is pretty straight-forward, installing Anaconda  distribution will in turn install  Jupyter notebook and several other important packages like NumPy, Pandas.



**Step 1:** If you follow the link (<https://www.anaconda.com/download/>) to the Anaconda download page you can choose between installers for Windows, macOS, and Linux

![img](https://cdn-images-1.medium.com/max/800/0*TmfU90PgHumYYsTI.png)



**Step2:** Select the operating system of your choice and choose Python 3.x download variant. The download should start after this, it’s a pretty large file, so it might take some time.

**Step3:** Go through the installation procedure with the installer, allow all recommended settings.

**Step4:** After the installation is complete, search for Anaconda Navigator in the Start menu. You’ll see something which looks like this:

![img](https://cdn-images-1.medium.com/max/2000/1*8VwF5RUh4vEf4FfrKMw7qg.png)



**Step5:** You can see that Jupyter Notebook is already installed. Press the launch button to start or navigate in command line to the folder containing a jupyter notebook file with `.ipynb` extension and type the command `jupyter notebook`. You will see the following response on the command line:

![img](https://cdn-images-1.medium.com/max/800/0*DEAK_sdiIeXHAKpu.png)



The web server will start and the Jupyter Notebook application will open in your default browser automatically. You should be able to see a browser output which is similar to the following screenshot:

![img](https://cdn-images-1.medium.com/max/800/0*1ld_s2rVcaBV4qz3.png)



## Updating and Installing Packages in Anaconda

1. Open your Anaconda Prompt from the Start menu.

2. Navigate to the **anaconda** directory.

3. Run `conda update conda`

4. To install packages in your environment run `conda install [package_name]`
