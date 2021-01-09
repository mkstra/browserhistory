# Usage on nixos:
# $ niv init
# $ nix-shell shell.nix
# $ python fetch_history.py markus brave && python clean_history.py && python posts_only.py

let
  sources = import ./nix/sources.nix;
  pkgs = import sources.nixpkgs { };
  inherit (pkgs.lib) optional optionals;

  mach-nix = import (builtins.fetchGit {
    url = "https://github.com/DavHau/mach-nix/";
    ref = "refs/tags/3.0.2";
  }) {};

  customPython = mach-nix.mkPython {
    requirements = ''
    pandas
    install
    bs4
    lxml
    '';
    providers = {
      _default = "nixpkgs,wheel,sdist";
    };
  };


in
pkgs.mkShell {
  buildInputs = with pkgs;
  [ customPython ];
}


