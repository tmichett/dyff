# dyff RPM Spec File for Fedora
# Build with: rpmbuild -ba dyff.spec

%global debug_package %{nil}
%global import_path github.com/homeport/dyff

# No special defines needed - we use a glob pattern in %files to handle optional docs

Name:           dyff
Version:        1.9.3
Release:        1%{?dist}
Summary:        A diff tool for YAML files, and sometimes JSON

License:        MIT
URL:            https://github.com/homeport/dyff
Source0:        https://github.com/homeport/%{name}/archive/v%{version}.tar.gz

# Build requirements
BuildRequires:  golang >= 1.23.0
BuildRequires:  git
BuildRequires:  make

# Runtime requirements (none for static binary)
# Requires:

# Exclusive architecture
ExclusiveArch:  x86_64

%description
dyff (pronounced /ˈdʏf/) is a diff tool for YAML files, and sometimes JSON.
It is inspired by the way the old BOSH v1 deployment output reported changes
from one version to another by only showing the parts of a YAML file that change.

Each difference is referenced by its location in the YAML document by using
either the Spruce dot-style syntax or go-patch path syntax. The output report
aims to be as compact as possible to give a clear and simple overview of the
change.

Key features:
- Diff YAML and JSON files with structural understanding
- Multiple output formats (human, brief, github, gitlab, gitea)
- Convert between YAML and JSON while preserving key order
- Integration with kubectl and git
- Kubernetes resource comparison support
- Pretty-print YAML/JSON with syntax highlighting
- Restructure YAML files with sensible key ordering

%prep
%setup -q -n %{name}-%{version}

%build
# Set up Go environment
export GODEBUG=netdns=go
export GIT_IPV4=true
export GOPROXY=direct
export GOPATH=$(pwd)/.gopath
export GO111MODULE=on
export CGO_ENABLED=0
export GOOS=linux
export GOARCH=amd64

# Build the binary with version information
go build -v \
  -buildmode=pie \
  -mod=readonly \
  -modcacherw \
  -ldflags="-s -w -X github.com/tmichett/dyff/internal/cmd.version=%{version}" \
  -o dyff \
  ./cmd/dyff

%install
# Create necessary directories
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_docdir}/%{name}
install -d %{buildroot}%{_licensedir}/%{name}

# Install binary
install -p -m 0755 dyff %{buildroot}%{_bindir}/dyff

# Install documentation
install -p -m 0644 README.md %{buildroot}%{_docdir}/%{name}/
install -p -m 0644 LICENSE %{buildroot}%{_docdir}/%{name}/
install -p -m 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/

# Install USER_GUIDE.md only if it exists (it's not in upstream repo)
if [ -f USER_GUIDE.md ]; then
  install -p -m 0644 USER_GUIDE.md %{buildroot}%{_docdir}/%{name}/
fi

# Generate man page (if available)
# For now, we'll create a basic man page
cat > %{buildroot}%{_mandir}/man1/dyff.1 << 'EOF'
.TH DYFF 1 "2025" "dyff %{version}" "User Commands"
.SH NAME
dyff \- a diff tool for YAML files, and sometimes JSON
.SH SYNOPSIS
.B dyff
[\fIGLOBAL OPTIONS\fR]
.I COMMAND
[\fICOMMAND OPTIONS\fR]
[\fIARGUMENTS\fR...]
.SH DESCRIPTION
.B dyff
is a diff tool for YAML files, and sometimes JSON. It understands the structure
of YAML and JSON documents and presents differences in a human-readable format.
.PP
Each difference is referenced by its location in the YAML document using either
the Spruce dot-style syntax (some.path.in.the.file) or go-patch path syntax
(/some/name=path/in/the/id=file).
.SH COMMANDS
.TP
.B between
Compare differences between input files from and to
.TP
.B yaml
Convert input documents into YAML format
.TP
.B json
Convert input documents into JSON format
.TP
.B last-applied
Compare differences between the current state and the one stored in Kubernetes
last-applied configuration
.TP
.B version
Show the version of dyff
.SH GLOBAL OPTIONS
.TP
\fB\-c\fR, \fB\-\-color\fR \fIon|off|auto\fR
Specify color usage
.TP
\fB\-t\fR, \fB\-\-truecolor\fR \fIon|off|auto\fR
Specify true color usage
.TP
\fB\-w\fR, \fB\-\-fixed\-width\fR \fINUMBER\fR
Disable terminal width detection and use provided fixed value
.TP
\fB\-k\fR, \fB\-\-preserve\-key\-order\-in\-json\fR
Use ordered keys during JSON decoding
.SH EXAMPLES
.TP
Compare two YAML files:
.B dyff between old.yml new.yml
.TP
Convert JSON to YAML:
.B dyff yaml config.json
.TP
Convert YAML to JSON:
.B dyff json config.yml
.TP
Use with kubectl:
.B export KUBECTL_EXTERNAL_DIFF="dyff between --omit-header --set-exit-code"
.br
.B kubectl diff -f deployment.yml
.TP
Compare with remote file:
.B dyff between local.yml https://example.com/remote.yml
.SH FILES
.TP
.I /usr/share/doc/dyff/README.md
Project README file
.TP
.I /usr/share/doc/dyff/USER_GUIDE.md
Comprehensive user guide
.TP
.I /usr/share/doc/dyff/LICENSE
License information
.SH EXIT STATUS
By default, dyff exits with status 0 regardless of differences found.
.PP
When using \fB\-\-set\-exit\-code\fR flag:
.TP
.B 0
No differences detected
.TP
.B 1
Differences found
.TP
.B 255
Error occurred
.SH SEE ALSO
.BR diff (1),
.BR kubectl (1),
.BR git (1)
.SH BUGS
Report bugs at: https://github.com/homeport/dyff/issues
.SH AUTHOR
The Homeport Team
.SH COPYRIGHT
Copyright (c) 2019 The Homeport Team. Licensed under MIT License.
EOF

%check
# Basic smoke test
%{buildroot}%{_bindir}/dyff version

%files
%{_bindir}/dyff
%{_mandir}/man1/dyff.1*
# License directory
%dir %{_licensedir}/%{name}
%{_licensedir}/%{name}/LICENSE
# Documentation directory - glob pattern includes README.md, LICENSE, and USER_GUIDE.md (if present)
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/*

%changelog
* Mon Oct 06 2025 Package Maintainer <maintainer@example.com> - 1.9.3-1
- Initial RPM package for Fedora
- Build for x86_64 architecture
- Static binary with no runtime dependencies
- Include man page and documentation
- MIT License
- Make USER_GUIDE.md optional for COPR builds (not in upstream source)

* Sun Oct 05 2025 Package Maintainer <maintainer@example.com> - 1.9.2-1
- Version bump to 1.9.2
- Updated dependencies

* Sat Oct 04 2025 Package Maintainer <maintainer@example.com> - 1.9.1-1
- Version bump to 1.9.1
- Bug fixes and improvements

* Fri Oct 03 2025 Package Maintainer <maintainer@example.com> - 1.9.0-1
- Version bump to 1.9.0
- New features and improvements

