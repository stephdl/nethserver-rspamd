Summary: NethServer rspamd configuration
Name: nethserver-mail-filter
Version: 0.2.1
Release: 1%{?dist}
License: GPL
URL: %{url_prefix}/%{name} 
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
Requires: rspamd
Requires: nethserver-antivirus
Requires: nethserver-mail-server
Requires: nethserver-dnsmasq, nethserver-unbound
Requires: nethserver-redis

BuildRequires: perl
BuildRequires: nethserver-devtools 

%description
Rspamd is an advanced spam filtering system that allows evaluation of messages
by a number of rules including regular expressions, statistical analysis and
custom services such as URL black lists. Each message is analysed by Rspamd
and given a spam score.

%prep
%setup

%build
perl createlinks

%install
rm -rf %{buildroot}
mkdir -p root/var/run/clamd.rspamd
(cd root; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} \
  --dir /var/run/clamd.rspamd 'attr(0750,_rspamd,_rspamd)' \
> %{name}-%{version}-filelist
echo "%doc COPYING" >> %{name}-%{version}-filelist

%post
/usr/bin/systemctl enable rspamd
/usr/bin/systemctl start rspamd
%preun

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update

%changelog

* Sat Dec 02 2017 stephane de Labrusse <stephdl@de-labrusse.fr>
- initial
