{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "python-dev-shell";

  buildInputs = [
    (
      pkgs.python3.withPackages (ps: [ 
        ps.pillow
        ps.black
      ])
    )
  ];
}
