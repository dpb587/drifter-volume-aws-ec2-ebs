Tool for managing drifting AWS EBS volumes.


## Vagrant

    vagrant up --provider aws

## Example

**attach**

    sudo -E ./bin/run.py --remap-device ubuntu --env-file /tmp/mount.env -vvv attach vol-00f21745

**usage**

    . /tmp/mount.env
    mkdir -p /tmp/mountme
    sudo mount $MOUNT_DEVICE /tmp/mountme

**detach**

    sudo -E ./bin/run.py -vvv detach vol-00f21745


## Docker

    sudo docker build -t dpb587/scs-drifter-volume-aws-ec2-ebs .


## License

[MIT License](./LICENSE)
