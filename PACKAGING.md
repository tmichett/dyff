# dyff Packaging Documentation

This document provides an overview of the packaging files and documentation created for dyff.

## Files Overview

### Documentation Files

1. **USER_GUIDE.md** - Comprehensive user documentation
   - Complete command reference
   - Usage examples and common use cases
   - Integration guides (kubectl, git, CI/CD)
   - Troubleshooting section
   - Advanced features and tips

2. **RPM_BUILD_INSTRUCTIONS.md** - RPM packaging guide
   - Prerequisites and system requirements
   - Step-by-step build instructions
   - Installation and verification procedures
   - Troubleshooting common issues
   - Distribution methods

3. **PACKAGING.md** (this file) - Packaging overview

### Packaging Files

1. **dyff.spec** - RPM specification file
   - Defines package metadata
   - Build instructions
   - Installation rules
   - Includes man page generation
   - Changelog tracking

2. **build-rpm.sh** - Automated RPM build script
   - Sets up RPM build environment
   - Creates source tarball
   - Installs dependencies
   - Builds and tests the RPM
   - Provides colored output and error handling

## Quick Start for RPM Building

### Requirements

- Fedora Linux (38 or later recommended)
- x86_64 architecture
- 500 MB free disk space
- 1 GB RAM

### Install Dependencies

```bash
sudo dnf install -y golang git rpm-build rpmdevtools make
```

### Build the RPM

```bash
# Make the build script executable (if not already)
chmod +x build-rpm.sh

# Run the build script
./build-rpm.sh

# Or specify a version
./build-rpm.sh 1.9.3
```

### Install the RPM

```bash
sudo dnf install ./dyff-*.rpm
```

### Verify Installation

```bash
dyff version
man dyff
```

## Package Contents

Once installed, the RPM provides:

```
/usr/bin/dyff                          # Main executable
/usr/share/man/man1/dyff.1.gz          # Man page
/usr/share/doc/dyff/README.md          # Project README
/usr/share/doc/dyff/USER_GUIDE.md      # Comprehensive user guide
/usr/share/doc/dyff/LICENSE            # License file
```

## Documentation Structure

### USER_GUIDE.md Sections

1. **Introduction** - Overview and key features
2. **Installation** - Various installation methods
3. **Basic Concepts** - Core concepts and terminology
4. **Commands Reference** - Detailed command documentation
5. **Common Use Cases** - Practical examples
6. **Advanced Features** - Power user features
7. **Configuration and Flags** - All available options
8. **Integration with Other Tools** - kubectl, git, CI/CD
9. **Troubleshooting** - Common issues and solutions
10. **Examples** - Real-world usage examples

### RPM_BUILD_INSTRUCTIONS.md Sections

1. **Prerequisites** - System and software requirements
2. **Quick Start** - Automated build process
3. **Manual Build Process** - Step-by-step instructions
4. **Package Details** - Package information and contents
5. **Installation** - Installation procedures
6. **Verification** - Testing and validation
7. **Troubleshooting** - Build and installation issues
8. **Distribution** - Repository setup and signing

## Usage Examples

### Basic Usage

```bash
# Compare two YAML files
dyff between old.yml new.yml

# Convert YAML to JSON
dyff json config.yml

# Convert JSON to YAML
dyff yaml config.json

# Pretty-print with restructuring
dyff yaml --restructure messy.yml
```

### With kubectl

```bash
export KUBECTL_EXTERNAL_DIFF="dyff between --omit-header --set-exit-code"
kubectl diff -f deployment.yml
```

### With Git

```bash
git config --local diff.dyff.command 'dyff_between() { dyff --color on between --omit-header "$2" "$5"; }; dyff_between'
echo '*.yml diff=dyff' >> .gitattributes
git diff config.yml
```

## Package Metadata

- **Name**: dyff
- **Version**: 1.9.3 (configurable)
- **License**: MIT
- **Architecture**: x86_64
- **Homepage**: https://github.com/homeport/dyff
- **Maintainer**: The Homeport Team

## Building Process Overview

1. **Preparation**
   - Set up RPM build environment
   - Prepare source tarball from git or download

2. **Dependencies**
   - Go 1.23 or later
   - Git, make, rpm-build tools

3. **Build**
   - Extract source
   - Compile with Go
   - Generate man page
   - Create binary RPM

4. **Testing**
   - Smoke test the binary
   - Verify package contents
   - Check version information

5. **Output**
   - Binary RPM: `dyff-<version>-<release>.fc<version>.x86_64.rpm`
   - Source RPM: `dyff-<version>-<release>.fc<version>.src.rpm`

## Customization

### Modify Version

Edit `dyff.spec`:
```spec
Version:        1.9.4
```

Or pass to build script:
```bash
./build-rpm.sh 1.9.4
```

### Add Custom Files

Edit the `%install` section in `dyff.spec`:
```spec
install -p -m 0644 custom-file %{buildroot}%{_docdir}/%{name}/
```

And the `%files` section:
```spec
%{_docdir}/%{name}/custom-file
```

### Modify Build Flags

Edit the `%build` section in `dyff.spec`:
```spec
go build -ldflags="-X main.version=%{version} -X main.custom=value" ...
```

## Distribution Options

### 1. Direct Distribution

Share the RPM file directly:
```bash
# Copy to shared location
cp dyff-*.rpm /shared/rpms/

# Users install with:
sudo dnf install /shared/rpms/dyff-*.rpm
```

### 2. HTTP Repository

Host RPMs via HTTP:
```bash
# Create repository
mkdir -p ~/rpm-repo
cp dyff-*.rpm ~/rpm-repo/
createrepo ~/rpm-repo/

# Serve via HTTP
cd ~/rpm-repo && python3 -m http.server 8000
```

### 3. Fedora Copr

Build and distribute via Copr:
```bash
# Upload to Copr
copr-cli build your-project dyff-*.src.rpm

# Users add repo and install:
sudo dnf copr enable you/your-project
sudo dnf install dyff
```

### 4. Internal Repository

Add to organization's package repository:
```bash
# Copy to repository
cp dyff-*.rpm /var/www/html/rpms/fedora/x86_64/

# Update repository metadata
createrepo --update /var/www/html/rpms/fedora/x86_64/
```

## Integration with CI/CD

### GitHub Actions

```yaml
name: Build RPM

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    container: fedora:latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Install dependencies
        run: |
          dnf install -y golang git rpm-build rpmdevtools make
      
      - name: Build RPM
        run: |
          ./build-rpm.sh
      
      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: rpm-package
          path: dyff-*.rpm
```

### GitLab CI

```yaml
build_rpm:
  image: fedora:latest
  
  before_script:
    - dnf install -y golang git rpm-build rpmdevtools make
  
  script:
    - ./build-rpm.sh
  
  artifacts:
    paths:
      - dyff-*.rpm
    expire_in: 1 week
```

## Testing

### Package Testing

```bash
# Install in clean environment
podman run -it --rm -v $(pwd):/work:z fedora:latest bash
cd /work
dnf install -y ./dyff-*.rpm
dyff version
```

### Automated Testing

```bash
# Add to build-rpm.sh or CI
cat > test-rpm.sh << 'EOF'
#!/bin/bash
set -e

# Install RPM
sudo dnf install -y ./dyff-*.rpm

# Test version
dyff version

# Test comparison
echo "test: 1" > test1.yml
echo "test: 2" > test2.yml
dyff between test1.yml test2.yml

# Test conversion
dyff json test1.yml
dyff yaml test1.yml

# Cleanup
rm test1.yml test2.yml

echo "All tests passed!"
EOF

chmod +x test-rpm.sh
./test-rpm.sh
```

## Maintenance

### Updating for New dyff Version

1. Update version in `dyff.spec`:
   ```spec
   Version:        1.9.4
   ```

2. Add changelog entry:
   ```spec
   %changelog
   * Mon Oct 06 2025 Maintainer <email> - 1.9.4-1
   - Updated to version 1.9.4
   - Bug fixes and improvements
   ```

3. Rebuild:
   ```bash
   ./build-rpm.sh 1.9.4
   ```

### Maintaining Documentation

- Keep USER_GUIDE.md synchronized with dyff features
- Update RPM_BUILD_INSTRUCTIONS.md for process changes
- Test all examples and commands before release

## Support and Resources

### Documentation

- User Guide: See USER_GUIDE.md
- Build Instructions: See RPM_BUILD_INSTRUCTIONS.md
- dyff README: See README.md

### Links

- dyff Project: https://github.com/homeport/dyff
- RPM Packaging Guide: https://rpm-packaging-guide.github.io/
- Fedora Packaging: https://docs.fedoraproject.org/en-US/packaging-guidelines/
- Go Packaging: https://docs.fedoraproject.org/en-US/packaging-guidelines/Golang/

### Getting Help

- **dyff Issues**: https://github.com/homeport/dyff/issues
- **RPM Questions**: https://ask.fedoraproject.org/
- **Packaging Help**: https://discussion.fedoraproject.org/

## License

All packaging materials are provided under the MIT License, matching the dyff project license.

```
MIT License

Copyright (c) 2019 The Homeport Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments

- The Homeport Team for creating dyff
- Fedora Project for packaging guidelines and tools
- Go community for excellent tooling

---

**Last Updated**: October 6, 2025  
**Package Version**: 1.9.3  
**Maintainer**: Package Maintainer

