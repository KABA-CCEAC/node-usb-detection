[![npm version](https://badge.fury.io/js/usb-detection.svg)](http://badge.fury.io/js/usb-detection) [![Gitter](https://badges.gitter.im/MadLittleMods/node-usb-detection.svg)](https://gitter.im/MadLittleMods/node-usb-detection?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)


# usb-detection

`usb-detection` allows you to listen for insert/remove events of USB devices on your system.


### [Changelog](https://github.com/MadLittleMods/node-usb-detection/blob/master/CHANGELOG.md)


# Install

```sh
npm install usb-detection
```

## Install for Electron

This module uses native extensions and needs to be compiled for your target version of Electron. Precompiled binaries for recent Node.js and Electron versions are built and published using [prebuild][] and can be installed automatically using [electron-rebuild][].

See the [Electron docs for using native modules][electron-native-modules] to ensure your project is set up to correctly use the prebuilt binaries for your version of Electron.

[prebuild]: https://github.com/prebuild/prebuild
[electron-rebuild]: https://github.com/electron/electron-rebuild
[electron-native-modules]: https://www.electronjs.org/docs/tutorial/using-native-node-modules

---

If you run into the following error, here are the exact steps you can use:

```
detection.node was compiled against a different Node.js version using NODE_MODULE_VERSION 72. This version of Node.js requires NODE_MODULE_VERSION 80. Please try re-compiling or re-installing
```

 1. `npm i electron-rebuild --save-dev`
 1. `./node_modules/.bin/electron-rebuild`


# Usage

```js
var usbDetect = require('usb-detection');

usbDetect.startMonitoring();

// Detect add/insert
usbDetect.on('add', function(device) { console.log('add', device); });
usbDetect.on('add:vid', function(device) { console.log('add', device); });
usbDetect.on('add:vid:pid', function(device) { console.log('add', device); });

// Detect remove
usbDetect.on('remove', function(device) { console.log('remove', device); });
usbDetect.on('remove:vid', function(device) { console.log('remove', device); });
usbDetect.on('remove:vid:pid', function(device) { console.log('remove', device); });

// Detect add or remove (change)
usbDetect.on('change', function(device) { console.log('change', device); });
usbDetect.on('change:vid', function(device) { console.log('change', device); });
usbDetect.on('change:vid:pid', function(device) { console.log('change', device); });

// Get a list of USB devices on your system, optionally filtered by `vid` or `pid`
usbDetect.find(function(err, devices) { console.log('find', devices, err); });
usbDetect.find(vid, function(err, devices) { console.log('find', devices, err); });
usbDetect.find(vid, pid, function(err, devices) { console.log('find', devices, err); });
// Promise version of `find`:
usbDetect.find().then(function(devices) { console.log(devices); }).catch(function(err) { console.log(err); });

// Allow the process to exit
//usbDetect.stopMonitoring()
```


# API

## `usbDetect.startMonitoring()`

Start listening for USB add/remove/change events. This will cause the Node.js process to stay open until you call `usbDetect.stopMonitoring()` (see below).


## `usbDetect.stopMonitoring()`

Stop listening for USB add/remove/change events. This will also allow the Node.js process to exit.

This is really only meant to be called once on exit. No guarantees if you start/stop monitoring multiple times, see https://github.com/MadLittleMods/node-usb-detection/issues/53


## `usbDetect.on(eventName, callback)`

 - `eventName`
    - `add`: also aliased as `insert`
       - `add:vid`
       - `add:vid:pid`
    - `remove`
       - `remove:vid`
       - `remove:vid:pid`
    - `change`
       - `change:vid`
       - `change:vid:pid`
 - `callback`: Function that is called whenever the event occurs
    - Takes a `device`


```js
var usbDetect = require('usb-detection');
usbDetect.startMonitoring();

usbDetect.on('add', function(device) {
	console.log(device);
});

/* Console output:
{
	locationId: 0,
	vendorId: 5824,
	productId: 1155,
	deviceName: 'Teensy USB Serial (COM3)',
	manufacturer: 'PJRC.COM, LLC.',
	serialNumber: '',
	deviceAddress: 11
}
*/
```


## `usbDetect.find(vid, pid, callback)`

**Note:** All `find` calls return a promise even with the node-style callback flavors.

 - `find()`
 - `find(vid)`
 - `find(vid, pid)`
 - `find(callback)`
 - `find(vid, callback)`
 - `find(vid, pid, callback)`

Parameters:

 - `vid`: restrict search to a certain vendor id
 - `pid`: restrict search to s certain product id
 - `callback`: Function that is called whenever the event occurs
    - Takes a `err` and `devices` parameter.


```js
var usbDetect = require('usb-detection');
usbDetect.startMonitoring();

usbDetect.find(function(err, devices) {
	console.log(devices, err);
});
// Equivalent to:
//		usbDetect.find().then(function(devices) { console.log(devices); }).catch(function(err) { console.log(err); });

/* Console output:
[
	{
		locationId: 0,
		vendorId: 0,
		productId: 0,
		deviceName: 'USB Root Hub',
		manufacturer: '(Standard USB Host Controller)',
		serialNumber: '',
		deviceAddress: 2
	},
	{
		locationId: 0,
		vendorId: 5824,
		productId: 1155,
		deviceName: 'Teensy USB Serial (COM3)',
		manufacturer: 'PJRC.COM, LLC.',
		serialNumber: '',
		deviceAddress: 11
	}
]
*/
```




# FAQ

### The script/process is not exiting/quiting

```js
var usbDetect = require('usb-detection');

// Do some detection
usbDetect.startMonitoring();

// After this call, the process will be able to quit
usbDetect.stopMonitoring();
```

### `usbDetect.find()` always returns the same list of devices, even after removal.

Make sure you call `usbDetect.startMonitoring()` before any calls to `usbDetect.find()`.


### `npm run rebuild` -> `The system cannot find the path specified.`

If you are running into the `The system cannot find the path specified.` error when running `npm run rebuild`,
make sure you have Python installed and on your PATH.

You can verify `node-gyp` is configured correctly by looking at the output of `node-gyp configure --verbose`.


### To build a debug version with error outputs use:

```sh
$ npm run rebuild --debug
```


# Development (compile from source)

This assumes you also have everything on your system necessary to compile ANY native module for Node.js using [node-gyp](https://github.com/nodejs/node-gyp). This may not be the case, though, so please ensure the following requirements are satisfied before filing an issue about "does not install".

If you are developing locally, you should use [Node.js v14](https://nodejs.org), but if you are just trying to install usb-detection, you should be able to compile from source using any supported version of Node.

### Windows

See [node-gyp's Windows installation instructions](https://github.com/nodejs/node-gyp#on-windows).

### macOS

See [node-gyp's macOS installation instructions](https://github.com/nodejs/node-gyp#on-windows).

### Linux

You know what you need for you system, basically your appropriate analog of build-essential. Keep rocking! See [node-gyp's Unix installation instructions](https://github.com/nodejs/node-gyp#on-unix) for more details.

```sh
sudo apt-get install build-essential
```

You will also need to install `libudev-dev`.

```sh
sudo apt-get install libudev-dev
```

# Testing

We have a suite of Mocha/Chai tests.

The tests require some manual interaction of plugging/unplugging a USB device. Follow the cyan background text instructions.

```sh
npm test
```
