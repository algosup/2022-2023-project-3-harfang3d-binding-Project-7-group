sudo curl http://www.lua.org/ftp/lua-5.3.2.tar.gz | tar xz
sudo pushd lua-5.3.2

sudo LUA_HOME_DIR=./install/lua

sudo make linux -j
sudo make INSTALL_TOP="$LUA_HOME_DIR" install

sudo popd
