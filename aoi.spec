%define version_nodot 281 

Name:           aoi
Version:        2.8.1
Release:        4
Summary:        3D modelling and rendering studio Written in Java
URL:            http://www.artofillusion.org
Group:          Graphics

Source0:        %{name}src%{version_nodot}.zip
Source1:        jmf-2_1_1e-alljava.zip
Patch0:         fix-build.patch
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
BuildRequires:  locales-en

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
export LC_ALL=ISO-8859-1
export CLASSPATH="."
%ant -buildfile ArtOfIllusion.xml

%install
# Installs the jar
%__install -dm 755 %{buildroot}%{_datadir}/%{name}/Plugins
%__install -m 644 ArtOfIllusion.jar %{buildroot}%{_datadir}/%{name}

# Install the script
cat > %{name} <<EOF
#!/bin/sh

AOI_CLASSPATH=/usr/share/java/buoy.jar:/usr/share/java/buoyx.jar:/usr/share/java/jama.jar:/usr/share/java/jogl.jar:/usr/share/java/bsh.jar:/usr/share/aoi/ArtOfIllusion.jar:/usr/share/java/gluegen.jar:

java -cp \$AOI_CLASSPATH artofillusion.ArtOfIllusion

EOF
%__install -dm 755 %{buildroot}%{_bindir}
%__install -m 755 %{name} %{buildroot}%{_bindir}

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



%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 2.8.1-2mdv2011.0
+ Revision: 609981
- rebuild

* Mon Feb 15 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2.8.1-1mdv2010.1
+ Revision: 506020
- import aoi


* Fri Feb 12 2010 Jonathan Bayle <hide@mrhide.fr> 2.8.1-1mdv2010.0
- new package



