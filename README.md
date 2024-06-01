# Frame Batteries

This project provides a docker container with basic developer tooling for Brilliant Lab's [Frame](https://docs.brilliant.xyz). It includes a Bluetooth Client, Lua script uploading, and example code to get you up and running.

The goal is to accelerate development for all of us who want to hack on this bleeding edge platform. The main development community [lives on discord](https://discord.com/invite/vDS9X7gdwg), come join us!



## Installation

VS Code integration is the native path but run the container however you wish. 

* Install VS Code
* Add the Remote Containers Exstension
* Ensure that Docker is running on your machine
* In the bottom left, select 'Open in container'

When you want to actually connect to the frame, you may run into some issues with bluetooth in the docker container. For now I'd recommend just running the script outside of the container and using the container's features for development and testing.

Sorry about that...

## Running Tests

To run tests, run the following command

```bash
make test
```


## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.

