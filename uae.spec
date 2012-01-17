%define Werror_cflags %nil
%define name		uae
%define mversion	0.8.29
%define fversion	20081130
%define release		0.%{fversion}.%mkrel 1
%define cdrname		cdrecord
%define cdrmainvers	1.9
%define cdrvers 	%{cdrmainvers}a05

# For building with SCSI support
%define build_scsi 1
%{?_with_scsi: %global build_scsi 1}
%{?_without_scsi: %global build_scsi 0}

Summary: A software emulation of the Amiga system
Name: %{name}
Version: %{mversion}
Release: %{release}
URL: http://www.rcdrummond.net/uae
Source0: http://www.rcdrummond.net/uae/uae-%{mversion}.tar.bz2
Source1: ftp://ftp.berlios.de/pub/cdrecord/alpha/%{cdrname}-%{cdrvers}.tar.bz2
License: GPL
Group: Emulators
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: XFree86-devel
BuildRequires: gtk+-devel
BuildRequires: glib-devel cdrkit
BuildRequires: SDL-devel

%description
UAE is a software emulation of the Amiga system hardware, which
enables you to run most available Amiga software.  Since it is a
software emulation, no extra or special hardware is needed.  The Amiga
hardware is emulated accurately, so that Amiga software is tricked
into thinking it is running on the real thing.  Your computer's
display, keyboard, hard disk and mouse assume the roles of their
emulated counterparts.

Note that to fully emulate the Amiga you need the Amiga KickStart ROM
images, which are copyrighted and, of course, not included here.


%prep
%setup -q -a 1 -n uae-%{mversion}

%build
%if %build_scsi
# build libscg for scsi-device support
(cd %{cdrname}-%{cdrmainvers}
ln -sf i586-linux-cc.rul RULES/ia64-linux-cc.rul
ln -sf i586-linux-cc.rul RULES/x86_64-linux-cc.rul
ln -sf i586-linux-cc.rul RULES/amd64-linux-cc.rul
ln -sf i686-linux-cc.rul RULES/athlon-linux-cc.rul
pwd
CFLAGS="$RPM_OPT_FLAGS" \
CONFFLAGS="%{_target_platform} --prefix=%{_prefix}" \
	XL_ARCH=%{_target_cpu} ./Gmake)
(cd src
./install_libscg ../%{cdrname}-%{cdrmainvers})
%endif

# build uae
CFLAGS="-O2 -fomit-frame-pointer" \
./configure --prefix=%{_prefix} \
            --with-x \
            --with-sdl \
            --with-sdl-sound \
            --with-sdl-gfx \
            --enable-threads \
            --enable-ui \
	    --enable-jit \
%if %build_scsi
            --enable-scsi-device \
%else
            --disable-scsi-device \
%endif
	    --enable-bsdsock
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}/{bin,lib/uae/amiga/source}
%makeinstall
cp -pR amiga/* %{buildroot}/%{_libdir}/uae/amiga/.

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc docs/*
%{_bindir}/*
%{_libdir}/uae
%doc docs/*
%{_datadir}/uae/configs/a1200.uae
%{_datadir}/uae/configs/a4000.uae
%{_datadir}/uae/configs/a500-expanded.uae
%{_datadir}/uae/configs/a500.uae
%{_datadir}/uae/configs/a500plus.uae
%{_datadir}/uae/configs/poweruser.uae


