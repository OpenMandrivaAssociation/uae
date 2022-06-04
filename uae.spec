Summary: A software emulation of the Amiga system
Name: uae
Version: 3.1.66
Release: 1
URL: https://fs-uae.net/download#source
Source0: https://fs-uae.net/files/FS-UAE/Stable/%{version}/fs-uae-%{version}.tar.xz
Patch0: fs-uae-3.0.5-compile.patch
License: GPLv2
Group: Emulators
Provides: fs-uae = %{EVRD}

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
%autosetup -p1 -n fs-uae-%{version}

%build
# build uae
%configure \
            --with-x \
            --with-sdl \
            --with-sdl-sound \
            --with-sdl-gfx \
            --enable-threads \
            --enable-ui \
	    --enable-jit \
            --enable-scsi-device \
	    --enable-bsdsock
%make_build

%install
%make_install
%find_lang fs-uae

%files -f fs-uae.lang
%defattr(-,root,root)
%{_bindir}/fs-uae
%{_bindir}/fs-uae-device-helper
%{_datadir}/applications/fs-uae.desktop
%{_datadir}/fs-uae
%{_datadir}/icons/*/*/*/fs-uae.*
%{_datadir}/mime/packages/fs-uae.xml
%doc %{_docdir}/fs-uae
