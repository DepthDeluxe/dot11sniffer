user { 'sniffer':
  ensure        => present,
  shell         => '/bin/nologin',
  groups        => ['colin'],
  managehome    => false,
}

package { 'python2':
  ensure => installed,
}

package { 'python2-pip':
  ensure => installed,
}

package { 'scapy':
  ensure => installed,
}

package { 'aircrack-ng':
  ensure => installed,
}

file { '/etc/systemd/system/dot11sniffer.service':
  ensure => file,
  source => './dot11sniffer.service',
  owner  => root,
  group  => root,
}
service { 'dot11sniffer':
  require => [ File['/etc/systemd/system/dot11sniffer.service'],
               Service['dot11monitor'],
               Package['python2'],
               Package['scapy'],
               User['sniffer'], ],

  ensure => running,
  enable => true,
}

file { '/etc/systemd/system/dot11monitor.service':
  ensure => file,
  source => './dot11monitor.service',
  owner  => root,
  group  => root,
}
service { 'dot11monitor':
  require => [ File['/etc/systemd/system/dot11monitor.service'],
               Package['aircrack-ng] ],

  ensure => running,
  enable => true,
}
