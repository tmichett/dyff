# Building dyff in Fedora COPR

This guide explains how to build dyff in Fedora COPR (Cool Other Package Repositories).

## Overview

The `dyff.spec` file has been designed to work both for local builds (where custom documentation like `USER_GUIDE.md` may be present) and COPR builds (which use upstream source tarballs that don't include custom documentation).

## The COPR Build Issue (Fixed)

### Problem

When building locally with our build script, we can include custom documentation files like `USER_GUIDE.md`. However, COPR builds from upstream GitHub releases, and these files don't exist in the upstream repository. This caused build failures:

```
install: cannot stat 'USER_GUIDE.md': No such file or directory
error: Bad exit status from /var/tmp/rpm-tmp.j9eREU (%install)
```

### Solution

The spec file now detects whether `USER_GUIDE.md` exists and conditionally includes it:

```spec
# In %prep section
%global has_userguide %(test -f USER_GUIDE.md && echo 1 || echo 0)

# In %install section
%if 0%{?has_userguide}
install -p -m 0644 USER_GUIDE.md %{buildroot}%{_docdir}/%{name}/
%endif

# In %files section
%if 0%{?has_userguide}
%{_docdir}/%{name}/USER_GUIDE.md
%endif
```

This allows the spec file to work in both scenarios:
- **Local builds**: Includes `USER_GUIDE.md` if present
- **COPR builds**: Skips `USER_GUIDE.md` if not present (no error)

## Setting Up COPR Build

### Prerequisites

1. **COPR Account**: Create an account at https://copr.fedorainfracloud.org/
2. **copr-cli**: Install the command-line tool
   ```bash
   sudo dnf install copr-cli
   ```
3. **API Token**: Get your API token from COPR settings and save to `~/.config/copr`

### Method 1: Build from Upstream GitHub (Recommended for COPR)

This method pulls directly from the dyff GitHub repository.

#### Step 1: Create a New COPR Project

1. Go to https://copr.fedorainfracloud.org/
2. Click "New Project"
3. Fill in:
   - **Name**: `dyff`
   - **Description**: `A diff tool for YAML files, and sometimes JSON`
   - **Instructions**: Link to documentation
   - **Chroots**: Select Fedora versions (e.g., Fedora 38, 39, 40, 41, 42, 43)
   - **Build dependencies**: Leave default or add specific requirements

#### Step 2: Upload the Spec File

You need to provide just the spec file. COPR will download the source from GitHub.

**Option A: Via Web Interface**

1. In your COPR project, click "Builds" → "New Build"
2. Select "Upload SRPM"
3. Or better, use "SCM" method:
   - **Type**: Git
   - **Clone URL**: `https://github.com/homeport/dyff.git`
   - **Committish**: `v1.9.3` (or `main` for latest)
   - **Subdirectory**: Leave empty
   - **Spec File**: Upload your `dyff.spec`
   - **Type**: `rpkg`

**Option B: Via copr-cli**

```bash
# Build from SCM (GitHub)
copr-cli build dyff --scm-type git \
  --scm-url https://github.com/homeport/dyff.git \
  --scm-method make_srpm \
  --spec dyff.spec
```

### Method 2: Build from Custom Source (With USER_GUIDE.md)

If you want to include the custom `USER_GUIDE.md` in COPR builds, you need to create a custom source repository.

#### Step 1: Fork dyff Repository

1. Fork https://github.com/homeport/dyff
2. Add your custom files:
   ```bash
   git clone https://github.com/YOUR_USERNAME/dyff.git
   cd dyff
   
   # Copy your custom documentation
   cp /path/to/USER_GUIDE.md .
   cp /path/to/dyff.spec .
   
   # Commit and push
   git add USER_GUIDE.md dyff.spec
   git commit -m "Add RPM spec and user guide"
   git push
   ```

#### Step 2: Build from Your Fork

```bash
copr-cli build dyff --scm-type git \
  --scm-url https://github.com/YOUR_USERNAME/dyff.git \
  --scm-method make_srpm \
  --spec dyff.spec
```

### Method 3: Build from Source RPM

Build the source RPM locally first, then upload to COPR.

#### Step 1: Create Source RPM Locally

```bash
# Set up build environment
rpmdev-setuptree

# Create source tarball with your custom files
VERSION="1.9.3"
TEMP_DIR=$(mktemp -d)
cd /path/to/dyff

# Create tarball including custom docs
git archive --format=tar --prefix="dyff-${VERSION}/" HEAD > "${TEMP_DIR}/base.tar"
tar -rf "${TEMP_DIR}/base.tar" --transform="s,^,dyff-${VERSION}/," USER_GUIDE.md
gzip < "${TEMP_DIR}/base.tar" > ~/rpmbuild/SOURCES/v${VERSION}.tar.gz

# Copy spec file
cp dyff.spec ~/rpmbuild/SPECS/

# Build source RPM
rpmbuild -bs ~/rpmbuild/SPECS/dyff.spec

# Source RPM will be in ~/rpmbuild/SRPMS/
```

#### Step 2: Upload to COPR

```bash
# Upload the source RPM
copr-cli build dyff ~/rpmbuild/SRPMS/dyff-1.9.3-1.fc*.src.rpm
```

## Using COPR Repository

Once the build succeeds, users can install dyff from your COPR repository.

### For End Users

```bash
# Enable the COPR repository
sudo dnf copr enable YOUR_USERNAME/dyff

# Install dyff
sudo dnf install dyff

# Verify installation
dyff version
```

### Creating .repo File

Alternatively, create a repository file manually:

```bash
sudo tee /etc/yum.repos.d/dyff-copr.repo << 'EOF'
[dyff-copr]
name=Copr repo for dyff owned by YOUR_USERNAME
baseurl=https://download.copr.fedorainfracloud.org/results/YOUR_USERNAME/dyff/fedora-$releasever-$basearch/
type=rpm-md
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://download.copr.fedorainfracloud.org/results/YOUR_USERNAME/dyff/pubkey.gpg
repo_gpgcheck=0
enabled=1
enabled_metadata=1
EOF
```

## Monitoring Builds

### Check Build Status

```bash
# List all builds
copr-cli list-builds dyff

# Watch a specific build
copr-cli watch-build BUILD_ID
```

### View Build Logs

1. Go to your COPR project page
2. Click on the build
3. View logs for each chroot (Fedora version)
4. Download logs if needed

## Troubleshooting COPR Builds

### Build Fails with "cannot stat 'USER_GUIDE.md'"

**Cause**: Using an old version of the spec file without conditional installation.

**Solution**: Use the updated `dyff.spec` file that includes the conditional logic.

### Build Fails with Go Errors

**Cause**: Missing build dependencies or Go version issues.

**Solution**: Check the build log and ensure BuildRequires are correct:
```spec
BuildRequires:  golang >= 1.23.0
BuildRequires:  git
BuildRequires:  make
```

### Build Succeeds but Package is Missing Files

**Cause**: Files not included in %files section.

**Solution**: Review the spec file and ensure all installed files are listed in %files.

### Mock Errors

**Cause**: Issues with the COPR build environment.

**Solution**: 
1. Test locally with Mock first:
   ```bash
   mock -r fedora-43-x86_64 ~/rpmbuild/SRPMS/dyff-*.src.rpm
   ```
2. Check the mock configuration in COPR project settings.

## Best Practices for COPR

### 1. Test Locally First

Always test your spec file locally before uploading to COPR:

```bash
# Local build
./build-rpm.sh

# Mock build (clean environment)
mock -r fedora-43-x86_64 ~/rpmbuild/SRPMS/dyff-*.src.rpm
```

### 2. Use Version Tags

Build from specific version tags rather than `main`:

```bash
copr-cli build dyff --scm-type git \
  --scm-url https://github.com/homeport/dyff.git \
  --scm-committish v1.9.3 \
  --scm-method make_srpm \
  --spec dyff.spec
```

### 3. Enable Multiple Fedora Versions

Build for multiple Fedora releases to maximize compatibility:
- Fedora 38, 39, 40 (stable releases)
- Fedora Rawhide (development)
- EPEL 8, 9 (for RHEL/CentOS)

### 4. Keep Spec File in Sync

Keep your spec file updated with upstream changes:
- Monitor dyff releases
- Update Version: field
- Update changelog
- Test each update

### 5. Document Your Repository

Add good description and instructions in your COPR project:
- What is dyff
- How to install
- Link to documentation
- Link to upstream project

## Advanced: Automated COPR Builds

### Using GitHub Actions

Create `.github/workflows/copr-build.yml`:

```yaml
name: COPR Build

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  copr-build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Install copr-cli
        run: |
          sudo dnf install -y copr-cli
      
      - name: Configure COPR
        run: |
          mkdir -p ~/.config
          echo "${{ secrets.COPR_CONFIG }}" > ~/.config/copr
      
      - name: Trigger COPR Build
        run: |
          VERSION=${GITHUB_REF#refs/tags/v}
          copr-cli build dyff \
            --scm-type git \
            --scm-url https://github.com/${{ github.repository }} \
            --scm-committish ${GITHUB_REF} \
            --scm-method make_srpm \
            --spec dyff.spec
```

### Using GitLab CI

Create `.gitlab-ci.yml`:

```yaml
copr-build:
  image: fedora:latest
  
  only:
    - tags
  
  before_script:
    - dnf install -y copr-cli
    - mkdir -p ~/.config
    - echo "$COPR_CONFIG" > ~/.config/copr
  
  script:
    - |
      copr-cli build dyff \
        --scm-type git \
        --scm-url $CI_REPOSITORY_URL \
        --scm-committish $CI_COMMIT_TAG \
        --scm-method make_srpm \
        --spec dyff.spec
```

## Example: Complete COPR Setup

Here's a complete example of setting up dyff in COPR:

```bash
# 1. Install copr-cli
sudo dnf install copr-cli

# 2. Configure API token (get from https://copr.fedorainfracloud.org/api/)
nano ~/.config/copr
# Paste your token configuration

# 3. Create COPR project (one-time)
copr-cli create dyff \
  --chroot fedora-38-x86_64 \
  --chroot fedora-39-x86_64 \
  --chroot fedora-40-x86_64 \
  --chroot fedora-41-x86_64 \
  --chroot fedora-42-x86_64 \
  --chroot fedora-43-x86_64 \
  --description "A diff tool for YAML files, and sometimes JSON" \
  --instructions "https://github.com/homeport/dyff"

# 4. Build from upstream GitHub
copr-cli build dyff \
  --scm-type git \
  --scm-url https://github.com/homeport/dyff.git \
  --scm-committish v1.9.3 \
  --scm-method make_srpm \
  --spec dyff.spec

# 5. Watch build progress
copr-cli watch-build <BUILD_ID>

# 6. Once successful, users can install with:
# sudo dnf copr enable YOUR_USERNAME/dyff
# sudo dnf install dyff
```

## Summary

The updated `dyff.spec` file now:
- ✅ Works with upstream GitHub sources (no custom docs)
- ✅ Works with custom sources (includes USER_GUIDE.md if present)
- ✅ Compatible with COPR build system
- ✅ No manual modifications needed
- ✅ Maintains backward compatibility with local builds

You can now build dyff in COPR without errors!

## Resources

- **COPR Documentation**: https://docs.pagure.org/copr.copr/
- **COPR Web Interface**: https://copr.fedorainfracloud.org/
- **copr-cli Documentation**: https://docs.pagure.org/copr.copr/user_documentation.html#copr-cli
- **dyff GitHub**: https://github.com/homeport/dyff
- **Fedora Packaging Guidelines**: https://docs.fedoraproject.org/en-US/packaging-guidelines/

## Support

- **COPR Issues**: https://pagure.io/copr/copr/issues
- **Fedora Packaging Help**: https://discussion.fedoraproject.org/
- **dyff Issues**: https://github.com/homeport/dyff/issues

