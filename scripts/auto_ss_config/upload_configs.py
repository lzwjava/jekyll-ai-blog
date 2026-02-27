#!/usr/bin/env python3

from google.cloud import storage
from ruamel.yaml import YAML
import base64
import re
import logging
import subprocess
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def decode_ss_url(ss_url):
    match = re.match(r"ss://(.+)@(.+):(\d+)/?", ss_url)
    if match:
        encoded_part = match.group(1)
        server = match.group(2)
        port = match.group(3)
        decoded_part = base64.urlsafe_b64decode(encoded_part).decode("utf-8")
        method, password = decoded_part.split(":")
        return {
            "server": server,
            "port": int(port),
            "cipher": method,
            "password": password,
        }
    return None


def create_proxy_config(proxy, index):
    return {
        "name": f"My SS Proxy {index+1}",
        "type": "ss",
        "server": proxy["server"],
        "port": proxy["port"],
        "cipher": proxy["cipher"],
        "password": proxy["password"],
        "udp": True,
        "plugin": "",
        "plugin-opts": {},
    }


def update_proxy_groups(config, proxy_names):
    # Update the existing "Proxy" group
    for group in config["proxy-groups"]:
        if group["name"] == "Proxy":
            group["proxies"] = proxy_names
            break
    else:
        # If "Proxy" group doesn't exist, create it
        config["proxy-groups"].append(
            {"name": "Proxy", "type": "select", "proxies": proxy_names}
        )


def _get_file_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    print(f"File path: {file_path}")
    return file_path


def generate_clash_config(ss_urls):
    # Decode Shadowsocks URLs
    proxies = []
    for ss_url in ss_urls:
        ss_url = ss_url.strip()
        if ss_url:
            proxy_config = decode_ss_url(ss_url)
            if proxy_config:
                proxies.append(proxy_config)

    if not proxies:
        logger.error("No valid SS URLs found in config file")
        return None

    logger.info(f"Found {len(proxies)} valid SS proxies")

    # Read existing config.yaml
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    with open(_get_file_path("clash_config_tmp.yaml"), "r") as file:
        config = yaml.load(file)

    # Create proxy configurations
    proxy_configs = [create_proxy_config(proxy, i) for i, proxy in enumerate(proxies)]
    proxy_names = [proxy["name"] for proxy in proxy_configs]

    # Update config
    config["proxies"] = proxy_configs
    update_proxy_groups(config, proxy_names)

    # Write updated config.yaml
    logger.info("Writing updated config...")
    output_file_path = _get_file_path("clash_config.yaml")
    with open(output_file_path, "w") as file:
        yaml.dump(config, file)

    logger.info("Config update completed")
    return output_file_path


def generate_ss_urls_file(ss_urls):
    output_file_path = _get_file_path("ss_urls.txt")
    with open(output_file_path, "w") as file:
        for ss_url in ss_urls:
            file.write(ss_url + "\n")
    logger.info("Generated ss_urls.txt")
    return output_file_path


def generate_ss_config():
    output_file_path = _get_file_path("ss.conf")
    logger.info("Generated ss.conf")
    return output_file_path


def upload_file(bucket_name, source_file, destination_blob_name):
    if source_file is None:
        logger.error("Source file is None, skipping upload")
        return None

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.cache_control = "no-cache"
    blob.upload_from_filename(source_file)
    blob.make_public()

    url = f"https://storage.googleapis.com/{bucket_name}/{destination_blob_name}"
    logger.info(f"Uploaded {source_file} to {url}")
    return url


def main():
    with open(_get_file_path("app_config.yaml"), "r") as f:
        config = YAML().load(f)

    bucket_name = config["bucket_name"]
    ss_urls = config["ss_urls"]

    if len(ss_urls) == 1:
        ss_urls.append(ss_urls[0])
    elif len(ss_urls) != 2:
        raise ValueError("app_config.yaml must contain exactly 2 SS URLs")

    logger.info("Generating Clash config...")
    clash_config_file = generate_clash_config(ss_urls)

    logger.info("Generating ss_urls.txt...")
    ss_urls_file = generate_ss_urls_file(ss_urls)

    logger.info("Generating ss.conf...")
    ss_config_file = generate_ss_config()

    logger.info("Uploading config files...")
    yaml_url = upload_file(bucket_name, clash_config_file, "clash_config.yaml")
    ss_urls_url = upload_file(bucket_name, ss_urls_file, "ss_urls.txt")
    ss_config_url = upload_file(bucket_name, ss_config_file, "ss.conf")
    logger.info("Upload completed")


if __name__ == "__main__":
    main()
