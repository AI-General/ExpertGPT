FROM python:3.10-bullseye

# Install GEOS library
# RUN apt-get update && apt-get install -y libgeos-dev pandoc
RUN apt-get update && apt-get install -y \
    libgeos-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    pandoc \
    binutils \
    curl \
    git \
    build-essential && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    rm -rf /var/lib/apt/lists/* && apt-get clean

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install zep-python
RUN pip install --no-cache-dir -r /code/requirements.txt --timeout 200

#You may need to run `chmod +x ./backend/core/scripts/start.sh` on your host machine if you get a permission error
COPY ./scripts/start.sh /code/scripts/start.sh
RUN chmod +x /code/scripts/start.sh

COPY . /code

ENTRYPOINT ["bash", "/code/scripts/start.sh"]
