# Hitron Cable CPE Tool

A command-line tool for communicating with Hitron Cable Consumer Provided Equipment (ie. Residential Modem/Router).

This tool utilizes the API provided by the device's web interface to allow scripting. In particular, I use it to turn my
WiFi on and off with a schedule.

I've only used this with the CGNVM-3582 model, but it may work with others, *YMMV*.

## Prerequisites

* Python 3+
* Requests module
  - `pip install requests`


## Running

All commands can be executed through the script wrapper, `hitron`. For example, to see if your device responds with the defaults, send a probe:

```
./hitron probe
```

If your device address is not the default (192.168.0.1) you can set it with the --address option:

```
./hitron probe --address=192.168.10.1
```

For a list of supported commands type:

```
./hitron help
```

For details of a particular command, pass the help flag to the command:

```
./hitron probe --help
```

## Configure

Certain options are almost always required:
* password
* address
* user

If you are not using the defaults for these (and you shouldn't for password), you can place
values in a configuration file to be read instead of as command line options. You can point
to this file with the `config` option, or place a file named `.hitronrc` in the current
working directory.
