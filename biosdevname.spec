Name:		biosdevname
Version:	0.7.2
Release:	2%{?dist}
Summary:	Udev helper for naming devices per BIOS names

Group:		System Environment/Base
License:	GPLv2
URL:		http://linux.dell.com/files/%{name}
# SMBIOS only exists on these arches.  It's also likely that other
# arches don't expect the PCI bus to be sorted breadth-first, or of
# so, there haven't been any comments about that on LKML.
ExclusiveArch:	%{ix86} x86_64 ia64
Source0:	http://linux.dell.com/files/%{name}/%{name}-%{version}/%{name}-%{version}.tar.gz

BuildRequires:	pciutils-devel, zlib-devel
# to figure out how to name the rules file
BuildRequires:	udev
#To generate the configure script
BuildRequires:	autoconf
BuildRequires:	automake
# for ownership of /etc/udev/rules.d
Requires: udev

Patch0: biosdevname-0.6.1-rules.patch
Patch1: 0001-Place-udev-rules-to-usr-lib.patch
Patch2: 0001-Fix-use-after-free-of-fd.patch
Patch3: 0002-Ignore-naming-of-non-Ethernet-network-interfaces.patch
Patch4: 0003-Prevent-reading-of-VPD-DCM-strings-for-SRIOV-vfs.patch

%description
biosdevname in its simplest form takes a kernel device name as an
argument, and returns the BIOS-given name it "should" be.  This is necessary
on systems where the BIOS name for a given device (e.g. the label on
the chassis is "Gb1") doesn't map directly and obviously to the kernel
name (e.g. eth0).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
autoreconf -iv
#If configure script doesn't exist generate it with autogen script
[ -e ./configure ] || ./autogen.sh --no-configure

%configure --disable-rpath --prefix=%{_prefix} --sbindir=%{_prefix}/sbin
make %{?_smp_mflags}


%install
make install install-data DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_prefix}/sbin/%{name}
# hack for either /etc or /lib rules location
%{_prefix}/lib/udev/rules.d/*.rules
%{_mandir}/man1/%{name}.1*


%changelog
* Fri Mar 31 2017 Michal Sekletar <msekleta@redhat.com> - 0.7.2-2
- backport fixes from upstream (#1385889)

* Thu May 26 2016 Michal Sekletar <msekleta@redhat.com> - 0.7.2-1
- rebase to 0.7.2 (#1269524)

* Fri Dec 18 2015 Michal Sekletar <msekleta@redhat.com> - 0.7.0-1
- rebase to 0.7.0 (#1269524)

* Fri Jun 12 2015 Michal Sekletar <msekleta@redhat.com> - 0.6.2-1
- rebase to 0.6.2 (#1182849)

* Thu Jan 08 2015 Michal Sekletar <msekleta@redhat.com> - 0.6.1-2
- fix up incorrectly generated patch

* Fri Dec 05 2014 Michal Sekletar <msekleta@redhat.com> - 0.6.1-1
- rebase to 0.6.1 (#1145572)

* Tue Mar 18 2014 Michal Sekletar <msekleta@redhat.com> - 0.5.0-10
- rename Mellanox card correctly (#1067135)

* Thu Mar 06 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 0.5.0-9
- stop reading VPD data once VPD-R section has been read (#1054414)

* Fri Feb 28 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 0.5.0-8
- remove KERNEL!="eth*", GOTO="netdevicename_end" (#1069817)

* Mon Feb 10 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 0.5.0-7
- Change 71-biosdevname.rules to match rhel6 setup (#1054170)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.5.0-6
- Mass rebuild 2013-12-27

* Fri Sep 20 2013 Václav Pavlín <vpavlin@redhat.com> - 0.5.0-5
- Fix regression introduced by the addslot function
- CoverityScan fixes
- Place udev rules to /usr/lib rather than /lib
Resolves: rhbz#1008899

* Mon Sep 02 2013 Harald Hoyer <harald@redhat.com> 0.5.0-3
- not only NAME KERNEL=="eth*", but every ethernet device

* Tue Jul 30 2013 Václav Pavlín <vpavlin@redhat.com> - 0.5.0-2
- Update help and man pages to cover all possible arguments
Resolves: rhbz#949021

* Tue Jul 30 2013 Václav Pavlín <vpavlin@redhat.com> - 0.5.0-1
- Updating the sources to 0.5.0 version. Following are the changes:
- Change scan of SMBIOS slot <-> PCI methods, recurse to set SMBIOS slot field
- Save off secondary bus of PCI device for PCI tree traversal
- Add version number to biosdevname

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 14 2012 Václav Pavlín <vpavlin@redhat.com> - 0.4.1-3
- Source link update

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.4.1-1
- Fix autoconfig for Fedora systems
- Make sure that vpd scan only runs on Dell systems, also blacklist Atheros
  wireless cards which hang when vpd is read.
- Add fixes to biosdevname to support cards that export multiple network
  ports per PCI device (chelsio/mellanox).



* Thu May 3 2012 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.4.0-1
- Create detached signature
- Fix man page to use new naming convention
- Remove unused variables from Stephen Hemminger [shemminger@vyatta.com]
- Use Physical device for slot numbering for embedded SR-IOV cards
- Add tracking of ifindex to eths structure
- Fix naming for add-in network adapters when SMBIOS version is invalid
- Read VPD-R on Dell systems only

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct  4 2011 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.3.11-5
- Added automake as a build dependency

* Tue Oct  4 2011 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.3.11-4
- Added autoconf as a build dependency

* Tue Oct  4 2011 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.3.11-3
- Generating the configure script if it doesn't exist

* Tue Oct  4 2011 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.3.11-2
- Fixed the dir structure inside the archive

* Tue Oct  4 2011 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.3.11-1
- Updating the sources to 0.3.11 version. Following are the changes:
- Fix man page for PCI slot naming
- Fix clearing of buffer for NPAR/SRIOV naming
- Add --nopirq and --smbios options to manpage.
- Verify length of VPD on network device
- Close file handle on sysfs read
- Fix naming policy for NPAR devices.
  Match each PCI device to its VPD 'physical' device to get correct index
- Exclude  building on ia64 arch
- Add support functions for determining PCIE slot
- Scan full path to parent when getting PCIE slot
- Fix NPAR naming for add-in cards
- Don't display _vf suffix on NPAR devices with single function
- Fix PCIe/PIRQ slot mapping

* Thu Apr 21 2011 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.3.8-1
- Add changes to parse VPD structure for device mapping on NPAR devices
- Fix pathname
- Cleanup and comment NPAR code
- Fix debian packaging rules to regenerate configure script
- Change pciX to pX for shortened names for PCI add-on devices
- Fix manpage typo
- Delete CR-LF in script
- Change default signing key
- Add command line arguments for checking SMBIOS version and ignore $PIRQ.

* Thu Feb 17 2011 Matt Domsch <Matt_Domsch@dell.com> - 0.3.7-1
- drop dump_pirq, suggest use biosdecode instead
- don't use '#' in names, use 'p' instead, by popular demand
- properly look for SMBIOS, then $PIR, then recurse
- Add kernel command line parameter "biosdevname={0|1}" to turn off/on biosdevname
- Fix segfault when BIOS advertises zero sized PIRQ Routing Table
- Add 'bonding' and 'openvswitch' to the virtual devices list
- fail PIRQ lookups if device domain is not 0
- Don't suggest names if running in a virtual machine (Xen, KVM,
  VMware tested, but should work on others)
- Typo fixes

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Matt Domsch <Matt_Domsch@dell.com> - 0.3.6-1
- drop biosdevnameS, it's unused and fails to build on F15

* Tue Jan 25 2011 Matt Domsch <Matt_Domsch@dell.com> - 0.3.5-1
- install dump_pirq into /usr/sbin
- fix udev rule, skip running if NAME is already set
- move udev rule to /lib/udev/rules.d by default

* Thu Dec 16 2010 Matt Domsch <mdomsch@fedoraproject.org> - 0.3.4-1
- drop unnecessary explicit version requirement on udev
- bugfix: start indices at 1 not 0, to match Dell and HP server port designations
- bugfix: don't assign names to unknown devices
- bugfix: don't assign duplicate names

* Thu Dec  9 2010 Matt Domsch <Matt_Domsch@dell.com> - 0.3.3-1
- add back in use of PCI IRQ Routing Table, if info is not provided by
  sysfs or SMBIOS

* Thu Dec  2 2010 Matt Domsch <Matt_Domsch@dell.com> - 0.3.2-1
- fix for multi-port cards with bridges
- removal of code for seriously obsolete systems

* Sun Nov 28 2010 Matt Domsch <Matt_Domsch@dell.com> 0.3.1-1
- remove all policies except 'physical' and 'all_ethN'
- handle SR-IOV devices properly

* Wed Nov 10 2010 Matt Domsch <Matt_Domsch@dell.com> 0.3.0-1
- add --policy=loms, make it default
- read index and labels from sysfs if available

* Mon Jul 27 2009 Jordan Hargrave <Jordan_Hargrave@dell.com> 0.2.5-1
- fix mmap error checking

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue May 06 2008 Matt Domsch <Matt_Domsch@dell.com> 0.2.4-5
- use policy=all_names to find breakage

* Sun Feb 10 2008 Matt Domsch <Matt_Domsch@dell.com> 0.2.4-4
- rebuild for gcc43

* Fri Sep 21 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.4-3
- fix manpage entry in files
 
* Fri Sep 21 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.4-2
- rebuild with Requires: udev > 115-3.20070920git

* Fri Sep 21 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.4-1
- coordinate udev rules usage with udev maintainer
- fix crashes in pcmcia search, in_ethernet(), and incorrect command
  line parsing.

* Mon Aug 27 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.3-1
- eliminate libbiosdevname.*, pre and post scripts

* Fri Aug 24 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.2-1
- ExclusiveArch those arches with SMBIOS and PCI IRQ Routing tables
- eliminate libsysfs dependency, move app to / for use before /usr is mounted.
- build static

* Mon Aug 20 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.1-1
- initial release
