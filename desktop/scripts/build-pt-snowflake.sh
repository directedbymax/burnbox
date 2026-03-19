#!/bin/bash
SNOWFLAKE_TAG=v2.10.1

OS=$(uname -s)

mkdir -p ./build/snowflake
cd ./build/snowflake
git clone https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/snowflake.git || echo "already cloned"
cd snowflake
git checkout $SNOWFLAKE_TAG
if [ "$OS" == "Darwin" ]; then
    if [[ $(uname -m) == 'arm64' ]]; then
        go build -o ../../../burnbox/resources/tor/snowflake-client-arm64 ./client
        GOOS=darwin GOARCH=amd64 go build -o ../../../burnbox/resources/tor/snowflake-client-amd64 ./client
        lipo -create -output ../../../burnbox/resources/tor/snowflake-client ../../../burnbox/resources/tor/snowflake-client-arm64 ../../../burnbox/resources/tor/snowflake-client-amd64
        rm ../../../burnbox/resources/tor/snowflake-client-arm64 ../../../burnbox/resources/tor/snowflake-client-amd64
    elif [[ $(uname -m) == 'x86_64' ]]; then
        go build -o ../../../burnbox/resources/tor/snowflake-client ./client
    fi
else
    go build -o ../../../burnbox/resources/tor/snowflake-client ./client
fi
