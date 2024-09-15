{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "python-dev-shell";

  buildInputs = [
    (
      pkgs.python3.withPackages (ps: [ 
        # ps.pip
        ps.numpy 
        ps.matplotlib 
        ps.scikit-image
      ])
    )
  ];
}
