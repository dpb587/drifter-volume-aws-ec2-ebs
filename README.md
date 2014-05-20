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


## systemd

**service** - `media-vol00f21745-drifter.service`

    [Service]
    RemainAfterExit=yes
    ExecStart=/usr/bin/docker run -v /media/drifter:/docker-mnt dpb587/scs-drifter-volume-aws-ec2-ebs --remap-device ubuntu --env-file /docker-mnt/vol00f21745.mount.env attach vol-00f21745
    ExecStop=/usr/bin/docker run dpb587/scs-drifter-volume-aws-ec2-ebs detach vol-00f21745


**mount** - `media-vol00f21745.mount`

    [Unit]
    Requires=media-vol00f21745-drifter.service

    [Mount]
    EnvironmentFile=/media/drifter/vol00f21745.mount.env
    What=$MOUNT_DEVICE
    Where=/media/vol00f21745
    Type=ext4

    [X-Fleet]
    X-ConditionMachineOf=media-vol00f21745-drifter.service


## License

[MIT License](./LICENSE)
