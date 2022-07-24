resource "google_compute_firewall" "http-server" {
  name = "http-server"
  network = local.network

  # allow port 80
  allow {
    protocol = "tcp"
    ports = ["80"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags = ["http-server"]
}