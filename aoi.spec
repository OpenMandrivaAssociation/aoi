%define name    aoi
%define version 2.8.1
%define release %mkrel 1
%define version_nodot 281 

Name:           %{name}
Version:        %{version}
Release:        %{release}

Summary:        3D modelling and rendering studio Written in Java
URL:            http://www.artofillusion.org
Group:          Graphics

Source0:        %{name}src%{version_nodot}.zip
Source1:        jmf-2_1_1e-alljava.zip
Patch0:         fix-build.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:        GPLv2+

BuildArch:      noarch

BuildRequires:  java-rpmbuild
BuildRequires:  ant
BuildRequires:  ant-nodeps
BuildRequires:  jogl
BuildRequires:  bsh
BuildRequires:  jama
BuildRequires:  dos2unix
BuildRequires:  buoy
BuildRequires:  xml-commons-apis
BuildRequires:  xerces-j2

Requires:       java >= 1.5
Requires:       bsh
Requires:       jogl
Requires:       jama
Requires:       gluegen
Requires:       buoy

%description
Art of Illusion is a free, open source 3D modelling and rendering studio.
Many of its capabilities rival those found in commercial programs.
Highlights include subdivision surface based modelling tools,
skeleton based animation, and a graphical language 
for designing procedural textures and materials.


%files
%defattr(644,root,root,755)
%doc LICENSE HISTORY README-source

%attr(755,root,root) %{_bindir}/%{name}
%attr(644,root,root) %{_datadir}/%{name}/ArtOfIllusion.jar
%attr(755,root,root) %{_datadir}/%{name}/Plugins
%attr(644,root,root) %{_desktopdir}/%{name}.desktop
%attr(644,root,root) %{_datadir}/pixmaps/%{name}.png

#--------------------------------------------------------------------

%prep
%setup -q -a1 -n AoIsrc%{version_nodot}
# We only use this jar for build, not inclued in %files.
mv JMF-2.1.1e/lib/jmf.jar .
%patch0 -p0

%build
export CLASSPATH="."
%ant -buildfile ArtOfIllusion.xml

%install
rm -rf $RPM_BUILD_ROOT

# Installs the jar
%__install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/Plugins
%__install -m 644 ArtOfIllusion.jar $RPM_BUILD_ROOT%{_datadir}/%{name}

# Install the script
cat > %{name} <<EOF
#!/bin/sh

AOI_CLASSPATH=/usr/share/java/buoy.jar:/usr/share/java/buoyx.jar:/usr/share/java/jama.jar:/usr/share/java/jogl.jar:/usr/share/java/bsh.jar:/usr/share/aoi/ArtOfIllusion.jar:/usr/share/java/gluegen.jar:

java -cp \$AOI_CLASSPATH artofillusion.ArtOfIllusion

EOF
%__install -dm 755 $RPM_BUILD_ROOT%{_bindir}
%__install -m 755 %{name} $RPM_BUILD_ROOT%{_bindir}

# convert win32 EOL to unix EOL
dos2unix LICENSE
dos2unix HISTORY
dos2unix README-source

# icons
%__install -d -m755 %{buildroot}%{_datadir}/pixmaps
%__install -m 644 HelpPlugin/AOIHelp/helpset/Overview/images/%{name}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

# desktopfile
%__install -d -m755 %{buildroot}%{_desktopdir}
cat > %{buildroot}%{_desktopdir}/%{name}.desktop << EOF
[Desktop Entry]
Name=Art of Illusion
GenericName=3D modelling and rendering studio
Comment=3D modelling and rendering studio Written in Java
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Multimedia-Graphics;Graphics;
EOF

%clean
rm -rf $RPM_BUILD_ROOT

