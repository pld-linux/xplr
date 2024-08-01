%define		crates_ver	0.21.9

Summary:	A hackable, minimal, fast TUI file explorer
Name:		xplr
Version:	0.21.9
Release:	1
License:	MIT
Group:		Applications/Console
Source0:	https://github.com/sayanarijit/xplr/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6b82ffcd9f0d39678c405c61b2bfe04a
Source1:	%{name}-crates-%{crates_ver}.tar.xz
# Source1-md5:	8fc446b98dc0b07a3f062506878a6dda
URL:		https://xplr.dev
BuildRequires:	cargo
BuildRequires:	luajit-devel < 2.2
BuildRequires:	luajit-devel >= 2.0.4
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.004
BuildRequires:	rust
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%{ix86} %{x8664} aarch64 armv6hl armv7hl armv7hnl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xplr is a terminal UI based file explorer that aims to increase our
terminal productivity by being a flexible, interactive orchestrator
for the ever growing awesome command-line utilities that work with the
file-system.

To achieve its goal, xplr strives to be a fast, minimal and more
importantly, hackable file explorer.

xplr is not meant to be a replacement for the standard shell commands
or the GUI file managers. Rather, it aims to integrate them all and
expose an intuitive, scriptable, keyboard controlled, real-time visual
interface, also being an ideal candidate for further integration,
enabling you to achieve insane terminal productivity.

%prep
%setup -q -a1

%{__mv} xplr-%{crates_ver}/* .
sed -i -e 's/@@VERSION@@/%{version}/' Cargo.lock

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

%cargo_build --frozen --no-default-features

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}/man1
export CARGO_HOME="$(pwd)/.cargo"

%cargo_install --frozen --no-default-features --root $RPM_BUILD_ROOT%{_prefix} --path $PWD
%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTING.md LICENSE README.md
%attr(755,root,root) %{_bindir}/xplr
