Name:           elastix
Version:        4.9.0
Release:        3%{?dist}
Summary:        A toolbox for rigid and nonrigid registration of images.

Group:          Applications/Engineering
License:        ASL 2.0
URL:            http://elastix.isi.uu.nl/
Source0:        https://github.com/SuperElastix/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  InsightToolkit-devel >= 4.13.0-6
BuildRequires:  gtest-devel
BuildRequires:  fftw3-devel
BuildRequires:  libminc-devel
BuildRequires:  gdcm-devel
BuildRequires:  itk-cmake

%description
elastix is open source software, based on the well-known [Insight Segmentation
and Registration Toolkit (ITK)](https://itk.org/). The software consists of a
collection of algorithms that are commonly used to solve (medical) image
registration problems. The modular design of elastix allows the user to quickly
configure, test, and compare different registration methods for a specific
application. A command-line interface enables automated processing of large
numbers of data sets, by means of scripting. Nowadays elastix is accompanied by
[SimpleElastix](http://simpleelastix.github.io/), making it available in
languages like C++, Python, Java, R, Ruby, C# and Lua.

%package        static
Summary:        elastix static libraries
Group:          Development/Libraries
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
elastix static libraries.

%package        devel
Summary:        elastix development files
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
elastix development files.

%prep
%setup -q


%build
# It seems that ITK_DIR isn't necessary on master as of 2018/06.19
# Maybe it won't be necessary to specify in a few more builds

    # This doesn't compile on my computer
    # -DUSE_ALL_COMPONENTS:BOOL=ON
%cmake \
    -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo"\
    -DCMAKE_CXX_FLAGS:STRING="%{optflags}" \
    -DCMAKE_VERBOSE_MAKEFILE=ON\
    -DELASTIX_BUILD_EXECUTABLE:BOOL=OFF \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    -DELASTIX_ARCHIVE_DIR:BOOL=%{_lib} \
    -DELASTIX_LIBRARY_DIR=%{_lib} \
    -DELASTIX_INCLUDE_DIR=include/%{name} \
    -DELASTIX_RUNTIME_DIR:PATH=%{_bindir}

# Replace the stupid build dir with the actual include dir
sed '/^set( ELASTIX_INCLUDE_DIRS/s@'"%{_builddir}/%{name}-%{version}"'@'"%{_includedir}/%{name}"'@g' -i ElastixConfig.cmake

sed 's@Elastix_DIR .* '")"'@'"Elastix_DIR %{_libdir}/cmake/%{name} )"'@' -i ElastixConfig.cmake

sed 's@ELASTIX_LIBRARY_DIRS .* '")"'@ELASTIX_LIBRARY_DIRS '"%{_libdir}"' '")"'@' -i ElastixConfig.cmake
sed 's@'"elxLIBRARY_DEPENDS_FILE .*/elxLibraryDepends.cmake"'@'"elxLIBRARY_DEPENDS_FILE \"\${Elastix_DIR}/elxLibraryDepends.cmake\""'@' -i ElastixConfig.cmake

# Correct static library locations
sed 's@/builddir/build/BUILD/elastix-4.9.0/bin@'"%{_libdir}"'@' -i ElastixTargets.cmake

%make_build

%install
%make_install

mkdir -p %{buildroot}%{_libdir}/cmake/%{name}
install ElastixConfig.cmake %{buildroot}%{_libdir}/cmake/%{name}
install ElastixTargets.cmake %{buildroot}%{_libdir}/cmake/%{name}
install UseElastix.cmake %{buildroot}%{_libdir}/cmake/%{name}
install elxLibraryDepends.cmake %{buildroot}%{_libdir}/cmake/%{name}

%files
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/cmake/%{name}

%files static
%{_libdir}/*.a

%changelog
* Wed Jun 20 2018 Mark Harfouche <mark.harfouche@gmail.com> - 4.9.0-3
- Now install cmake files

* Tue Jun 19 2018 Mark Harfouche <mark.harfouche@gmail.com> - 4.9.0-2
- Initial build
