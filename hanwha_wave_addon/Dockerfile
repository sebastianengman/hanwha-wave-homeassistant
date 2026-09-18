FROM ubuntu:22.04

ARG BUILD_VERSION
ARG BUILD_ARCH
ARG WAVE_URL=https://updates.wavevms.com/hanwha/42921/linux/wave-server-6.1.2.42921-linux_x64.deb

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash ca-certificates cifs-utils curl debconf file libasound2 libcap2-bin \
        libdrm2 libexpat1 libglib2.0-0 libgomp1 libudev1 net-tools procps zlib1g \
    && curl -fsSL --retry 3 --retry-delay 2 -o /tmp/wave-server.deb "${WAVE_URL}" \
    && dpkg -i /tmp/wave-server.deb \
    && rm -f /tmp/wave-server.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY run.sh /run.sh

RUN chmod a+x /run.sh

LABEL \
  io.hass.version="${BUILD_VERSION}" \
  io.hass.type="app" \
  io.hass.arch="${BUILD_ARCH}"

CMD ["/run.sh"]
