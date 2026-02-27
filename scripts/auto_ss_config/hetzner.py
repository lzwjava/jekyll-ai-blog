from hcloud import Client
import os
import time
import argparse
import sys

# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Hetzner Cloud server snapshot and clone tool"
)
parser.add_argument(
    "--create-snapshot", action="store_true", help="Create snapshots of servers"
)
parser.add_argument(
    "--create-server",
    action="store_true",
    help="Create servers from existing snapshots",
)
parser.add_argument(
    "--snapshot-id", type=str, help="Specific snapshot ID to use when creating a server"
)
parser.add_argument(
    "--server-name",
    type=str,
    help="Server name to operate on (optional, all servers if not specified)",
)
args = parser.parse_args()

# If no action specified, show help and exit
if not (args.create_snapshot or args.create_server):
    parser.print_help()
    sys.exit(0)

# Get the API token from the environment variable
api_token = os.environ.get("HERTZNER_API_KEY")

if not api_token:
    print("Error: HERTZNER_API_KEY environment variable not set.")
    exit(1)

# Create a client instance
client = Client(token=api_token)


def create_snapshot(server):
    try:
        print(f"Creating snapshot for server {server.name}...")
        # Create the snapshot directly - the API will handle any locking issues
        response = client.servers.create_image(
            server, description=f"{server.name}-snapshot", type="snapshot"
        )
        print(f"Snapshot created for server {server.name} with ID: {response.image.id}")
        return response.image
    except Exception as e:
        if "locked" in str(e).lower():
            print(f"Server {server.name} is locked. Please try again later.")
        else:
            print(f"Error creating snapshot for server {server.name}: {e}")
        return None


def create_server_from_snapshot(snapshot_id, source_server, new_name=None):
    try:
        if new_name is None:
            new_name = f"{source_server.name}-clone"

        # Get the server type and location from the source server
        server_type = source_server.server_type
        datacenter = source_server.datacenter

        print(f"Waiting for snapshot (ID: {snapshot_id}) to be available...")

        # Wait for the snapshot to be available
        max_attempts = 20
        attempts = 0
        snapshot = None

        while attempts < max_attempts:
            try:
                # Try to get the image
                snapshot = client.images.get_by_id(snapshot_id)
                print(f"Snapshot status: {snapshot.status}")

                # Only proceed when the snapshot is actually available
                if snapshot.status == "available":
                    print(f"Snapshot is now fully ready to use")
                    break

                print(
                    f"Snapshot found but status is '{snapshot.status}', waiting for 'available' status..."
                )
            except Exception as e:
                print(
                    f"Attempt {attempts+1}/{max_attempts}: Snapshot not accessible yet: {e}"
                )

            # Increment attempts and wait regardless of error or not-ready status
            attempts += 1
            if attempts < max_attempts:
                sleep_time = 20  # Wait longer between attempts
                print(
                    f"Waiting {sleep_time} seconds before retrying (attempt {attempts}/{max_attempts})..."
                )
                time.sleep(sleep_time)

        if snapshot is None or snapshot.status != "available":
            print("Failed to get a ready snapshot after multiple attempts")
            return None

        print(f"Creating new server '{new_name}' from snapshot (ID: {snapshot_id})")
        print(f"  - Using server type: {server_type.name}")
        print(
            f"  - Using datacenter: {datacenter.name} (location: {datacenter.location.name})"
        )

        # Create the new server using the snapshot as the image
        response = client.servers.create(
            name=new_name,
            server_type=server_type,
            image=snapshot,
            datacenter=datacenter,
            start_after_create=True,
        )

        print(f"New server created with ID: {response.server.id}")
        print(f"Root password: {response.root_password}")
        return response.server
    except Exception as e:
        print(f"Error creating server from snapshot: {e}")
        return None


# Get all servers
servers = client.servers.get_all()

# Filter servers if server_name is specified
if args.server_name:
    servers = [s for s in servers if s.name == args.server_name]
    if not servers:
        print(f"Error: No server found with name '{args.server_name}'")
        sys.exit(1)

# Print server details
for server in servers:
    print(f"Server ID: {server.id}")
    print(f"Server Name: {server.name}")
    print(f"Server Status: {server.status}")
    print(f"Server IPv4: {server.public_net.ipv4.ip}")
    print(f"Server IPv6: {server.public_net.ipv6.ip}")
    print(f"Server Type: {server.server_type.name}")
    print(f"Server Location: {server.datacenter.location.name}")
    print("----------------------------------")

# Create snapshots if requested
if args.create_snapshot:
    print("\n=== Creating Snapshots ===\n")
    for server in servers:
        snapshot = create_snapshot(server)
        if snapshot and args.create_server:
            # Create a new server from the snapshot if both flags are set
            new_server = create_server_from_snapshot(snapshot.id, server)

# Create servers from existing snapshot if requested
if args.create_server and args.snapshot_id and not args.create_snapshot:
    print("\n=== Creating Server from Existing Snapshot ===\n")
    # Use the first server as template for the new server
    snapshot = None
    try:
        snapshot = client.images.get_by_id(args.snapshot_id)
        print(f"Found snapshot with ID {args.snapshot_id}")
    except Exception as e:
        print(f"Error: Could not find snapshot with ID {args.snapshot_id}: {e}")
        sys.exit(1)

    if snapshot and servers:
        new_server = create_server_from_snapshot(args.snapshot_id, servers[0])
