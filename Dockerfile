FROM ubuntu:22.04

# Constants
ARG VERSION_LLVM="16"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    lsb-release \
    wget \ 
    software-properties-common \
    gnupg \
    python3.10 && \
    rm -rf /var/lib/apt/lists/*

# Install clang
RUN wget https://apt.llvm.org/llvm.sh && \
    chmod +x ./llvm.sh && \
    ./llvm.sh ${VERSION_LLVM} && \
    rm ./llvm.sh

COPY "build.py" "/build.py"

# Make sure to keep "VERSION_LLVM" and "--llvm" in sync.
ENTRYPOINT ["/build.py", "--language", "c", "--llvm", "16", "--path", "/contract"]

LABEL llvm=${VERSION_LLVM}
