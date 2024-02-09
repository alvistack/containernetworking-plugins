# Copyright 2025 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: containernetworking-plugins
Epoch: 100
Version: 1.6.1
Release: 1%{?dist}
Summary: Libraries for writing CNI plugin
License: Apache-2.0
URL: https://github.com/containernetworking/plugins/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.23
BuildRequires: glibc-static
Requires: containernetworking

%description
The CNI (Container Network Interface) project consists of a
specification and libraries for writing plugins to configure network
interfaces in Linux containers, along with a number of supported
plugins. CNI concerns itself only with network connectivity of
containers and removing allocated resources when the container is
deleted.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p bin
set -ex && \
    export CGO_ENABLED=1 && \
    ./build_linux.sh -buildmode pie -v -ldflags "-s -w"

%install
install -Dpm755 -d %{buildroot}/opt/cni/bin
install -Dpm755 -d %{buildroot}%{_unitdir}
install -Dpm755 -t %{buildroot}/opt/cni/bin bin/*
install -Dpm644 -t %{buildroot}%{_unitdir} plugins/ipam/dhcp/systemd/*

%files
%license LICENSE
%dir /opt/cni
%dir /opt/cni/bin
/opt/cni/bin/*
%{_unitdir}/*

%changelog
