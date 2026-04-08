# Dockerfile for the ASDN Net-Tools Image — SOLUTION
# ====================================================
# This image contains all networking tools needed for the course labs.

FROM ubuntu:22.04

# Install all networking tools in a single layer
# - Combine commands with && to reduce layers
# - Use DEBIAN_FRONTEND=noninteractive to prevent interactive prompts
# - Clean up apt cache to reduce image size
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    iproute2 \
    iputils-ping \
    traceroute \
    tcpdump \
    curl \
    wget \
    dnsutils \
    netcat-openbsd \
    iptables \
    net-tools \
    nmap \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Default command: open a bash shell
CMD ["bash"]
