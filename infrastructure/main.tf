# save nat ip as variable


resource "null_resource" "ubuntu" {
  triggers = {
    always_run = timestamp()
  }

  provisioner "remote-exec" {
    inline = ["sudo apt update && sudo apt-get install ansible -y"]

    connection {
      host = google_compute_instance.gist-scanner.network_interface.0.access_config.0.nat_ip
      type = "ssh"
      user = local.ssh_username
      private_key = file(local.private_key_path)
    }
  }
  provisioner "local-exec" {
    command = "ansible-playbook ansible/install.yml -i ${google_compute_instance.gist-scanner.network_interface.0.access_config.0.nat_ip}, --private-key ${local.private_key_path}"
  }
}
