#!/usr/local/bin/python
from basis import msg

def examples():
    """Prints examples of using the script to the console using colored output.
    """
    script = "BASIS_SOLVE"
    explain = (" For simple 1D Quantum Potential Solver"
               " in real-time.")
    contents = [(("Solve the potential in `kp.cfg` using 200 basis functions,"),
		"basis_solve.py 200 -potential kp.cfg", 
		This saves the solution to the default 'output.dat'") 
		("Start plotting the data from the COM3 serial port."), 
                 "livemon.py COM3",
                 "If '-logdir' is not specified, *no* data will be logged."),
                (("Plot *and* log the data from /dev/tty."),
                 "livemon.py /dev/tty -logdir ~/sensordata", ""),
                ("Log the data, but don't generate a live plot.",
                 "livemon.py COM3 -noplot -logdir C:\\sensordata\\", ""),
                ("List the available serial ports on the system.",
                 "livemon.py list", ""),
                ("Use the config file `custom.cfg` to log and plot the data. "
                 "Plot any sensors listed in that file.",
                 "livemon.py auto -config custom.cfg",
                 "If your file is called `sensors.cfg`, you can just use "
                 "`livemon.py auto`.")]
    required = ("REQUIRED: potential config file 'pot.cfg',")
    output = ("RETURNS: plot window; for logging-only mode, the data being "
              "logged is also periodically printed to stdout.")
    details = ("The plotting uses `matplotlib` with the default configured "
               "backend. If you want a different backend, set the rc config "
               "for `matplotlib` using online documentation. However, many "
               "backends don't play well with the animation (depending on OS "
               "type and version, etc., etc.; so use carefully.")
    outputfmt = ("")

    msg.example(script, explain, contents, required, output, outputfmt, details)


script_options = {
    "N":{dict(default=100,type=int,
		help=("Spectifices how many basis functions to use in the expansion "
		      "solution."))}	
    "-method": dict(default="average", choices=["last", "average"],
                    help=("Specifies how buffered data is aggregated each "
                          "time it is read from the serial port.")),

    "-listen": dict(action="store_true",
                    help=("Prints the raw output from the serial port "
                          "instead of plotting and logging it. Useful "
                          "for debugging port connection issues.")),
    "-virtual": dict(action="store_true",
                     help=("Specifies that the port being connected to is "
                           "virtual (e.g., with `socat`), which changes the "
                           "parameters for connection.")),
    "-sensors": dict(nargs="+", default="all",
                     help="Filter the list of sensors being logged/plotted."),
    "-maxpts": dict(type=int, default=100,
                    help=("Maximum number of values to keep in the plot "
                          "for each sensor")),
    "-window": dict(type=float, default=20.,
                    help="Width of window in time units."),
    "-wait": dict(type=float, default=1.,
                  help=("Number of seconds to wait before failing because "
                        "no data is present on the stream for plotting."))
    }
"""dict: default command-line arguments and their
    :meth:`argparse.ArgumentParser.add_argument` keyword arguments.
"""


def _parser_options():
    """Parses the options and arguments from the command line."""
    #We have two options: get some of the details from the config file,
    import argparse
    from basis import base
    pdescr = "1D Quantum Potential solver."
    parser = argparse.ArgumentParser(parents=[base.bparser], description=pdescr)
    for arg, options in script_options.items():
        parser.add_argument(arg, **options)

    args = base.exhandler(examples, parser)
    if args is None:
        return

    return args

if __name__ == '__main__': # pragma: no cover
    run(_parser_options())
