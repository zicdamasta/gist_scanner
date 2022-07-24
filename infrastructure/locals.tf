locals {
  project_id = "gist-scanner"
  network = "default"
  region = "europe-north1"
  zone = "europe-north1-a"
  image = "ubuntu-os-cloud/ubuntu-2004-lts"
  ssh_username = "ubuntu"
  public_key_path = "~/.ssh/id_ed25519.pub"
  private_key_path = "~/.ssh/id_ed25519"
}