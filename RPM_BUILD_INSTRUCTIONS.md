# Building RPM Package for dyff on Fedora

This guide provides comprehensive instructions for building an RPM package of dyff for Fedora Linux (x86_64 architecture).

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Manual Build Process](#manual-build-process)
4. [Package Details](#package-details)
5. [Installation](#installation)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)
8. [Distribution](#distribution)

---

## Prerequisites

### System Requirements

- **Operating System**: Fedora Linux (tested on Fedora 38+)
- **Architecture**: x86_64 (AMD64)
- **Disk Space**: At least 500 MB free space
- **Memory**: At least 1 GB RAM

### Required Software

Install the required tools:

```bash
sudo dnf install -y \
    golang \
    git \
    rpm-build \
    rpmdevtools \
    make
```

### Verify Go Installation

Ensure Go 1.23 or later is installed:

```bash
go version
# Should output: go version go1.23.x or higher
```

If Go is not installed or the version is too old:

```bash
# Install or update Go
sudo dnf install golang

# Or download from https://go.dev/dl/
```

---

## Quick Start

Use the provided build script for automated RPM building:

```bash
# Make the script executable
chmod +x build-rpm.sh

# Build the RPM (uses version from spec file)
./build-rpm.sh

# Or specify a version
./build-rpm.sh 1.9.3
```

The script will:
1. Set up the RPM build environment
2. Create the source tarball
3. Install build dependencies
4. Build the RPM package
5. Copy the RPM to the current directory
6. Display installation instructions

**Output**: `dyff-<version>-<release>.fc<fedora_version>.x86_64.rpm`

---

## Manual Build Process

If you prefer to build manually or the script doesn't work:

### Step 1: Set Up RPM Build Environment

```bash
# Create RPM build directory structure
rpmdev-setuptree

# This creates:
# ~/rpmbuild/
# ├── BUILD/
# ├── RPMS/
# ├── SOURCES/
# ├── SPECS/
# └── SRPMS/
```

### Step 2: Prepare Source Tarball

**Option A: From Git Repository**

```bash
# Clone or navigate to the dyff repository
cd /path/to/dyff

# Get the current version
VERSION="1.9.3"  # Update as needed

# Create source tarball
git archive --format=tar --prefix="dyff-${VERSION}/" HEAD | gzip > ~/rpmbuild/SOURCES/v${VERSION}.tar.gz

# Verify tarball
tar tzf ~/rpmbuild/SOURCES/v${VERSION}.tar.gz | head
```

**Option B: Download from GitHub**

```bash
VERSION="1.9.3"  # Update as needed

# Download release tarball
curl -L -o ~/rpmbuild/SOURCES/v${VERSION}.tar.gz \
    https://github.com/homeport/dyff/archive/v${VERSION}.tar.gz

# Verify download
ls -lh ~/rpmbuild/SOURCES/v${VERSION}.tar.gz
```

### Step 3: Copy Spec File

```bash
# Copy the spec file to SPECS directory
cp dyff.spec ~/rpmbuild/SPECS/

# Optionally, edit the spec file to update version
vi ~/rpmbuild/SPECS/dyff.spec
```

### Step 4: Install Build Dependencies

```bash
# Automatic method (if available)
sudo dnf builddep ~/rpmbuild/SPECS/dyff.spec

# Manual method
sudo dnf install -y golang git make
```

### Step 5: Build the RPM

```bash
# Build both binary and source RPM
rpmbuild -ba ~/rpmbuild/SPECS/dyff.spec

# Or just build binary RPM
rpmbuild -bb ~/rpmbuild/SPECS/dyff.spec
```

### Step 6: Locate Built Packages

```bash
# Find the built RPM
find ~/rpmbuild/RPMS/ -name "dyff*.rpm"

# Find the source RPM
find ~/rpmbuild/SRPMS/ -name "dyff*.src.rpm"
```

---

## Package Details

### Package Information

- **Name**: dyff
- **Version**: 1.9.3 (or as specified)
- **Architecture**: x86_64
- **License**: MIT
- **Source**: https://github.com/homeport/dyff

### Package Contents

The RPM installs the following files:

```
/usr/bin/dyff                          # Main executable
/usr/share/man/man1/dyff.1.gz          # Man page
/usr/share/doc/dyff/README.md          # README
/usr/share/doc/dyff/USER_GUIDE.md      # User guide
/usr/share/doc/dyff/LICENSE            # License
```

### Inspect Package Before Installation

```bash
# View package information
rpm -qip dyff-*.rpm

# List package contents
rpm -qlp dyff-*.rpm

# View package dependencies
rpm -qRp dyff-*.rpm

# View package scripts
rpm -q --scripts -p dyff-*.rpm
```

---

## Installation

### Install from Local RPM

```bash
# Using DNF (recommended)
sudo dnf install ./dyff-*.rpm

# Using RPM directly
sudo rpm -ivh dyff-*.rpm

# Upgrade existing installation
sudo dnf upgrade ./dyff-*.rpm
# or
sudo rpm -Uvh dyff-*.rpm
```

### Verify Installation

```bash
# Check if dyff is installed
rpm -q dyff

# Test the installation
dyff version

# View installed files
rpm -ql dyff

# View documentation
man dyff
less /usr/share/doc/dyff/USER_GUIDE.md
```

### Uninstall

```bash
# Remove the package
sudo dnf remove dyff
# or
sudo rpm -e dyff
```

---

## Verification

### Post-Installation Tests

```bash
# 1. Check version
dyff version

# 2. Test YAML comparison
cat > test1.yml << EOF
name: test
version: 1
EOF

cat > test2.yml << EOF
name: test
version: 2
EOF

dyff between test1.yml test2.yml

# 3. Test YAML to JSON conversion
dyff json test1.yml

# 4. Test JSON to YAML conversion
echo '{"name":"test","version":1}' | dyff yaml -

# 5. Check man page
man dyff

# Cleanup
rm test1.yml test2.yml
```

### Package Integrity

```bash
# Verify package signature (if signed)
rpm -K dyff-*.rpm

# Verify installed files
rpm -V dyff

# Check for missing dependencies
ldd /usr/bin/dyff
```

---

## Troubleshooting

### Build Failures

#### Error: "Go version too old"

**Solution:**
```bash
# Check Go version
go version

# Update Go
sudo dnf update golang

# Or install newer version from https://go.dev/dl/
wget https://go.dev/dl/go1.23.0.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.23.0.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
```

#### Error: "BuildRequires not met"

**Solution:**
```bash
# Install missing dependencies manually
sudo dnf install golang git make rpm-build
```

#### Error: "Source tarball not found"

**Solution:**
```bash
# Verify the tarball exists
ls -l ~/rpmbuild/SOURCES/

# Re-download or recreate the tarball
VERSION="1.9.3"
curl -L -o ~/rpmbuild/SOURCES/v${VERSION}.tar.gz \
    https://github.com/homeport/dyff/archive/v${VERSION}.tar.gz
```

#### Error: "Permission denied"

**Solution:**
```bash
# Make sure directories have correct permissions
chmod -R u+w ~/rpmbuild

# Don't build as root (use regular user)
```

### Installation Issues

#### Error: "package dyff-x.x.x.rpm is not signed"

**Solution:**
```bash
# Install without signature verification (use with caution)
sudo rpm -ivh --nosignature dyff-*.rpm

# Or using DNF
sudo dnf install --nogpgcheck ./dyff-*.rpm
```

#### Error: "dyff: command not found" after installation

**Solution:**
```bash
# Check if package is installed
rpm -q dyff

# Check PATH
echo $PATH

# Binary should be in /usr/bin
ls -l /usr/bin/dyff

# Try with full path
/usr/bin/dyff version
```

### Runtime Issues

#### Error: "failed to load input files"

**Solution:**
```bash
# Check file permissions
ls -l your-file.yml

# Verify file is valid YAML
cat your-file.yml

# Test with simple file
echo "test: value" | dyff yaml -
```

---

## Distribution

### Create RPM Repository

If you want to distribute the RPM via a repository:

```bash
# Install createrepo
sudo dnf install createrepo_c

# Create repository directory
mkdir -p ~/rpm-repo/fedora/x86_64

# Copy RPM to repository
cp dyff-*.rpm ~/rpm-repo/fedora/x86_64/

# Create repository metadata
createrepo ~/rpm-repo/fedora/x86_64/

# Serve via HTTP (example with Python)
cd ~/rpm-repo
python3 -m http.server 8000
```

### Configure Clients to Use Your Repository

On client machines:

```bash
# Create repo file
sudo tee /etc/yum.repos.d/dyff.repo << EOF
[dyff]
name=dyff Repository
baseurl=http://your-server:8000/fedora/x86_64/
enabled=1
gpgcheck=0
EOF

# Install from repository
sudo dnf install dyff
```

### Sign RPM Package

For production distribution, sign your RPMs:

```bash
# Generate GPG key if you don't have one
gpg --gen-key

# Configure RPM macros
cat >> ~/.rpmmacros << EOF
%_signature gpg
%_gpg_name Your Name <your-email@example.com>
EOF

# Sign the RPM
rpm --addsign dyff-*.rpm

# Verify signature
rpm --checksig dyff-*.rpm
```

### Upload to Package Repositories

#### Fedora Copr

1. Create account at https://copr.fedorainfracloud.org/
2. Create new project
3. Upload SRPM:

```bash
# Build source RPM
rpmbuild -bs ~/rpmbuild/SPECS/dyff.spec

# Upload to Copr (via web interface or copr-cli)
copr-cli build your-project ~/rpmbuild/SRPMS/dyff-*.src.rpm
```

---

## Advanced Topics

### Building for Different Fedora Versions

```bash
# Build for Fedora 38
rpmbuild -ba --define "fedora 38" ~/rpmbuild/SPECS/dyff.spec

# Build for Fedora 39
rpmbuild -ba --define "fedora 39" ~/rpmbuild/SPECS/dyff.spec
```

### Mock Builds

Use Mock for clean room builds:

```bash
# Install Mock
sudo dnf install mock

# Add your user to mock group
sudo usermod -a -G mock $USER
newgrp mock

# Build using Mock
mock -r fedora-38-x86_64 ~/rpmbuild/SRPMS/dyff-*.src.rpm

# Results in:
# /var/lib/mock/fedora-38-x86_64/result/
```

### Customizing the Spec File

Edit `dyff.spec` to customize:

```spec
# Change version
Version:        1.9.4

# Add patches
Patch0:         custom.patch

# Modify build flags
go build -ldflags="-X main.customflag=value" ...

# Add custom files
install -p -m 0644 custom-doc.md %{buildroot}%{_docdir}/%{name}/
```

### Cross-Architecture Builds

While this spec is for x86_64, you can adapt for other architectures:

```spec
# In dyff.spec, change:
ExclusiveArch:  x86_64

# To support multiple architectures:
ExclusiveArch:  x86_64 aarch64
```

---

## Appendix

### Spec File Structure

The `dyff.spec` file contains:

1. **Header**: Package metadata
2. **%description**: Package description
3. **%prep**: Prepare source code
4. **%build**: Compile the software
5. **%install**: Install files
6. **%check**: Run tests
7. **%files**: List installed files
8. **%changelog**: Version history

### Useful Commands

```bash
# Show RPM build configuration
rpmbuild --showrc

# List macros
rpm --showrc | grep topdir

# Check spec file syntax
rpmlint ~/rpmbuild/SPECS/dyff.spec

# Check RPM package
rpmlint dyff-*.rpm

# Extract RPM contents
rpm2cpio dyff-*.rpm | cpio -idmv
```

### Resources

- **RPM Packaging Guide**: https://rpm-packaging-guide.github.io/
- **Fedora Packaging Guidelines**: https://docs.fedoraproject.org/en-US/packaging-guidelines/
- **Go Packaging**: https://docs.fedoraproject.org/en-US/packaging-guidelines/Golang/
- **dyff Project**: https://github.com/homeport/dyff

---

## Support

For issues specific to:
- **dyff software**: https://github.com/homeport/dyff/issues
- **RPM packaging**: Create an issue in your repository
- **Fedora packaging**: https://ask.fedoraproject.org/

---

## License

The dyff software is licensed under the MIT License.
This packaging is also provided under the MIT License.

Copyright (c) 2019 The Homeport Team

