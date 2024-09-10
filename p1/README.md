# P1 (6% of grade): Counting Pop Songs in Spotify Dataset with Dockerized Shell Script

## Overview

In this project, you'll setup your programming environment for the
first part of the semester (virtual machine, Docker).  You'll practice
writing some shell commands to download a zipped file and search
(grep) through its contents.  You'll automate these steps with a shell
script.  The shell script may depend on other programs (like `unzip`),
so you'll deploy it as a Docker image with the necessary installs.

Learning objectives:
* deploy a virtual machine in the cloud
* follow a complicated series of steps to install Docker
* write a shell script to automate several bash commands
* bundle a shell script up as a Docker image/container

Before starting, please review the [general project directions](../projects.md).

## Part 1: Virtual Machine Setup

We'll use Google's Cloud (GCP) for our virtual machines.  They've
generously given each 639 student $100 in credits, which should last
the whole semester if you remember to __suspend__ (don't delete it!) your VM when not using it.

You can obtain the credits here: https://canvas.wisc.edu/courses/425476/pages/google-credits.

Setup a virtual machine that you'll use for the first few projects
(we'll eventually delete it and create a more powerful one for some of
the later projects).

You should have some experience in creating VMs in a prior course (320
or 400), so these directions will be brief:

* Go to https://console.cloud.google.com/compute/instances to view and launch VMs.
* Click "Create a VM", and use the following settings.
  - Machine type: `e2-small`
  - Boot disk: `Ubuntu 22.04 LTS` (select x86/64 version, not Arm64) with disk size `25GB`.
  - You can decide things like what geographic region to create it in (I picked Iowa since it's nearby).
* Once you select these settings, the monthly estimate should be about $14.73 for the VM (if it’s not, you probably selected something wrong, and might run out of free credits before the end of the semester).
* Click "Create".
* You'll need to setup an SSH key so you can connect from your laptop--the browser-based SSH client won't work for what we need to do in this class.
  - [Install](https://cloud.google.com/sdk/docs/install) and initialize gcloud CLI. (I personally used conda: ``conda install google-cloud-sdk -c conda-forge``).
  - Follow instructions in "Connect to VMs" section to automatically generate an SSH key and connect to your VM: https://cloud.google.com/compute/docs/connect/standard-ssh#connect_to_vms.
  - Your SSH key should now be visible at https://console.cloud.google.com/compute/metadata?tab=sshkeys.

When you're done, check that you have the correct Operating System and
CPU with `cat /etc/os-release` and `lscpu`.  Save the outputs to hand in too:

``` 
cat /etc/os-release > os.txt
lscpu > cpu.txt
```

## Part 2: Docker Install

Carefully follow the directions here to install Docker 24.0.5 and Compose 2.20.2 on your virtual machine: https://docs.docker.com/engine/install/ubuntu/

Notes:
* There are several different approaches described under "Installation methods".  Use the directions under "Install using the apt repository".  Make sure you don't keep going after you reach "Install from a package"
* The first step under "Install Docker Engine" has two options: "Latest" or "Specific version".  Choose **"Specific version"**
* Here are the versions we will be using and the command to install them:
  * docker-ce: `5:24.0.5-1~ubuntu.22.04~jammy`
  * docker-ce-cli: `5:24.0.5-1~ubuntu.22.04~jammy`
  * docker-compose-plugin: `2.20.2-1~ubuntu.22.04~jammy`
  
  ```
  sudo apt-get install docker-ce=5:24.0.5-1~ubuntu.22.04~jammy docker-ce-cli=5:24.0.5-1~ubuntu.22.04~jammy containerd.io docker-buildx-plugin docker-compose-plugin=2.20.2-1~ubuntu.22.04~jammy
  ```

To avoid needing to run every Docker command with root, there are a
few more steps you can do here:
https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user
(don't go beyond the "Manage Docker as a non-root user" section).

Create some more files so we can check your Docker install:

```
docker version > docker.txt
docker compose version > compose.txt
```

## Part 3: Shell Script

This zip file contains a CSV file with data on all songs that were on the Top 200 Global Weekly charts of Spotify in 2020 and 2021: https://ms.sites.cs.wisc.edu/cs639/data/spotify.zip.

Try running some shell commands to download the zip, extract the
contents, and __print how many songs contain the genre "pop"__. Make sure you're only counting the word "pop" (direct match) and not "k-pop", "uk pop", etc. It's OK for a song to have multiple genres, as long as "pop" is included.

Now, combine these commands in a `count.sh` file; the script should
have a shebang line so that the following runs with bash:

```sh
./count.sh
```

Make sure your .sh file is executable!

We will now create a docker image so you can copy over and execute this script inside your container.

## Part 4: Docker Image with MySQL installation

Create a `Dockerfile` that starts from base image `Ubuntu:24.04`, installs `MySQL`, and copies over and executes `count.sh`. __The Dockerfile should also do any installs needed to run `count.sh`__.

Once you've created the `Dockerfile`, you should be able to create an image and container like this:

```
docker build . -t p1
docker run p1
```

It's OK if there's extra output besides the actual count.

## Submission

At a minimum, your submission repo (see below section) should contain the following: `os.txt`, `cpu.txt`,
`docker.txt`, `compose.txt`, `count.sh`, `Dockerfile`.

### Github classroom

* Invitation to join [github classroom](https://classroom.github.com/a/uVWrRr1y).
* Search for name and join the classroom by clicking on it
* If you cannot find your name, please contact Sachi Sanghavi: sachi at cs dot wisc dot edu
* **Just for project 1, we want everyone to make individual submissions**
* Create a team name:
  * I recommend using this format: p<id>_<github_username>. For example, my team name would be *p1_msyamkumar*. 
  * Team names are publicly visible, so please use appropriate team names
* Refresh until the repo is ready
* Visit the repo, and clone it to your VM - happy coding!

## Tester

Copy `autograde.py` and `../tester.py` to your working directory 
then run `python3 autograde.py` to test your work and environment setup.
The test result will be written to a `test.json` file in your directory. 
This will probably be your grade, but autograders are imperfect, so we
reserve the right to deduct further points.  Some cases are when
students achieve the correct output by hardcoding, or not using an
approach we specifically requested.
