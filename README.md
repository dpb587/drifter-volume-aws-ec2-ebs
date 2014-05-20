Tool for managing drifting volumes on AWS.


## Vagrant

    AWS_VAGRANT_IAM_PROFILE_NAME=safetest \
    vagrant up --provider aws


## Example

**create**

    R0=$( aws --region us-east-1 ec2 create-volume --size 1 --availability-zone $( aws --region us-east-1 ec2 describe-instances --instance-id `cat .vagrant/machines/default/aws/id` | jq -r '.Reservations[0].Instances[0].Placement.AvailabilityZone' ) )
    VOLUME_ID=$( echo "$R0" | jq -r '.VolumeId' )

**attach**

    vagrant ssh -c "cd /vagrant ; sudo -E ./bin/run.py --env-file /tmp/volume.env -vv attach '$VOLUME_ID'"

**usage**

    vagrant ssh -c ". /tmp/volume.env ; mkdir -p /tmp/mountme ; sudo mkfs -t ext4 \$MOUNT_DEVICE ; sudo mount \$MOUNT_DEVICE /tmp/mountme ; sudo chown ubuntu:ubuntu /tmp/mountme ; date >> /tmp/mountme/verify.txt ; cat /tmp/mountme/verify.txt ; sudo umount /tmp/mountme"

**detach**

    vagrant ssh -c "cd /vagrant ; sudo -E ./bin/run.py -vv detach '$VOLUME_ID'"

**destroy**

    R1=$( aws --region us-east-1 ec2 delete-volume --volume-id "$VOLUME_ID" )


## Docker

    sudo docker build -t dpb587/drifter-volume-aws-ec2-ebs .


## systemd

**service** - `media-vol00f21745-drifter.service`

    [Service]
    RemainAfterExit=yes
    ExecStart=/usr/bin/docker run -v /media/drifter:/docker-mnt dpb587/drifter-volume-aws-ec2-ebs --env-file /docker-mnt/vol00f21745.mount.env attach vol-00f21745
    ExecStop=/usr/bin/docker run dpb587/drifter-volume-aws-ec2-ebs detach vol-00f21745


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
