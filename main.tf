terraform {
  required_providers {
    sbercloud = {
      source  = "sbercloud-terraform/sbercloud"
      version = "1.10.0"
    }
  }
}
#Конфигурируем провайдера сберклауд
provider "sbercloud" {
  region     = var.region
  auth_url   = var.auth_url
  access_key = var.access_key
  secret_key = var.secret_key
}

variable "region" {
  description = "our region ru-moscow-1"
  type        = string
}

variable "auth_url" {
  description = "auth url"
  type        = string
}

variable "access_key" {
  description = "access key"
  type        = string
}

variable "secret_key" {
  description = "Secret key"
  type        = string
}

variable "root_passwd" {
  description = "root password"
  sensitive   = true
  type = string
}


#Данные для ссылки на имя проекта
data "sbercloud_enterprise_project" "enterprise_project" {
  name = "default"
}

#Creating vpc_01 
resource "sbercloud_vpc" "vpc_01" {
    name = "vpc_01"
    cidr = "192.168.0.0/16"
    enterprise_project_id = data.sbercloud_enterprise_project.enterprise_project.id
}

#Creating subnet_01
resource "sbercloud_vpc_subnet" "subnet_01" {
    name = "subnet_01"
    cidr = "192.168.10.0/24"

    gateway_ip = "192.168.10.1"
    vpc_id = sbercloud_vpc.vpc_01.id

    primary_dns = "100.125.13.59"
    secondary_dns = "8.8.8.8"

    dhcp_enable = true
}

#creating eip for front-end
resource "sbercloud_vpc_eip" "front_eip" {
  publicip {
    type = "5_bgp"
  }
  bandwidth {
    name        = "front_bandwidth"
    size        = 5
    share_type  = "PER"
    charge_mode = "bandwidth"
  }
}

resource "sbercloud_vpc_eip" "snat_eip" {
  publicip {
    type = "5_bgp"
  }
  bandwidth {
    name        = "snat_bandwidth"
    size        = 5
    share_type  = "PER"
    charge_mode = "bandwidth"
  }
}

#получаем зоны AZ
data "sbercloud_availability_zones" "myaz" {}

#получаем данные для образа debian
data "sbercloud_images_image" "debian10_image" {
  name        = "Debian 10.0.0 64bit"
  most_recent = true
}

# Получаем flavor name
data "sbercloud_compute_flavors" "flavor_name" {
  availability_zone = data.sbercloud_availability_zones.myaz.names[0]
  performance_type  = "normal"
  cpu_core_count    = 2
  memory_size       = 8
}


resource "sbercloud_compute_eip_associate" "associated_01" {
  public_ip   = sbercloud_vpc_eip.front_eip.address
  instance_id = sbercloud_compute_instance.nginx-front.id
}

resource "sbercloud_compute_eip_associate" "associated_02" {
  public_ip   = sbercloud_vpc_eip.snat_eip.address
  instance_id = sbercloud_compute_instance.docker-sandbox.id
}



#Создаём ECS docker-sandbox
resource "sbercloud_compute_instance" "docker-sandbox" {
  name              = "docker-sandbox"
  image_id          = data.sbercloud_images_image.debian10_image.id
  flavor_id         = data.sbercloud_compute_flavors.flavor_name.ids[0]
  security_groups   = ["default"]
  availability_zone = data.sbercloud_availability_zones.myaz.names[0]
  system_disk_type  = "SSD"
  system_disk_size  = 40
  admin_pass        = var.root_passwd
#  user_data         = file("${path.module}/hello.txt")
  network {
    uuid = sbercloud_vpc_subnet.subnet_01.id
    fixed_ip_v4 = "192.168.10.50"

  }
  
}

#Создаём ECS 2
resource "sbercloud_compute_instance" "nginx-front" {
  name              = "nginx-front"
  image_id          = data.sbercloud_images_image.debian10_image.id
  flavor_id         = data.sbercloud_compute_flavors.flavor_name.ids[0]
  security_groups   = ["default"]
  availability_zone = data.sbercloud_availability_zones.myaz.names[0]
  system_disk_type  = "SSD"
  system_disk_size  = 40
  admin_pass        = var.root_passwd
#  user_data         = var.nginx_deploy
  network {
    uuid = sbercloud_vpc_subnet.subnet_01.id
    fixed_ip_v4 = "192.168.10.100"
  }
}




