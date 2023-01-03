#!/bin/bash
sudo curl http://www.lua.org/ftp/lua-5.3.2.tar.gz | tar xz
pushd lua-5.3.2
make linux -j
make install
popd
