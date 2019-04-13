FROM ubuntu:xenial

# Mostly Mike Grima: mgrima@netflix.com
MAINTAINER NetflixOSS <netflixoss@netflix.com>

# Install the Python RTM bot itself:
ARG RTM_VERSION
ADD python-rtmbot-${RTM_VERSION}.tar.gz /

RUN \
  # Install Python:
  apt-get update && \
  apt-get upgrade -y && \
  apt-get install python3 python3-pip nano jq -y

# Add all the other stuff to the plugins:
COPY / /python-rtmbot-${RTM_VERSION}/hubcommander

# Install all the things:
RUN \
  # Rename the rtmbot:
  mv /python-rtmbot-${RTM_VERSION} /rtmbot

  # Install all the deps:
RUN  /bin/bash -c "pip3 install --upgrade pip" && \
  /bin/bash -c "pip3 install --upgrade setuptools" && \
  /bin/bash -c "pip3 install wheel" && \
  /bin/bash -c "pip3 install /rtmbot/hubcommander" && \

  # The launcher script:
  mv /rtmbot/hubcommander/launch_in_docker.py /rtmbot && chmod +x /rtmbot/launch_in_docker.py && \
  rm /rtmbot/hubcommander/python-rtmbot-${RTM_VERSION}.tar.gz

# DEFINE YOUR ENV VARS FOR SECRETS HERE:
ENV SLACK_TOKEN="REPLACEMEINCMDLINE" \
    GITHUB_TOKEN="REPLACEMEINCMDLINE" \
    TRAVIS_PRO_USER="REPLACEMEINCMDLINE" \
    TRAVIS_PRO_ID="REPLACEMEINCMDLINE" \
    TRAVIS_PRO_TOKEN="REPLACEMEINCMDLINE" \
    TRAVIS_PUBLIC_USER="REPLACEMEINCMDLINE" \
    TRAVIS_PUBLIC_ID="REPLACEMEINCMDLINE" \
    TRAVIS_PUBLIC_TOKEN="REPLACEMEINCMDLINE" \
    DUO_HOST="REPLACEMEINCMDLINE" \
    DUO_IKEY="REPLACEMEINCMDLINE" \
    DUO_SKEY="REPLACEMEINCMDLINE"

WORKDIR /rtmbot

# Installation complete!  Ensure that things can run properly:
CMD ["python3", "/rtmbot/launch_in_docker.py"]
