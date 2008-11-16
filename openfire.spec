#
# TODO:
# - PLDize init script
# - PLDize at all...
Summary:	Openfire XMPP Server
Name:		openfire
Version:	3.6.1
Release:	0.1
# Source0 URL: http://www.igniterealtime.org/downloads/download-landing.jsp?file=openfire/openfire_src_3_6_0a.tar.gz
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	3dc742b91ea49a7fd33ec36f18b6f9dc
Source1:	%{name}.sysconfig
License:	GPL
Group:		Applications/Communications
URL:		http://www.igniterealtime.org/
BuildRequires:	ant
BuildRequires:	java-sun
Requires:	java-sun
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Openfire is a leading Open Source, cross-platform IM server based on
the XMPP (Jabber) protocol. It has great performance, is easy to setup
and use, and delivers an innovative feature set.

This particular release includes a bundled JRE.

%prep
%setup -q -n %{name}_src
cp %{SOURCE1} .

%if "%{_lib}" == "lib64"
%{__sed} -i -e 's/lib/lib64/' openfire.sysconfig
%endif

%build
cd build
%ant openfire
%ant -Dplugin=search plugin
cd ..

%install
rm -rf $RPM_BUILD_ROOT
# Prep the install location.
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/openfire
# Copy over the main install tree.
cp -R target/openfire $RPM_BUILD_ROOT%{_datadir}
# Set up the init script.
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install $RPM_BUILD_ROOT%{_datadir}/openfire/bin/extra/redhat/openfire $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/openfire
# Make the startup script executable.
chmod 755 $RPM_BUILD_ROOT%{_datadir}/openfire/bin/openfire.sh
# Set up the sysconfig file.
install -d $RPM_BUILD_ROOT/etc/sysconfig
install openfire.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/openfire
# Copy over the i18n files
cp -R resources/i18n $RPM_BUILD_ROOT%{_datadir}/openfire/resources/i18n
# Make sure scripts are executable
chmod 755 $RPM_BUILD_ROOT%{_datadir}/openfire/bin/extra/openfired
chmod 755 $RPM_BUILD_ROOT%{_datadir}/openfire/bin/extra/redhat-postinstall.sh
# Move over the embedded db viewer pieces
mv $RPM_BUILD_ROOT%{_datadir}/openfire/bin/extra/embedded-db.rc $RPM_BUILD_ROOT%{_datadir}/openfire/bin
mv $RPM_BUILD_ROOT%{_datadir}/openfire/bin/extra/embedded-db-viewer.sh $RPM_BUILD_ROOT%{_datadir}/openfire/bin
# We don't really need any of these things.
rm -rf $RPM_BUILD_ROOT%{_datadir}/openfire/bin/extra
rm -f $RPM_BUILD_ROOT%{_datadir}/openfire/bin/*.bat
rm -rf $RPM_BUILD_ROOT%{_datadir}/openfire/resources/nativeAuth/osx-ppc
rm -rf $RPM_BUILD_ROOT%{_datadir}/openfire/resources/nativeAuth/solaris-sparc
rm -rf $RPM_BUILD_ROOT%{_datadir}/openfire/resources/nativeAuth/win32-x86
rm -f $RPM_BUILD_ROOT%{_datadir}/openfire/lib/*.dll
rm -rf $RPM_BUILD_ROOT%{_datadir}/openfire/resources/spank

%clean
rm -rf $RPM_BUILD_ROOT

%preun
	/sbin/chkconfig --del openfire

%post
	/sbin/chkconfig --add openfire

%files
%defattr(644,root,root,755)
%doc README.html LICENSE.html changelog.html documentation/
%attr(750, daemon, daemon) %dir %{_datadir}/openfire
%dir %{_datadir}/openfire/bin
%{_datadir}/openfire/bin/openfire.sh
%{_datadir}/openfire/bin/openfirectl
%config(noreplace) %{_datadir}/openfire/bin/embedded-db.rc
%{_datadir}/openfire/bin/embedded-db-viewer.sh
%dir %{_datadir}/openfire/conf
%config(noreplace) %{_datadir}/openfire/conf/openfire.xml
%dir %{_datadir}/openfire/lib
%{_datadir}/openfire/lib/*.jar
%dir %{_datadir}/openfire/logs
%dir %{_datadir}/openfire/plugins
%{_datadir}/openfire/plugins/search.jar
%dir %{_datadir}/openfire/plugins/admin
%{_datadir}/openfire/plugins/admin/*
%dir %{_datadir}/openfire/resources
%dir %{_datadir}/openfire/resources/database
%{_datadir}/openfire/resources/database/*.sql
%dir %{_datadir}/openfire/resources/database/upgrade
%dir %{_datadir}/openfire/resources/database/upgrade/*
%{_datadir}/openfire/resources/database/upgrade/*/*
%dir %{_datadir}/openfire/resources/i18n
%{_datadir}/openfire/resources/i18n/*
%dir %{_datadir}/openfire/resources/nativeAuth
%dir %{_datadir}/openfire/resources/nativeAuth/linux-i386
%{_datadir}/openfire/resources/nativeAuth/linux-i386/*
%dir %{_datadir}/openfire/resources/security
%config(noreplace) %{_datadir}/openfire/resources/security/keystore
%config(noreplace) %{_datadir}/openfire/resources/security/truststore
%config(noreplace) %{_datadir}/openfire/resources/security/client.truststore
%attr(754,root,root) /etc/rc.d/init.d/openfire
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/openfire
