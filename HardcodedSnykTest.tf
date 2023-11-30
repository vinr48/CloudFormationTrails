provider "aws" {
  region     = "us-east-1"
  access_key = "AKIAQTSHLD4OL6SWD77P"
  secret_key = "Sn3gBn9JwawRNwJHnYZW2Jo0yffUiTZECoF9ZM9"
}

resource "aws_instance" "myec2" {
    ami = "ami-00c39f71452c08778"
    instance_type = "t2.micro"
}
