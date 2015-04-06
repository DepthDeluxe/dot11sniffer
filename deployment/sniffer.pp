$proot = '/home/sniffer/dot11sniffer'

user { 'sniffer':
  ensure        => present,
  shell         => '/bin/nologin',
}

package { 'python2':
  ensure => installed,
}

package { 'python2-pip':
  ensure => installed,
}
exec { 'pip-install':
  command => 'pip2 install netifaces',
}

package { 'scapy':
  ensure => installed,
}

package { 'aircrack-ng':
  ensure => installed,
}

# service files for the sniffer
file { '/etc/systemd/system/dot11sniffer.service':
  ensure => file,
  source => "${proot}/deployment/dot11sniffer.service",
  owner  => root,
  group  => root,
}
service { 'dot11sniffer':
  require => [ File['/etc/systemd/system/dot11sniffer.service'],
               Service['dot11monitor'],
               Package['python2'],
               Package['scapy'],
               Exec['pip-install'],
               User['sniffer'], ],

  ensure => running,
  enable => true,
}

# service file to create the monitor interface
file { '/etc/systemd/system/dot11monitor.service':
  ensure => file,
  source => "${proot}/deployment/dot11monitor.service",
  owner  => root,
  group  => root,
}
service { 'dot11monitor':
  require => [ File['/etc/systemd/system/dot11monitor.service'],
               Package['aircrack-ng'] ],

  ensure => running,
  enable => true,
}
