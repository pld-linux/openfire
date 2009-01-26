#
# TODO:
# - PLDize init script
# - PLDize at all...
Summary:	Openfire XMPP Server
Name:		openfire
Version:	3.6.3
Release:	0.1
# Source0 URL: http://www.igniterealtime.org/downloads/download-landing.jsp?file=openfire/openfire_src_3_6_3.tar.gz
Source0:	openfire_src_3_6_3.tar.gz
# Source0-md5:	914b4af58dab8e26c873c9ae8a2d72cd
Source1:	%{name}.sysconfig
Source2:	%{name}.init
License:	GPL
Group:		Applications/Communications
URL:		http://www.igniterealtime.org/
BuildRequires:	ant
BuildRequires:	java-sun
Requires:	java-sun
Requires:	java-sun-jre-X11
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
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/rc.d/init.d,%{_sysconfdir}/%{name},/etc/sysconfig,%{_datadir}/%{name},/var/log/%{name}}
# Copy over the main install tree.
cp -R target/openfire $RPM_BUILD_ROOT%{_datadir}
rm -rf  $RPM_BUILD_ROOT%{_datadir}/openfire/logs
# Set up the init script.
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/openfire
# Set up the sysconfig file.
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

# Symlinks for PLD
ln -s %{_datadir}/openfire/conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/resources
ln -s %{_datadir}/openfire/resources/security $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/resources
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/bin
ln -s %{_datadir}/openfire/bin/embedded-db.rc $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/bin
ln -s /var/log/openfire $RPM_BUILD_ROOT%{_datadir}/openfire/logs

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
%attr(755,root,root) %{_datadir}/openfire/bin/openfire.sh
%{_datadir}/openfire/bin/openfirectl
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/openfire/bin/embedded-db.rc
%{_datadir}/openfire/bin/embedded-db-viewer.sh
%dir %{_datadir}/openfire/conf
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/openfire/conf/openfire.xml
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
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/openfire/resources/security/keystore
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/openfire/resources/security/truststore
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/openfire/resources/security/client.truststore
%attr(754,root,root) /etc/rc.d/init.d/openfire
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/openfire
%attr(770,root,root) %dir %{_var}/log/%{name}
# Symlinks for PLD
%dir %{_sysconfdir}/openfire
%dir %{_sysconfdir}/openfire/bin
%{_sysconfdir}/openfire/bin/embedded-db.rc
%dir %{_sysconfdir}/openfire/conf
%dir %{_sysconfdir}/openfire/resources
%dir %{_sysconfdir}/openfire/resources/security
