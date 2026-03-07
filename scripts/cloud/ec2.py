import subprocess
import random
import string
import argparse
import yaml
import os

KEY_PATH = os.path.expanduser("~/Downloads/LightsailDefaultKey-ap-east-1.pem")


def _get_ec2_instances():
    print("Fetching EC2 instances...")
    try:
        result = subprocess.run(
            ["aws", "ec2", "describe-instances", "--region", "ap-east-1"],
            capture_output=True,
            text=True,
            check=True,
        )
        print("EC2 instances fetched successfully.")
        return yaml.safe_load(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error getting EC2 instances: {e}")
        return None
    except yaml.YAMLError as e:
        print(f"Error decoding YAML response: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def _get_ec2_instance(instance_id):
    print(f"Fetching details for instance: {instance_id}")
    try:
        result = subprocess.run(
            [
                "aws",
                "ec2",
                "describe-instances",
                "--region",
                "ap-east-1",
                "--instance-ids",
                instance_id,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        instance_data = yaml.safe_load(result.stdout)
        if (
            not instance_data
            or "Reservations" not in instance_data
            or not instance_data["Reservations"]
            or "Instances" not in instance_data["Reservations"][0]
            or not instance_data["Reservations"][0]["Instances"]
        ):
            print(f"Could not find instance with id: {instance_id}")
            return None
        return instance_data["Reservations"][0]["Instances"][0]
    except subprocess.CalledProcessError as e:
        print(f"Error getting instance details: {e}")
        return None
    except yaml.YAMLError as e:
        print(f"Error decoding YAML response: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def create_ec2_instance(
    instance_name=None,
    availability_zone="ap-east-1a",
    instance_type="t3.micro",
    user_data=None,
):
    if not instance_name:
        random_chars = "".join(random.choice(string.ascii_lowercase) for _ in range(4))
        instance_name = f"{random_chars}"

    if not user_data:
        user_data = """#!/bin/bash
        sudo apt update
        """
    print(
        f"Creating EC2 instance with name: {instance_name}, zone: {availability_zone}, type: {instance_type}..."
    )

    command = [
        "aws",
        "ec2",
        "run-instances",
        "--image-id",
        "ami-01c19c4912400a3fd",
        "--instance-type",
        instance_type,
        "--block-device-mappings",
        '{"DeviceName":"/dev/sda1","Ebs":{"Encrypted":false,"DeleteOnTermination":true,"Iops":3000,"SnapshotId":"snap-0c3acb47c6e06a14b","VolumeSize":8,"VolumeType":"gp3","Throughput":125}}',
        "--network-interfaces",
        '{"DeviceIndex":0,"Groups":["sg-preview-1"]}',
        "--credit-specification",
        '{"CpuCredits":"unlimited"}',
        "--metadata-options",
        '{"HttpEndpoint":"enabled","HttpPutResponseHopLimit":2,"HttpTokens":"required"}',
        "--private-dns-name-options",
        '{"HostnameType":"ip-name","EnableResourceNameDnsARecord":true,"EnableResourceNameDnsAAAARecord":false}',
        "--count",
        "1",
        "--region",
        "ap-east-1",
        "--tag-specifications",
        f"ResourceType=instance,Tags=[{{Key=Name,Value={instance_name}}}]",
    ]

    if user_data:
        command.extend(["--user-data", user_data])

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        instance_data = yaml.safe_load(result.stdout)
        instance_id = instance_data["Instances"][0]["InstanceId"]
        print(
            f"EC2 instance '{instance_name}' created successfully with id: {instance_id}."
        )
        return instance_id
    except subprocess.CalledProcessError as e:
        print(f"Error creating EC2 instance: {e}")
        return None


def delete_all_ec2_instances(instance_id=None):
    if instance_id:
        print(f"Deleting instance: {instance_id}")
        print(
            f"Executing command: aws ec2 terminate-instances --instance-ids {instance_id} --region ap-east-1"
        )
        try:
            subprocess.run(
                [
                    "aws",
                    "ec2",
                    "terminate-instances",
                    "--instance-ids",
                    instance_id,
                    "--region",
                    "ap-east-1",
                ],
                check=True,
            )
            print(f"EC2 instance '{instance_id}' deleted successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error deleting EC2 instance: {e}")
        return

    instances_yaml = _get_ec2_instances()
    if not instances_yaml or "Reservations" not in instances_yaml:
        print("No EC2 instances found to delete.")
        return

    instance_list = []
    for reservation in instances_yaml.get("Reservations", []):
        instance_list.extend(reservation.get("Instances", []))

    if not instance_list:
        print("No EC2 instances found to delete.")
        return

    for instance in instance_list:
        instance_id = instance["InstanceId"]
        print(f"Deleting instance: {instance_id}")
        print(
            f"Executing command: aws ec2 terminate-instances --instance-ids {instance_id} --region ap-east-1"
        )
        subprocess.run(
            [
                "aws",
                "ec2",
                "terminate-instances",
                "--instance-ids",
                instance_id,
                "--region",
                "ap-east-1",
            ],
            check=True,
        )
    print("All EC2 instances deleted successfully.")


def install_outline_server(instance_id):
    instance = _get_ec2_instance(instance_id)
    if not instance:
        return
    public_ip = instance["PublicIpAddress"]
    print(f"Installing outline server on instance: {instance_id} with IP: {public_ip}")
    user_data = """#!/bin/bash
    sudo apt update
    sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/Jigsaw-Code/outline-server/master/src/server_manager/install_scripts/install_server.sh)"
    """

    os.chmod(KEY_PATH, 0o600)
    print(f"Executing command: chmod 600 {KEY_PATH}")

    ssh_command = ["ssh", "-i", KEY_PATH, f"ubuntu@{public_ip}", user_data]
    print(f"Executing command: {' '.join(ssh_command)}")
    try:
        subprocess.run(ssh_command, check=True)
        print(f"Outline server installed on {instance_id} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing outline server: {e}")


def open_firewall_ports(instance_id):
    print(f"Opening firewall ports for instance: {instance_id}")

    instance = _get_ec2_instance(instance_id)
    if not instance:
        return

    security_groups = instance["SecurityGroups"]
    if not security_groups:
        print(f"No security groups found for instance: {instance_id}")
        return

    security_group_id = security_groups[0]["GroupId"]

    for protocol in ["tcp", "udp"]:
        command = [
            "aws",
            "ec2",
            "authorize-security-group-ingress",
            "--group-id",
            security_group_id,
            "--protocol",
            protocol,
            "--port",
            "1000-65535",
            "--cidr",
            "0.0.0.0/0",
            "--region",
            "ap-east-1",
        ]
        print(f"Executing command: {' '.join(command)}")
        subprocess.run(command, check=True)
    print(f"Firewall ports opened for instance '{instance_id}' successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create or delete EC2 instances.")
    parser.add_argument(
        "--job",
        type=str,
        choices=["create", "delete", "install"],
        required=True,
        help="Action type: create, delete, or install",
    )
    args = parser.parse_args()

    print("Setting AWS region to ap-east-1")
    subprocess.run(["aws", "configure", "set", "region", "ap-east-1"], check=True)

    if args.job == "create":
        instance_id = create_ec2_instance()
        if instance_id:
            open_firewall_ports(instance_id)
    elif args.job == "delete":
        instance_id = input("Enter the instance id to delete: ")
        delete_all_ec2_instances(instance_id)
    elif args.job == "install":
        instance_id = input("Enter the instance id to install Outline server on: ")
        install_outline_server(instance_id)
