* https://github.com/davatorium/rofi
* compile rofi in ubuntu 22.04 https://gist.github.com/cboully/52a0d46a49d18bd9e3e51007282ebcbe
    * ```shell
      git clone --depth=1 --single-branch --branch 1.7.5 https://github.com/davatorium/rofi.git
      cd rofi
      git submodule update --init

      sudo apt install bison flex libxcb-xkb-dev libxkbcommon-x11-dev \
      libxcb-ewmh-dev libxcb-icccm4-dev libxcb-xrm-dev libxcb-xinerama0-dev \
      libstartup-notification0-dev libmpdclient-dev libxcb-randr0-dev \
      libxcb-cursor-dev doxygen cppcheck ohcount go-md2man meson
      # Had to install this on kubuntu 22.04
      sudo apt install libcairo2-dev libpango1.0-dev libgdk-pixbuf-2.0-dev

      meson setup build
      ninja -C build
      sudo ninja -C build install
      ```
* https://github.com/topics/rofi-scripts
* snippets
    * https://github.com/tkancf/rofi-snippet/blob/master/config.toml
    * https://github.com/raphaelfournier/rofi-modi-snippets
