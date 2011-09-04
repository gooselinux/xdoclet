# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define _without_maven 1

%define gcj_support 0

# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'
%define with_maven %{!?_without_maven:1}%{?_without_maven:0}
%define without_maven %{?_without_maven:1}%{!?_without_maven:0}

# FIXME: Fedora lacks webwork and xwork, needed for the demo
%define _without_demo 1

# If you do not want to build samples in demo subpackage because of their 
# runtime deps, give rpmbuild option '--without demo'
%define with_demo %{!?_without_demo:1}%{?_without_demo:0}

Name:           xdoclet
Version:        1.2.3
Release:        11.6%{?dist}
Epoch:          0
Summary:        XDoclet Attribute Orientated Programming Framework
License:        BSD       
Group:          Development/Framework
URL:            http://xdoclet.sourceforge.net
Source0:        http://superb-east.dl.sourceforge.net/sourceforge/xdoclet/xdoclet-src-1.2.3.tgz 
#Source1:        %{name}-modules-objectweb-4.6.tgz
Patch0:         xdoclet-build_xml.patch
Patch1:         xdoclet-XDocletModulesEjbMessages.patch
Patch2:         xdoclet-ant.not-required.patch
Patch3:         xdoclet-WebLogicSubTask.patch
Patch4:         xdoclet-project_xml.patch
Patch5:         xdoclet-AbstractProgramElementTagsHandler.patch
Patch6:         xdoclet-build_docs_xml.patch

%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  java-devel >= 0:1.4.2
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-nodeps >= 0:1.5
BuildRequires:  ant-trax
%if %{with_maven}
BuildRequires:  maven >= 0:1.1
%endif
BuildRequires:  junit
BuildRequires:  javacc
BuildRequires:  jrefactory
BuildRequires:  bsf 
BuildRequires:  jakarta-commons-collections 
BuildRequires:  jakarta-commons-lang 
BuildRequires:  jakarta-commons-logging 
BuildRequires:  jakarta-commons-net 
BuildRequires:  log4j
%if %{with_demo}
BuildRequires:  struts 
%endif
BuildRequires:  velocity 
BuildRequires:  xalan-j2 >= 0:2.7.0
BuildRequires:  xml-commons-apis 
BuildRequires:  xjavadoc >= 0:1.1

Requires:  bsf
Requires:  jakarta-commons-collections
Requires:  jakarta-commons-logging
Requires:  log4j
Requires:  velocity
Requires:  xalan-j2 >= 0:2.7.0
Requires:  xml-commons-apis
Requires:  xjavadoc = 0:1.1

%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
Requires(post):         java-gcj-compat
Requires(postun):       java-gcj-compat
%endif

%description
This package contains the XDoclet Attribute Orientated Programming Framework

%if %{with_demo}
%package demo
Summary:        XDoclet Sample Projects
Group:          Development/Framework
BuildRequires:  servletapi4
BuildRequires:  struts
BuildRequires:  velocity
BuildRequires:  webwork >= 0:2.1
BuildRequires:  xwork
BuildRequires:  geronimo-ejb-2.1-api
BuildRequires:  myfaces
BuildRequires:  geronimo-jms-1.1-api
BuildRequires:  mx4j
Requires:  %{name} = %{version}-%{release}
Requires:  geronimo-ejb-2.1-api
Requires:  myfaces
Requires:  geronimo-jms-1.1-api
Requires:  webwork
Requires:  xwork
Requires:  mx4j
Requires:  struts
Requires:  servletapi4

%description demo
This package contains sample XDoclet projects.
%endif

%if %{with_maven}
%package maven-plugin
Summary:        XDoclet Maven Plugin
Group:          Development/Framework
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       maven >= 0:1.1

%description maven-plugin
%{summary}.
%endif

%package javadoc
Summary:        XDoclet Javadoc
Group:          Development/Documentation

%description javadoc
This package contains XDoclet javadoc

%package manual
Summary:        XDoclet Sample Manuals and Documentation
Group:          Development/Documentation

%description manual
This package contains XDoclet documentation.

%prep
%setup -q
# Remove binary information in the source tar
find . -name "*.jar" -exec rm {} \;
find . -name "*.class" -exec rm {} \;

# Replace JOnAS specific tasks with code blessed by ObjectWeb
#pushd modules
#mv objectweb objectweb.orig
#tar xzf %{SOURCE1}
#popd

# Remove mockobjects support.
rm -rf modules/mockobjects

for j in xjavadoc-1.1 jrefactory javacc junit bsf commons-collections commons-logging log4j velocity xalan-j2 xjavadoc xml-commons-apis; do
        ln -s $(build-classpath $j) lib
done

%if %{with_demo}
for j in servletapi4 struts velocity webwork-migration xwork geronimo-ejb-2.1-api myfaces/myfaces-jsf-api geronimo-jms-1.1-api; do
        ln -s $(build-classpath $j) samples/lib
done
for j in mx4j/mx4j-jmx mx4j/mx4j-tools; do
        i=$(build-classpath $j)
        ln -s $(build-classpath $j) samples/lib
done
%endif

%patch0 -b .sav
%patch1 -b .sav
%patch2 -b .sav 
%patch3 -b .sav
%patch4 -b .sav
%patch5 -b .sav
%patch6 -b .sav

%build
export MAVEN_HOME=/usr/share/maven
export MAVEN_LOCAL_HOME=$(pwd)/.maven
%if %{with_maven}
ant -Dbuild.sysclasspath=first core modules maven docs l10n
%else
ant -Dbuild.sysclasspath=first core modules docs l10n
%endif
%if %{with_demo}
ant samples
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_javadir}/%{name}
install -m 644 target/lib/xdoclet*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}
%if %{with_maven}
install -m 644 target/lib/maven-xdoclet*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}
%endif
(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%if %{with_demo}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr samples/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
%endif

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rm -rf target/docs/api

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr target/docs/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 

%if %{gcj_support}
%{_bindir}/aot-compile-rpm 
%endif

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(-, root, root, -)
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/%{name}*.jar
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/LICENSE.txt

%if %{gcj_support}
%attr(-,root,root) %dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-apache-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-bea-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-borland-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-caucho-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-ejb-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-exolab-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-hibernate-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-hp-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-ibm-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-java-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-jboss-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-jdo-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-jmx-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-jsf-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-libelis-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-macromedia-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-mvcsoft-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-mx4j-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-objectweb-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-openejb-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-oracle-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-orion-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-portlet-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-pramati-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-solarmetric-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-spring-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-sun-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-sybase-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-tjdo-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-web-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-webwork-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-wsee-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-xdoclet-module-1.2.3.jar.*
%endif

%if %{with_maven}
%files maven-plugin
%defattr(-, root, root, -)
%{_javadir}/%{name}/maven-%{name}*.jar
%endif

%if %{with_demo}
%files demo
%defattr(-, root, root, -)
%{_datadir}/%{name}-%{version}
%endif

%files javadoc
%defattr(-, root, root, -)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files manual
%defattr(-, root, root, -)
%doc %{_docdir}/%{name}-%{version}

%changelog
* Tue Feb 09 2010 Andrew Overholt <overholt@redhat.com> 0:1.2.3-11.6
- Conditionalize struts BR (with_demo).
- Don't build gcj support.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:1.2.3-11.5
- Rebuilt for RHEL 6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.3-11.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.3-10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 05 2008 Matt Wringe <mwringe@redhat.com> - 0:1.2.3-9.4
- Update xdoclet-ant.not-required.patch to apply with fuzz=0.

* Fri Aug 29 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0:1.2.3-9.3
- include /usr/share/doc/xdoclet-1.2.3 directory

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.2.3-9.2
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.2.3-9jpp.1
- Autorebuild for GCC 4.3

* Wed Apr 25 2007 Matt Wringe <mwringe@redhat.com> - 0:1.2.3-8jpp.1
- Merge with newest jpp version
- Fix some rpm lint warnings

* Tue Apr 11 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0:1.2.3-7jpp.3
- Remove mockobjects requirements.

* Wed Mar 07 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.2.3-8jpp
- Optionally build without maven
- Separate out maven-xdoclet-plugin into own subpackage
- Reactivate demo, now that webwork and xwork are available
- No native xdoclet-maven-plugin


* Fri Aug 04 2006 Matt Wringe <mwringe at redhat.com> - 0:1.2.3-7jpp.2
- Rebuild with define with_gcj_support

* Thu Aug 03 2006 Matt Wringe <mwringe at redhat.com> - 0:1.2.3-7jpp.1
- Merge with upstream version
- Remove unnecessary define with_gcj_support
- Add missing javadoc requires
- Add missing javadoc postun

* Wed Jul 26 2006 Matt Wringe <mwringe at redhat.com> - 0:1.2.3-6jpp_4fc
- Remove xalan-j2 and xalan-j2-serializer from the ant OPT_JAR_LIST

* Mon Jul 23 2006 Matt Wringe <mwringe at redhat.com> - 0:1.2.3-6jpp_3fc
- Rebuild on new gcj

* Sun Jul 23 2006 Matt Wringe <mwringe at redhat.com> - 0:1.2.3-6jpp_2fc
- Rebuild

* Sat Jul 22 2006 Matt Wringe <mwringe at redhat.com> - 0:1.2.3-6jpp_1fc
- Merge with upstream version
- Remove dependency on maven, use ant instead
- Natively compile jpackages

* Sat Jul 22 2006 Matt Wringe <mringe at redhat.com> - 0:1.2.3-6jpp
- Add conditional native compiling
- Add missing buildrequires: ant-nodeps and ant-trax
- Add missing javadoc %%ghost symlink

* Thu Jun 08 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.2.3-5jpp
- Update objectweb module to match JOnAS 4.6.x
- Build without demo because JPP 1.7 lacks webwork and xwork

* Thu Jun 08 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.2.3-4jpp
- Patch AbstractProgramElementTagsHandler to sort members, 
  Thx Jesus Rodriguez

* Thu Apr 06 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.2.3-3jpp
- Replace non-free (B)Rs in -demo with free ones

* Tue Feb 21 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.2.3-2jpp
- Adapt project.xml (docs) to maven-1.1

* Tue Dec 20 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.2.3-1jpp
- Upgrade to 1.2.3
- Build docs with maven

* Fri Sep 23 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.2.2-3jpp
- Adapt to build samples with webwork-2.1.7

* Fri Mar 04 2005 Fernando Nasser <fnasser@redhat.com> - 0:1.2.2-2jpp
- Add patch to prevent attempt to load DTD from the net, when it comes with
  the source and is locally available
- Replace JOnAS specific tasks with code blessed by ObjectWeb
- Do not save copies of the java files when patching.

* Tue Feb 15 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.2.2-1jpp
- Upgrade to 1.2.2
- Add jsf requirement for demo
- Drop jndi requirement for demo
- Drop servletapi and mx4j requirement for main package
- Buildrequire maven and use it to build docs

* Thu Aug 26 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.2.1-2jpp
- Build with ant-1.6.2

* Fri Jul 02 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.2.1-1jpp
- Upgrade to 1.2.1
- Relax build-time dependencies
- Relax dependency versions
- Make subpackage xdoclet-demo optional

* Fri Mar 05 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.2-1jpp
- First JPackage release.

