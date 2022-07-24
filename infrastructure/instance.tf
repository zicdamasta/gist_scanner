# Create a single Compute Engine instance
resource "google_compute_instance" "gist-scanner" {
  name = "gist-scanner"
  machine_type = "e2-micro"
  zone = local.zone
  tags = ["http-server"]

  boot_disk {
    initialize_params {
      image = local.image
    }
  }

  metadata = {
    ssh-keys = "${local.ssh_username}:${file(local.public_key_path)}"
  }
  metadata_startup_script = "sudo apt-get update"

  network_interface {
    network = local.network
    access_config {}
  }
}