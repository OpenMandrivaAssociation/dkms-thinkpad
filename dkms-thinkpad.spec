%define	modname	thinkpad
%define	name	dkms-%{modname}
%define	version	6.0
%define	rel	2
%define	release	%mkrel %{rel}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	DKMS-ready module adding kernel support for older Thinkpad laptops
License:	GPL
Source0:	%{modname}_%{version}.tar.gz
Patch0:		thinkpad-6.0-linux-2.6.2x-Makefiles.patch
Url:		http://heanet.dl.sourceforge.net/sourceforge/tpctl/
Group:		Development/Kernel
Requires(pre):	dkms
Requires(post): dkms
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Buildarch:	noarch

%description
This package contains a DKMS-ready module adding kernel support
for older Thinkpad laptops.

%prep
%setup -q -c -n %{modname}-%{version}
%patch0 -p0
# fix bad name, otherwise kbuild doesn't compile it
mv %modname-%version/2.6/drivers/smapi_call.s %modname-%version/2.6/drivers/smapi_call.S
chmod -R go=u-w .

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_usrsrc}/%{modname}-%{version}-%{release}
cp -a %{modname}-%{version}/* %{buildroot}%{_usrsrc}/%{modname}-%{version}-%{release}
cat > %{buildroot}%{_usrsrc}/%{modname}-%{version}-%{release}/dkms.conf <<EOF

PACKAGE_VERSION="%{version}-%{release}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="%{modname}"
MAKE[0]="make -C \${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build"
CLEAN="make -C \${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build clean"
BUILT_MODULE_LOCATION[0]="2.6/drivers"
BUILT_MODULE_NAME[0]="thinkpad"
DEST_MODULE_LOCATION[0]="/extra"
BUILT_MODULE_LOCATION[1]="2.6/drivers"
BUILT_MODULE_NAME[1]="smapi"
DEST_MODULE_LOCATION[1]="/extra"
BUILT_MODULE_LOCATION[2]="2.6/drivers"
BUILT_MODULE_NAME[2]="superio"
DEST_MODULE_LOCATION[2]="/extra"
BUILT_MODULE_LOCATION[3]="2.6/drivers"
BUILT_MODULE_NAME[3]="rtcmosram"
DEST_MODULE_LOCATION[3]="/extra"
REMAKE_INITRD="no"
AUTOINSTALL="YES"
EOF

%post
#if [ $1 == 1 ]
#then 
  dkms add -m %{modname} -v %{version}-%{release} --rpm_safe_upgrade \
  && dkms build -m %{modname} -v %{version}-%{release} --rpm_safe_upgrade \
  && dkms install -m %{modname} -v %{version}-%{release} --rpm_safe_upgrade
#fi


%preun
#if [ $1 == 0 ]
#  then
  dkms remove -m %{modname} -v %{version}-%{release} --rpm_safe_upgrade --all
#fi

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%docdir %{_usrsrc}/%{modname}-%{version}-%{release}/doc
/usr/src/%{modname}-%{version}-%{release}


