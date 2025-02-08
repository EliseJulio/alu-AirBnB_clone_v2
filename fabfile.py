#!/usr/bin/python3
"""Fabric script that distributes an archive to web servers"""
from fabric import Connection
from fabric import task
from os.path import exists

# Define the servers
hosts = ["54.85.169.157", "54.227.112.222"]
user = "ubuntu"
key_path = "~/.ssh/id_rsa"

@task
def do_deploy(c, archive_path):
    """Deploys an archive to web servers"""
    if not exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        path_name = f"/data/web_static/releases/{name}"

        # Connect to each server and execute commands
        for host in hosts:
            conn = Connection(host=host, user=user, connect_kwargs={"key_filename": key_path})

            conn.put(archive_path, "/tmp/")
            conn.run(f"mkdir -p {path_name}/")
            conn.run(f"tar -xzf /tmp/{file_name} -C {path_name}/")
            conn.run(f"rm /tmp/{file_name}")
            conn.run(f"mv {path_name}/web_static/* {path_name}")
            conn.run(f"rm -rf {path_name}/web_static")
            conn.run("rm -rf /data/web_static/current")
            conn.run(f"ln -s {path_name}/ /data/web_static/current")

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

