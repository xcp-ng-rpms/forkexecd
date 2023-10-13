%global package_speccommit 8ce13ac0825ac5b67d71ab8fec200e4004781171
%global package_srccommit v1.18.3
Version: 1.18.3
Release: 3.1%{?xsrel}%{?dist}
Name:           forkexecd
Summary:        A subprocess management service
License:        LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception
URL:            https://github.com/xapi-project/forkexecd
Source0: forkexecd-1.18.3.tar.gz
Source1: forkexecd.service
Source2: forkexecd-sysconfig
BuildRequires:  xs-opam-repo
BuildRequires:  ocaml-xcp-idl-devel
BuildRequires:  systemd-devel
#BuildRequires:  sudo

Requires:       jemalloc
%{?systemd_requires}

%description
A service which starts and manages subprocesses, avoiding the need to manually
fork() and exec() in a multithreaded program.

%global ocaml_dir    %{_opamroot}/ocaml-system
%global ocaml_libdir %{ocaml_dir}/lib
%global ocaml_docdir %{ocaml_dir}/doc
%global build_ocaml_dir %{buildroot}%{ocaml_dir}
%global build_ocaml_libdir %{buildroot}%{ocaml_libdir}
%global build_ocaml_docdir %{buildroot}%{ocaml_docdir}

%prep
%autosetup -p1

%build
make

# requires sudo which doesn't quite work without a terminal
#%check
#make test

%install
mkdir -p %{build_ocaml_libdir}
mkdir -p %{build_ocaml_docdir}
make install OPAM_PREFIX=%{build_ocaml_dir} OPAM_LIBDIR=%{build_ocaml_libdir} DESTDIR=%{buildroot} SBINDIR=%{_sbindir}
%{__install} -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/forkexecd.service
%{__install} -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/forkexecd

# this is to make opam happy
mkdir -p %{build_ocaml_libdir}/xapi-forkexecd
touch %{build_ocaml_libdir}/xapi-forkexecd/opam.config

%files
%{_sbindir}/forkexecd
%{_sbindir}/forkexecd-cli
%{_unitdir}/forkexecd.service
%config(noreplace) %{_sysconfdir}/sysconfig/forkexecd

%post
%systemd_post forkexecd.service

%preun
%systemd_preun forkexecd.service

%postun
%systemd_postun forkexecd.service

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       xs-opam-repo
Requires:       ocaml-xcp-idl-devel

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%files devel
%{ocaml_libdir}/xapi-forkexecd
%{ocaml_libdir}/forkexec
%{ocaml_docdir}/forkexec

%changelog
* Fri Oct 13 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.18.3-3.1
- Rebuild after sync with hotfix XS82ECU1049
- No source changes: only rebuild for dependencies
- *** Upstream changelog ***
- * Mon Oct 02 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 1.18.3-3
- - Bump release and rebuild

* Wed Aug 09 2023 Gael Duperrey <gduperrey@vates.fr> - 1.18.3-2.1
- Sync with hotfix XS82ECU1040
- *** Upstream changelog ***
- * Thu Jul 20 2023 Rob Hoes <rob.hoes@citrix.com> - 1.18.3-2
- - Bump release and rebuild
- * Mon Jun 19 2023 Christian Lindig <christian.lindig@citrix.com> - 1.18.3-1
- - Revert "CA-341921: avoid EINVAL errors for >1024 FDs"
- * Thu Jun 08 2023 Christian Lindig <christian.lindig@citrix.com> - 1.18.2-1
- - CA-341921: avoid EINVAL errors for >1024 FDs
- * Fri May 12 2023 Christian Lindig <christian.lindig@citrix.com> - 1.18.1-4
- - Bump release and rebuild
- * Fri May 12 2023 Christian Lindig <christian.lindig@citrix.com> - 1.18.1-3
- - Bump release and rebuild

* Fri Apr 14 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.18.1-2.1
- Sync with hotfix XS82ECU1027
- *** Upstream changelog ***
- * Thu Feb 23 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 1.18.1-2
- - Change license to match source
- - Remove macro for dependency generator

* Wed Oct 12 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.18.1-1.1
- Update as part of XAPI security update synced from XS82ECU1019
- *** Upstream changelog ***
- * Tue Aug 16 2022 Rob Hoes <rob.hoes@citrix.com> - 1.18.1-1
- - CP-34942: Make test compatible with dune 2.7+

* Wed Aug 17 2022 Gael Duperrey <gduperrey@vates.fr> - 1.18.0-3.2
- Rebuild for updated xenopsd from XS82ECU1011

* Mon Dec 20 2021 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.18.0-3.1
- Sync with CH 8.2.1
- *** Upstream changelog ***
- * Mon Sep 27 2021 Pau Ruiz Safont <pau.safont@citrix.com> - 1.18.0-3
- - Bump package after xs-opam update
- * Tue Jul 13 2021 Edwin Török <edvin.torok@citrix.com> - 1.18.0-2
- - bump packages after xs-opam update

* Thu Sep 02 2021 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.18.0-1.3
- Rebuild for updated message-switch from XS82E031

* Tue May 18 2021 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.18.0-1.2
- Rebuild for updated xs-opam-repo and ocaml-xcp-idl from XS82E020

* Thu Nov 05 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.18.0-1.1
- Rebuild for xs-opam-src 6.35.1 from XS82E002

* Fri Mar 06 2020 Christian Lindig <christian.lindig@citrix.com> - 1.18.0-1
- CA-336056: fix non-root forkhelpers
- Fix unit tests: lower max_fds
- Update Travis to use common config

* Fri Aug 23 2019 Edwin Török <edvin.torok@citrix.com> - 1.17.0-2
- bump packages after xs-opam update

* Thu Aug 15 2019 Christian Lindig <christian.lindig@citrix.com> - 1.17.0-1
- maintenance: use rpclib (#39)
- opam: use ppx_deriving_rpc (#40)

* Mon Apr 29 2019 Christian Lindig <christian.lindig@citrix.com> - 1.16.0-1
- CP-30037: use transient systemd units for spawning long-running processes

* Wed Jan 23 2019 Christian Lindig <christian.lindig@citrix.com> - 1.15.0-1
- Prepare for Dune 1.6
- Remove from Makefile: OPAM_LIBDIR, OPAM_PREFIX

* Tue Dec 04 2018 Christian Lindig <christian.lindig@citrix.com> - 1.14.0-1
- Moved from jbuilder to dune. DEprecated xcp in favour of xapi-idl.

* Wed Oct 31 2018 Christian Lindig <christian.lindig@citrix.com> - 1.13.0-1
- Update opam files for Opam 2

* Mon Sep 24 2018 Christian Lindig <christian.lindig@citrix.com> - 1.12.0-1
- CP-29470: Use a path on tmpfs for temporary sockets and files

* Tue Aug 21 2018 Christian Lindig <christian.lindig@citrix.com> - 1.11.0-1
- Simplify lib/jbuild

* Tue May 29 2018 Christian Lindig <christian.lindig@citrix.com> - 1.10.0-1
- fecomms: update and simplify interface using fd-send-recv >= 2.0.0

* Thu May 24 2018 Christian Lindig <christian.lindig@citrix.com> - 1.9.0-1
- lib/fecomms: make safe-string compliant

* Fri Mar 09 2018 Christian Lindig <christian.lindig@citrix.com> - 1.8.0-1
- CA-277850 Add fe_argv module for incrementally building argv

* Wed Feb 07 2018 Christian Lindig <christian.lindig@citrix.com> - 1.7.0-1
- jbuilder runtest: fix running sudo test, wait for socket to appear
- CA-282740: handle errors from execve in forkexecd

* Wed Jan 03 2018 Christian Lindig <christian.lindig@citrix.com> - 1.6.0-1
- Port to jbuilder, .travis+jbuild: run test with sudo
- Fix warnings, make reindent
- Split Stdext and port Xstringext -> Astring
- Remove unnecessary init.d-fe
- forkhelpers: add correct error message
- Makefile: remove gh-pages target

* Wed Dec 20 2017 Marcello Seri <marcello.seri@citrix.com> - 1.5.0-2
- Port to jbuilder

* Fri Jun 16 2017 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.5.0-1
- Sync opam file with xs-opam

* Fri May 12 2017 Rob Hoes <rob.hoes@citrix.com> - 1.4.0-1
- opam: update opam file and fix uninstall section

* Wed Mar 22 2017 Rob Hoes <rob.hoes@citrix.com> - 1.3.0-1
- .travis.yml: run "oasis setup" before "make"

* Mon Mar 13 2017 Marcello Seri <marcello.seri@citrix.com> - 1.2.1-2
- Update OCaml dependencies and build/install script after xs-opam-repo split

* Thu Mar 02 2017 Gabor Igloi <gabor.igloi@citrix.com> - 1.2.1-1
- Port to xs-opam-repo providing updated OCaml libraries:
  Use the new ppx-based rpclib
- Fixing the build step: oasis setup was missing

* Fri Feb 17 2017 Frederico Mazzone <frederico.mazzone@citrix.com> - 1.1.1-2
- CA-243676: Do not restart toolstack services on RPM upgrade

* Tue Jan 10 2017 Rob Hoes <rob.hoes@citrix.com> - 1.1.1-1
- git: Add metadata to the result of `git archive`

* Fri Sep 02 2016 Euan Harris <euan.harris@citrix.com> - 1.1.0-1
- Update to 1.1.0

* Mon Aug 22 2016 Rafal Mielniczuk <rafal.mielniczuk@citrix.com> - 1.0.1-2
- Package for systemd

* Fri Jul 22 2016 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.0.1-1
- Update to 1.0.1

* Mon May 16 2016 Si Beaumont <simon.beaumont@citrix.com> - 1.0.0-2
- Re-run chkconfig on upgrade

* Wed Apr 13 2016 Si Beaumont <simon.beaumont@citrix.com> - 1.0.0-1
- Update to 1.0.0
- Add build dependency on oasis

* Fri Jun 6 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.2-1
- Update to 0.9.2

* Wed Sep 25 2013 David Scott <dave.scott@eu.citrix.com> - 0.9.1-1
- Update to 0.9.1

* Fri May 31 2013 David Scott <dave.scott@eu.citrix.com>
- Initial package

