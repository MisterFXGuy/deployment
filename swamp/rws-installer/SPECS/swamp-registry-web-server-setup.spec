#
# spec file for SWAMP directory server setup installation RPM
# On install, this RPM will 
# 1) save a copy of the current /etc/httpd/conf.d and /etc/httpd/modsecurity.d folders in /opt/swamp 
# 2) Replace /etc/httpd/conf.d and /etc/httpd/modsecurity.d with SWAMP supplied versions of those folders.
# On uninstall, this RPM will 
# 1) Remove SWAMP versions of /etc/httpd/conf.d and /etc/httpd/modsecurity.d 
# 2) Restore the copies of the current /etc/httpd/conf.d and /etc/httpd/modsecurity.d folders from /opt/swamp 
#
%define is_darwin %(test -e /Applications && echo 1 || echo 0)
%if %is_darwin
%define _topdir	 	/Users/dboulineau/Projects/cosa/trunk/swamp/src/main/deployment/swamp/installer
%define nil #
%define _rpmfc_magic_path   /usr/share/file/magic
%define __os Linux
%endif
%define _arch noarch

%define _target_os Linux
# Leave our files alone
%define __jar_repack 0
%define __os_install_post %{nil}


Summary: Registry Web Server installation for Software Assurance Marketplace (SWAMP) 
Name: swamp-registry-web-server-setup
Version: %(perl -e 'print $ENV{RELEASE_NUMBER}')
Release: %(perl -e 'print $ENV{BUILD_NUMBER}')
License: Apache 2.0
Group: Development/Tools
Source: swamp-setup.tar
URL: http://www.continuousassurance.org
Vendor: The Morgridge Institute for Research
Packager: Support <support@continuousassurance.org>
BuildRoot: /tmp/%{name}-buildroot
BuildArch: noarch
Requires: httpd,mod_security_crs,php,mod_ssl
Conflicts: swamp-rt-perl,swamp-exec,swamp-submit,swamp-csaweb
AutoReqProv: no

%description
A state-of-the-art facility designed to advance our nation's cybersecurity by improving the security and reliability of open source software.
This RPM contains the Registry Web Server setup package (Apache configs).

%prep
%setup -c -q

%build
echo "Here's where I am at build $PWD"
#cd ../BUILD/%{name}-%{version}
%install
echo rm -rf $RPM_BUILD_ROOT
echo "At install i am $PWD"
%if %is_darwin
cd %{name}-%{version}
%endif

mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
mkdir -p $RPM_BUILD_ROOT/etc/httpd/modsecurity.d
mkdir -p $RPM_BUILD_ROOT/opt/swamp
mkdir -p $RPM_BUILD_ROOT/var/www/html/scripts
cp -r apache $RPM_BUILD_ROOT/opt/swamp

cp html/scripts/version.js $RPM_BUILD_ROOT/opt/swamp

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root, root)
/opt/swamp

%pre

if [ "$1" = "1" ] 
then
    mkdir -p /opt/swamp
    /bin/tar -C /etc/httpd/conf.d -czf /opt/swamp/conf.d.tar.gz .
    /bin/tar -C /etc/httpd/modsecurity.d -czf /opt/swamp/modsecurity.d.tar.gz .
fi

%post
# If this is the first time this RPM has been installed...
    # One time allow upgrading of RPM which will do normal installation AND update version
if [ "$1" = "1" -o "$1" = "2" ] 
then
    /bin/rm -rf /etc/httpd/conf.d/* /etc/httpd/modsecurity.d/*
    cp -r /opt/swamp/apache/conf.d /etc/httpd
    cp -r /opt/swamp/apache/modsecurity.d /etc/httpd
	cp /etc/httpd/conf.d/ssl.conf /etc/httpd/conf.d/ssl.conf.bak
    sed -e's/SSLEngine.*$/SSLEngine off/' -e 's/^\s\{0,\}SSLCertificateFile/##SSLCertificateFile/' -e's/^\s\{0,\}SSLCertificateKeyFile/##SSLCertificateKeyFile/' -e's/^\s\{0,\}SSLCACertificateFile/##SSLCACertificateFile/' /etc/httpd/conf.d/ssl.conf > tmp.conf && mv tmp.conf /etc/httpd/conf.d/ssl.conf
    sed -e's/SSLEngine.*$/SSLEngine off/' -e 's/^\s\{0,\}SSLCertificateFile/##SSLCertificateFile/' -e's/^\s\{0,\}SSLCertificateKeyFile/##SSLCertificateKeyFile/' -e's/^\s\{0,\}SSLCACertificateFile/##SSLCACertificateFile/' /etc/httpd/conf.d/ssl_port8443.conf > tmp.conf && mv tmp.conf /etc/httpd/conf.d/ssl_port8443.conf
    sed -e's/SSLEngine.*$/SSLEngine off/' -e 's/^\s\{0,\}SSLCertificateFile/##SSLCertificateFile/' -e's/^\s\{0,\}SSLCertificateKeyFile/##SSLCertificateKeyFile/' -e's/^\s\{0,\}SSLCACertificateFile/##SSLCACertificateFile/' /etc/httpd/conf.d/ssl_port443.conf > tmp.conf && mv tmp.conf /etc/httpd/conf.d/ssl_port443.conf
    # One time allow upgrading of RPM which will do normal installation 
    if [ "$1" = "2" ] 
    then
        cp /opt/swamp/version.js /var/www/html/scripts
    fi
fi
echo The following changes need to be made to the HTTP configuration files:
echo 1. Install SSL Certificates
echo 2. Set SSLEngine on
echo 3. Set ServerName to CommonName used in SSL Certificate

%preun
# If this is an uninstallation, arg 1 will be 0
if [ "$1" = "0" ] 
then
    # Remove our files from /etc/httpd
    /bin/rm -rf /etc/httpd/conf.d/* /etc/httpd/modsecurity.d/*
    # Restore original files
    /bin/tar -C /etc/httpd/conf.d -xzf /opt/swamp/conf.d.tar.gz 
    /bin/tar -C /etc/httpd/modsecurity.d -xzf /opt/swamp/modsecurity.d.tar.gz 
    /bin/rm -f /opt/swamp/modsecurity.d.tar.gz /opt/swamp/conf.d.tar.gz 
fi
