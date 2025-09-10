# To learn more about how to use Nix to configure your environment
# see: https://firebase.google.com/docs/studio/customize-workspace
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.05"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    (pkgs.python311.withPackages (ps: with ps; [
      litellm
      python-dotenv
      pydantic
      jupyter
      matplotlib
      pandas
      networkx
      streamlit
      openpyxl
      pip
    ]))
  ];

  # Sets environment variables in the workspace
  # environment.variables = {
  #   "MY_VARIABLE" = "value";
  # };

  # Disables extensions that are known to conflict with your configuration.
  # devcontainer.conflictExtensions = [
  #   "ms-python.python"
  # ];
}
