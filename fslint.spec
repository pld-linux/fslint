Summary:	Utility to find and clean "lint" on a filesystem
Name:		fslint
Version:	2.42
Release:	1
License:	GPL
Group:		Applications/File
Source0:	http://www.pixelbeat.org/fslint/%{name}-%{version}.tar.gz
# Source0-md5:	a22a27dc9c8474ba58d770ebf8529d9c
Source1:	%{name}.desktop
Patch0:		%{name}.patch
URL:		http://www.pixelbeat.org/fslint/
BuildRequires:	gettext-devel >= 0.13
BuildRequires:	python-devel >= 2.3
BuildRequires:	python-pygtk-devel >= 2.4
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
Requires:	coreutils
Requires:	cpio
Requires:	gettext >= 0.11.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
fslint is a toolkit to find all redundant disk usage (for example
duplicated files).

This package includes collection of utilities to find lint on a
filesystem:
- findup -- find DUPlicate files
- findnl -- find Name Lint (problems with filenames)
- findu8 -- find filenames with invalid utf8 encoding
- findbl -- find Bad Links (various problems with symlinks)
- findsn -- find Same Name (problems with clashing names)
- finded -- find Empty Directories
- findid -- find files with dead user IDs
- findns -- find Non Stripped executables
- findrs -- find Redundant Whitespace in files
- findtf -- find Temporary Files
- findul -- find possibly Unused Libraries
- zipdir -- Reclaim wasted space in ext2 directory entries

%package gui
Summary:	fslint GUI
Group:		X11/Applications
Requires:	fslint
Requires:	python >= 2.0
Requires:	python-pygtk-glade

%description gui
fslint is a toolkit to find all redundant disk usage (for example
duplicated files).

This package includes the GUI.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e '
	# remove script_dir variable setting
	/script_dir=/,/script_dir=/d;

	# find* programs are in $PATH
	s,"$script_dir"/find,find,

	# replace $script_dir with real path
	s,"$script_dir",%{_datadir}/fslint,
' fslint/{find??,fslint,zipdir}

%{__perl} -pi -e 's|^liblocation=.*$|liblocation="%{_datadir}/%{name}" #RPM edit|' fslint-gui
%{__perl} -pi -e 's|^locale_base=.*$|locale_base=None #RPM edit|' fslint-gui
%{__perl} -pi -e 's|liblocation\+"/fslint/|liblocation+"/|' fslint-gui
%{__perl} -pi -e 's|"./find|"find|' fslint-gui

%build
%{__make} -C po

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_pixmapsdir},%{_desktopdir},%{_mandir}/man1,%{_datadir}/fslint}
install fslint-gui $RPM_BUILD_ROOT%{_bindir}/fslint-gui

install fslint.glade $RPM_BUILD_ROOT%{_datadir}/fslint
install fslint_icon.png $RPM_BUILD_ROOT%{_datadir}/fslint
ln -s %{_datadir}/fslint/fslint_icon.png $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

cp -a fslint/{find??,fslint,zipdir} $RPM_BUILD_ROOT%{_bindir}
cp -a fslint/{fstool,supprt} $RPM_BUILD_ROOT%{_datadir}/fslint

install man/fslint-gui.1 $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} -C po install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_bindir}/findbl
%attr(755,root,root) %{_bindir}/finded
%attr(755,root,root) %{_bindir}/findid
%attr(755,root,root) %{_bindir}/findnl
%attr(755,root,root) %{_bindir}/findns
%attr(755,root,root) %{_bindir}/findrs
%attr(755,root,root) %{_bindir}/findsn
%attr(755,root,root) %{_bindir}/findtf
%attr(755,root,root) %{_bindir}/findu8
%attr(755,root,root) %{_bindir}/findul
%attr(755,root,root) %{_bindir}/findup
%attr(755,root,root) %{_bindir}/fslint
%attr(755,root,root) %{_bindir}/zipdir

%dir %{_datadir}/fslint
%dir %{_datadir}/fslint/fstool
%attr(755,root,root) %{_datadir}/fslint/fstool/dir_size
%attr(755,root,root) %{_datadir}/fslint/fstool/dupwaste
%attr(755,root,root) %{_datadir}/fslint/fstool/edu
%attr(755,root,root) %{_datadir}/fslint/fstool/lS

%dir %{_datadir}/fslint/supprt
%attr(755,root,root) %{_datadir}/fslint/supprt/fslver
%attr(755,root,root) %{_datadir}/fslint/supprt/getffl
%attr(755,root,root) %{_datadir}/fslint/supprt/getffp
%attr(755,root,root) %{_datadir}/fslint/supprt/getfpf
%attr(755,root,root) %{_datadir}/fslint/supprt/md5sum_approx

%dir %{_datadir}/fslint/supprt/rmlint
%attr(755,root,root) %{_datadir}/fslint/supprt/rmlint/fix_ws.sh
%attr(755,root,root) %{_datadir}/fslint/supprt/rmlint/fixdup
%attr(755,root,root) %{_datadir}/fslint/supprt/rmlint/fixdup.sh
%attr(755,root,root) %{_datadir}/fslint/supprt/rmlint/merge_hardlinks
%attr(755,root,root) %{_datadir}/fslint/supprt/rmlint/view_ws.sh

%files gui -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fslint-gui
%{_mandir}/man1/fslint-gui.1*
%{_desktopdir}/fslint.desktop
%{_datadir}/fslint/fslint.glade
%{_datadir}/fslint/fslint_icon.png
%{_pixmapsdir}/fslint_icon.png
