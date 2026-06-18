%global commit1 fdd8867333016a479b66dcb3ec9de5eaf54b9adb
%global name1 cbang
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
# Bundled boost version
%global boostver 1.63.0

Name:           camotics
Version:        1.1.1
Release:        15%{?dist}
Summary:        Open-Source Simulation & Computer Aided Machining - A 3-axis CNC GCode simulator

# Licenses in order: camotics / cbang / boost, clipper / libevent
License:        GPLv2+ and LGPLv2+ and Boost and BSD
URL:            http://camotics.org/
Source0:        https://github.com/CauldronDevelopmentLLC/CAMotics/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/CauldronDevelopmentLLC/cbang/archive/%{commit1}.tar.gz#/%{name1}-%{shortcommit1}.tar.gz
Source2:        camotics.xml
Source3:        CAMotics.appdata.xml

# https://github.com/CauldronDevelopmentLLC/CAMotics/issues/214
Patch0:         camotics-fix-misleading-indentation.patch
# Backported patches to use system libraries
Patch1:         camotics-0001-Use-system-cairo-if-present.patch
Patch2:         camotics-0002-Allow-using-system-GLEW.patch
Patch3:         camotics-0003-Use-system-dxflib-and-move-dxf-to-3rdparty-location.patch
Patch4:         camotics-Use-memcpy-instead-of-strncpy-and-ensure-null-termin.patch

BuildRequires:  bzip2-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(dxflib)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(re2)
BuildRequires:  pkgconfig(QtCore)
BuildRequires:  pkgconfig(QtGui)
BuildRequires:  pkgconfig(QtOpenGL)
BuildRequires:  scons
BuildRequires:  sqlite-devel
BuildRequires:  v8-314-devel

# Boost currently builds only from cbang sources. Since commit 97e5ae8 no
# longer an option. CAMotics depends on cbang-boost static library.
Provides:       bundled(boost-iostreams) = %{boostver}
Provides:       bundled(boost-filesystem) =  %{boostver}
Provides:       bundled(boost-system) =  %{boostver}
Provides:       bundled(boost-regex) =  %{boostver}
# Cbang is currently not designed to be packaged separately. There are several
# issue like static libraries and sharing scons config with CAMotics.
Provides:       bundled(cbang)
# cbang requires at least libevent 2.1.2 for event_base_loopcontinue
Provides:       bundled(libevent) = 2.1.4

# No matching package to install: 'v8-314-devel'
ExcludeArch:    aarch64 ppc64le s390x
# v8-314-devel available for ppc64 starting from Fedora 26
%if 0%{?fedora} < 26
ExcludeArch:    ppc64
%endif

%description
CAMotics is an Open-Source software which can simulate
3-axis NC machining. It is a fast, flexible and user friendly simulation
software for the DIY and Open-Source community.

At home manufacturing is one of the next big technology revolutions. Much like
the PC was 30 years ago. There have been major advances in desktop 3D printing
(e.g.  Maker Bot) yet uptake of desktop CNCs has lagged despite the
availability of cheap CNC machines. One of the major reasons for this is a
lack of Open-Source simulation and CAM (model to tool path conversion)
software. CAM and NC machine simulation present some very difficult
programming problems as evidenced by 30+ years of academic papers on these
topics. Whereas 3D printing simulation and tool path generation is much
easier. However, such software is essential to using a CNC.

Being able to simulate is a critical part of creating usable CNC tool paths.
Programming a CNC with out a simulator is cutting with out measuring; it's
both dangerous and expensive. With CAMotics you can preview the results of
your cutting operations before you fire up your machine. This will
save you time and money and open up a world of creative possibilities by
allowing you to rapidly visualize and improve upon designs without wasting
material or breaking tools.


%prep
%setup -T -qb1 -n %{name1}-%{commit1}

# https://github.com/CauldronDevelopmentLLC/cbang/issues/18
%autosetup -n CAMotics-%{version} -p1
for file in $(grep -Rl --include=SConscript -- '-Werror' src/ 2>/dev/null); do
  sed -i "s/\.replace('-Werror', '')/\nflags = re.sub(r'-Werro([^\\\s]+|r)', '', flags)/" $file
  sed -i '1iimport re' $file
done


%build
export CBANG_HOME=%{_builddir}/%{name1}-%{commit1}
# re2 from system uses c++11 features (GH cbang #22)
%global _scopts cxxstd=c++11 debug=1 strict=0 disable_local="bzip2 expat re2 sqlite3 zlib" %{?_smp_mflags}
# C! does not work with newer version of v8 that Fedora supplies.
# https://github.com/CauldronDevelopmentLLC/cbang/issues/17
# 'unnecessary parentheses in declaration' as warnings (GH cbang #26)
%global _ccflags %{?fedora:-I%{_includedir}/v8-3.14/} %{optflags} -Wno-error=parentheses

cd %{_builddir}/%{name1}-%{commit1}
# Bundled boost uses auto_ptr (GH cbang #23)
scons ccflags="%{_ccflags} -Wno-deprecated-declarations" %{_scopts} \
      linkflags="%{?__global_ldflags}"

cd %{_builddir}/CAMotics-%{version}
scons ccflags="%{_ccflags}" %{_scopts} \
      linkflags="%{?__global_ldflags}"


%install
export CBANG_HOME=%{_builddir}/%{name1}-%{commit1}
scons install ccflags="%{_ccflags}" %{_scopts} install_prefix=%{buildroot}/usr \
              linkflags="%{?__global_ldflags}"

install -d -m 0755 %{buildroot}%{_datadir}/applications
# https://github.com/CauldronDevelopmentLLC/CAMotics/issues/213
desktop-file-install --add-mime-type="application/x-camotics-project" \
                     --set-key="Exec" --set-value="camotics %f" \
                     --add-mime-type="application/x-camotics-nc" CAMotics.desktop

# https://github.com/CauldronDevelopmentLLC/CAMotics/issues/211
install -d -m 0755 %{buildroot}%{_datadir}/mime/packages
install -p -m 0644 %{SOURCE2} %{buildroot}/%{_datadir}/mime/packages

install -d -m 0755 %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
install -p -m 0644 images/camotics.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/

install -d -m 0755 %{buildroot}%{_datadir}/%{name}
cp -pr tpl_lib/ %{buildroot}/%{_datadir}/%{name}

install -d -m 0755 %{buildroot}%{_docdir}/%{name}
cp -pr examples/ %{buildroot}%{_docdir}/%{name}

# https://github.com/CauldronDevelopmentLLC/CAMotics/pull/236
install -d -m 0755 %{buildroot}%{_datadir}/appdata
install -p -m 0644 %{SOURCE3} %{buildroot}/%{_datadir}/appdata

# Convert files with DOS line endings to Unix
find "%{buildroot}%{_datadir}" -not -type d -exec file {} \; \
     | grep CRLF | cut -f1 -d: | while read -r dosfile; do
       sed -i $'s/\r$//' $dosfile; done

# Remove executable bit from executable files in datadir
find "%{buildroot}%{_datadir}" -executable -type f -exec chmod -x {} \;


%check
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.appdata.xml


%files
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/128x128/apps/*
%{_datadir}/mime/packages/%{name}.xml
%{_docdir}/%{name}/*
%license COPYING LICENSE
%doc CHANGELOG.md README.md


%changelog
* Sun Feb 03 2019 Samuel Rakitničan <samuel.rakitnican@gmail.com> - 1.1.1-15
- Backport upstream fix for GCC 9
- Don't use -Werror option when compiling

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 23 2018 Nicolas Chauvet <kwizart@gmail.com> - 1.1.1-14
- Rebuilt for glew 2.1.0

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 1.1.1-12
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Sun Feb 18 2018 Samuel Rakitničan <samuel.rakitnican@gmail.com> 1.1.1-11
- Update cbang to fdd8867 with fixes for GCC 8

* Wed Feb 14 2018 Samuel Rakitničan <samuel.rakitnican@gmail.com> 1.1.1-10
- GCC's 8 'unnecessary parentheses in declaration' as warning
- Pass the Fedora hardening flags for the linker

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 04 2018 Samuel Rakitničan <samuel.rakitnican@gmail.com>
- Remove post/postun/posttrans scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 06 2017 Samuel Rakitničan <samuel.rakitnican@gmail.com> 1.1.1-7
- Upgrade cbang to b35fa09 with ARM fix included
- Re-enable armv7hl for all platforms and ppc64 for F26 and newer

* Wed Jul 05 2017 Samuel Rakitničan <samuel.rakitnican@gmail.com> 1.1.1-6
- Disable building on aarch64, armv7hl, ppc64, ppc64le and s390x

* Mon Jun 12 2017 Samuel Rakitničan <samuel.rakitnican@gmail.com>
- Update cbang to aba85ac
- Drop cbang support for OpenSSL since upstream now allows it - not necessary
  for CAMotics

* Fri Jun 02 2017 Samuel Rakitničan <samuel.rakitnican@gmail.com> 1.1.1-5
- Add missing bzip2-devel build requirement for epel
- Use desktop object type for AppStream to be compatible with epel

* Thu Jun 01 2017 Samuel Rakitničan <samuel.rakitnican@gmail.com> 1.1.1-4
- Reuse common compiler flags and build options from global variables
- Include AppStream Metadata

* Wed May 31 2017 Samuel Rakitničan <samuel.rakitnican@gmail.com>
- Backport a patch to unbundle dxflib
- Remove boost build dependency, no longer an option
- Unbundle re2
- Make sure bzip2, expat, re2, sqlite3 and zlib are unbundled
- Correct License tag according to bundled libraries

* Fri May 26 2017 Samuel Rakitničan <samuel.rakitnican@gmail.com> 1.1.1-3
- Update cbang to 7f96da9 (GH issues 18, 21)
- Use system Cairo and GLEW

* Wed May 24 2017 Samuel Rakitničan <samuel.rakitnican@gmail.com> 1.1.1-2
- Do not strip binary manually
- Try once more with debug build
- Patch to fix misleading-indentation error with debug build
- Update cbang, fixes compilation error with optflags
- Comment unusual procedures
- Add Provides bundle(cbang)
- Add gcc-c++ build requirement
- Correct license tag
- Fix line-endings and remove executable bit from datadir files

* Fri Mar 17 2017 Samuel Rakitničan <samuel.rakitnican@gmail.com>
- Drop non-required mariadb-devel build dependecy
- Convert qt-devel and openssl-devel build dependecy into pkgconfig modules

* Wed Mar  8 2017 Samuel Rakitničan <samuel.rakitnican@gmail.com> 1.1.1-1
- Initial build
