Summary: nethserver-rspamd is a module to integrate rspamd
%define name nethserver-rspamd
Name: %{name}
%define version 0.1.0
%define release 1
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
#Source1: http://rspamd.com/rspamd_statistics/bayes.spam.sqlite
#Source2: http://rspamd.com/rspamd_statistics/bayes.ham.sqlite
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
Requires: rspamd
Requires: nethserver-antivirus
Requires: nethserver-mail-server
Requires: nethserver-redis
BuildRequires: nethserver-devtools
BuildArch: noarch

%description
Rspamd is an advanced spam filtering system that allows evaluation of messages 
by a number of rules including regular expressions, statistical analysis and 
custom services such as URL black lists. Each message is analysed by Rspamd 
and given a spam score.

%changelog
* Sat Dec 02 2017 stephane de Labrusse <stephdl@de-labrusse.fr>
- initial

%prep

%setup

%build
%{makedocs}
perl createlinks

%install
rm -rf $RPM_BUILD_ROOT
#mkdir -p root/var/lib/rspamd
#mv %{SOURCE1}  root/var/lib/rspamd/
#mv %{SOURCE2}  root/var/lib/rspamd/

(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist
%{genfilelist} $RPM_BUILD_ROOT \
> %{name}-%{version}-%{release}-filelist

%post
/usr/bin/systemctl enable rspamd
/usr/bin/systemctl start rspamd

%postun

%clean 
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%doc COPYING
