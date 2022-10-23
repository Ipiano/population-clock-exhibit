# Population Clock

A small app built for the Children's Museum of Minnesota Ag Lab to showcase the world's population for young inquisiting minds.

## Initial Requirements

* Display the world population clock
* Will run on a screen
* Should not be interactable
* Will just be a thin, wide screen; only the population on it - 24"x ~6"
* https://www.census.gov/popclock/
* Want to keep it relatively up to date with real world
    * Probably can't just embed the clock from the site - more data than we want
    * Something like a 7-segment display would be good
    * Could run off a RPi-0 or something

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
* `git` must be installed (to clone `pi-gen`)
* `docker` must be installed
  * It is unknown if rootless docker supports the build process, however, it
    should not be necessary to add your user to the `docker` group
* The following packages must be installed OR your user must have root permissions
  so that the script can install them for you
  * `qemu` `binfmt-support` `qemu-user-static`
