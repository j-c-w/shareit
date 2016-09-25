Configuring a ShareCenter

-------------------

Most likely,  you will want to configure a share center.
To do this, you need to fill in the following files:

    .addr
    .name
    .tools
    .email

The name and addr files should be filled in
with your name and address (which should be the
only things in the files). See the files's current
contents for examples.

The .email file should be filled in with *your*
email address. This is crucial for security

The .tools file should be filled in as follows:

    Tool Name
    Tool Price Per Hour (in pennies, so 1p = 1, 1 pound = 100)
    Tool Description (as a single line of text)
    ID (MUST be UNIQUE (No spaces please))

    Next item (note blank line)
    ...



NOTE TO SELF ** code injection is very possible there
got to tackle that.

You must have python (2.7), flask and flask-restful.
Download these as follows:

    http://tecadmin.net/install-python-2-7-on-ubuntu-and-linuxmint/

And for flask and flask-restful, you can use pip:

    ` pip install flask flask-restful


Then, start the server by *moving to the shareit directory*
and executing:

    python mytools.py

Now, we need to make a crontab to support starting
the library at boot:

    crontab -e

Then enter:

    @reboot cd ...(path to shareit folder)...;python mytools.py

------------------------------

For a nameserver, there is less setup. You need to
clone the project (and install the tools as
above).

After this is done, you may start the server by
executing

    python nameserver.py


To get some servers to use *your* nameserver, you
must note the IP address of your sever. Then,
get the corresponding libraries to change
their '.nameserverIP' files to contain
the IP address of your name server.

Finally, we need this process to start on boot
of the pi:

    crontab -e

And at the bottom of the file:

    @reboot cd .....(path to shareit directory)...; python nameserver.py



