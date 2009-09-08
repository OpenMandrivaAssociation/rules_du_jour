Summary:	This script updates SpamAssassin RuleSet files from the internet
Name:		rules_du_jour
Version:	1.30
Release:	%mkrel 4
License:	GPL
Group:		Networking/Mail
URL:		http://sandgnat.com/rdj/rules_du_jour
Source0:	http://sandgnat.com/rdj/rules_du_jour
Requires:	curl
Requires:	spamassassin
Requires:	spamassassin-spamd
Requires:	wget
BuildArch:	noarch
Buildroot:	%{_tmppath}/%{name}-%{version}-root

%description
This script updates SpamAssassin RuleSet files from the internet.

%prep

%setup -c -T -n %{name}-%{version}
cp %{SOURCE0} %{name}

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_sysconfdir}/cron.daily
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/mail/spamassassin/RulesDuJour

cat > RulesDuJour << EOF
TRUSTED_RULESETS="TRIPWIRE EVILNUMBERS SARE_RANDOM"
SA_DIR="%{_sysconfdir}/mail/spamassassin"
SA_RESTART="%{_initrddir}/spamd restart"
#SA_RESTART="svc -du /service/spamd /service/spamd/log"
EOF

install -m0755 %{name} %{buildroot}%{_sbindir}/
ln -s %{_sbindir}/%{name} %{buildroot}%{_sysconfdir}/mail/spamassassin/RulesDuJour/%{name}
ln -s %{_sbindir}/%{name} %{buildroot}%{_sysconfdir}/cron.daily/%{name}

install -m0644 RulesDuJour %{buildroot}%{_sysconfdir}/sysconfig/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %attr(0755,root,root) %{_sysconfdir}/mail/spamassassin/RulesDuJour
%config(noreplace) %{_sysconfdir}/sysconfig/RulesDuJour
%attr(0755,root,root) %{_sbindir}/%{name}
%attr(0755,root,root) %{_sysconfdir}/mail/spamassassin/RulesDuJour/%{name}
%attr(0755,root,root) %{_sysconfdir}/cron.daily/%{name}
