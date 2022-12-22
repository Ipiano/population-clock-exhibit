# Population Clock

A small app built for the Children's Museum of Minnesota Ag Lab to showcase the world's population for young inquisiting minds.

## Initial Requirements

- Display the world population clock
- Will run on a screen
- Should not be interactable
- Will just be a thin, wide screen; only the population on it - 24"x ~6"
- https://www.census.gov/popclock/
- Want to keep it relatively up to date with real world
  - Probably can't just embed the clock from the site - more data than we want
  - Something like a 7-segment display would be good
  - Could run off a RPi-0 or something

# Installation

Release images can be written to an SD card and then used to run a Raspberry Pi. Various tools exist
to do this; these instructions will use the tool from the Raspberry Pi group.

1. Install the RPi imager tool from here: https://www.raspberrypi.com/software/
2. Download a [release](https://github.com/Ipiano/population-clock-exhibit/releases).
3. Run the imaging tool
4. When choosing your OS, choose "custom image" and find the image file that you downloaded
5. Customize the image
   - It is important to leave the username as the default "pi", otherwise the app will not auto-run
   - Choose a password for the device user
   - Enter Wi-Fi details for the network that the device should connect to
6. Write the image to your SD card
   - If you are writing the image on Windows, the imaging tool may get "stuck" at the end of
     the verification step because it ejects the SD card and expects it to be re-connected. You
     can physically remove the SD card and insert it again to complete the verification step.

On first boot, the system may restart a couple times before eventually coming online.

# Details

The project is split up into two parts - the application itself (contained in `app`),
and an image generation script (contained in `image`).

## `app`

The population clock app will display a ticker of the world population which updates
regularly. Statistics used to calculate this value will be loaded from <https://www.census.gov/popclock>.

### Requirements

See `app/requirements.txt` for the list of Python packages needed to run and develop this
app.

### Getting Data

Statistical data is acquired via an HTTP GET request to <https://www.census.gov/popclock/data/population.php/world> - this URL returns a JSON object with details about the world population.
This approach was discovered by inspecting the source of the `census.gov/popclock` page.

The data is expected to contain, at minimum, data like this

```json
{
    "world": {
        "population": 7915854387,
        "population_rate": 2.3441182775241,
        "rate_interval": "second",
        "last_updated": {epoch timestamp seconds}
    }
}
```

Using this data, it's possible to calculate the world population at any point in
time using the equation `world.population + normalized_population_rate * now - world.last_updated`.
`normalized_population_rate` is calculated by converting `world.population_rate` according to
the value of `world.rate_interval`.

### Caching

The population clock app will cache the result from `census.gov` any time it is
successfully retrieved. If the cache file is present, this is loaded on startup
before attempting to get new data, allowing the tool to display approximate
information even if no network connection is available.

The application will not function if the cache file cannot be written.

### UI

If the tool is run in graphical mode, a simple Qt QML UI will display the
world population information, updating regularly. If no cached data is present,
and the data has not been retrieved from `census.gov`, this UI will display the
text "Loading..."

## `image`

This directory contains everything needed to build a Raspberry Pi image that will
run the application on boot. It uses the [PI gen](https://github.com/RPi-Distro/pi-gen)
project to accomplish this.

The image is produced by running `image/build-image.sh`. Run
`image/build-image.sh --help` for details about configuring the image. Images
produced by this script are placed in `image/deploy`. Building an image from
scratch is expected to take 30-45 minutes.

Once the image has been built, use something like `RPi-Imager` to write the image to an
SD card. (See <https://www.raspberrypi.com/software/>)

### Requirements

To run `build-image.sh` and produce an image, your system must meet the following
requirements:

- `git` must be installed (to clone `pi-gen`)
- `docker` must be installed
  - It is unknown if rootless docker supports the build process, however, it
    should not be necessary to add your user to the `docker` group
- The following packages must be installed OR your user must have root permissions
  so that the script can install them for you
  - `qemu` `binfmt-support` `qemu-user-static`
