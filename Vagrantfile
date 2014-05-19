Vagrant.configure("2") do |config|
  config.vm.synced_folder ".", "/vagrant", type: "rsync"
  config.vm.provision :shell, :inline => "cd /vagrant ; ./bin/install.sh"

  config.vm.provider :aws do | aws, override |
    override.vm.box = "dummy-aws"
    override.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"

    aws.region = 'us-east-1'
    aws.ami = 'ami-018c9568' # aka ubuntu-14.04-x64

    aws.use_iam_profile = 'true' == ENV['AWS_VAGRANT_USE_IAM']
    aws.access_key_id = ENV['AWS_ACCESS_KEY_ID']
    aws.secret_access_key = ENV['AWS_SECRET_ACCESS_KEY']

    aws.iam_instance_profile_name = ENV['AWS_VAGRANT_IAM_PROFILE_NAME']
    aws.instance_type = 'c3.large'
    aws.keypair_name = ENV['AWS_KEYPAIR_NAME']
    aws.security_groups = [ 'vagrant' ]

    aws.tags = {
      'Environment' => 'dev',
      'Service' => "repo--scs-volume-aws-ec2-ebs",
      'Name' => "#{ENV['USER']}-#{File.basename(Dir.getwd)}",
    }

    override.ssh.username = 'ubuntu'
    override.ssh.private_key_path = ENV['AWS_PRIVATE_KEY_PATH']
  end
end

load "Vagrantfile.local" if File.exists? "Vagrantfile.local"
