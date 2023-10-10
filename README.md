# mx-sdk-clang-contract-builder

**Important:** we do not offer support for writing contracts in C or C++. The recommended language to write smart contracts is **Rust**.

This repository is only meant to be used for building **test** smart contracts, as found within unit and integration tests of the MultiversX Node and VM.

## Build the Docker image

```
docker build --network=host . -t multiversx/sdk-clang-contract-builder:latest -f ./Dockerfile
```

## Building contracts using Docker

The container must be ran as the current user, not as root. In the example below, see the `--user` option. Furthermore, it's recommended to use a stateless container. That is, remove it after use with `--rm`. 

Note that, by default, the entrypoint `build.py` is invoked with `--path=/contract`. Thus, map the contract directory to `/contract` in the container:

```
export CONTRACT_PATH=~/clang-contracts/simple-counter

docker run --network=host --user=$(id -u):$(id -g) --rm -it --volume $CONTRACT_PATH:/contract multiversx/sdk-clang-contract-builder:latest
```

## Building contracts without Docker:

It's possible to build contracts without setting up a Docker container. Simply invoke the `build.py` Python script directly.

```
./build.py --llvm=14 --path=~/clang-contracts/simple-counter
```

