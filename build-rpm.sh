#!/bin/bash
# Build script for creating dyff RPM package for Fedora
# Usage: ./build-rpm.sh [version]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print with color
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Default version - can be overridden
VERSION="${1:-1.9.3}"

print_info "Building dyff RPM package version ${VERSION}"

# Check if running on Fedora or RHEL-based system
if ! command -v rpmbuild &> /dev/null; then
    print_error "rpmbuild not found. Please install it first:"
    echo "  sudo dnf install rpm-build rpmdevtools"
    exit 1
fi

# Check for Go
if ! command -v go &> /dev/null; then
    print_error "Go is not installed. Please install Go 1.23 or later:"
    echo "  sudo dnf install golang"
    exit 1
fi

GO_VERSION=$(go version | awk '{print $3}' | sed 's/go//')
print_info "Go version: ${GO_VERSION}"

# Set up RPM build environment
print_info "Setting up RPM build environment..."
rpmdev-setuptree

# Define directories
RPMBUILD_DIR="${HOME}/rpmbuild"
SOURCES_DIR="${RPMBUILD_DIR}/SOURCES"
SPECS_DIR="${RPMBUILD_DIR}/SPECS"
RPMS_DIR="${RPMBUILD_DIR}/RPMS/x86_64"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

print_info "RPM build directory: ${RPMBUILD_DIR}"

# Check if we're in a git repository
if [ -d "${SCRIPT_DIR}/.git" ]; then
    print_info "Detected git repository"
    
    # Create source tarball from git
    print_info "Creating source tarball from git repository..."
    cd "${SCRIPT_DIR}"
    
    # Create a clean export
    TEMP_DIR=$(mktemp -d)
    git archive --format=tar --prefix="dyff-${VERSION}/" HEAD | tar -x -C "${TEMP_DIR}"
    
    # Copy USER_GUIDE.md if it exists
    if [ -f "${SCRIPT_DIR}/USER_GUIDE.md" ]; then
        cp "${SCRIPT_DIR}/USER_GUIDE.md" "${TEMP_DIR}/dyff-${VERSION}/"
    fi
    
    # Create tarball
    cd "${TEMP_DIR}"
    tar czf "${SOURCES_DIR}/v${VERSION}.tar.gz" "dyff-${VERSION}/"
    
    # Cleanup
    rm -rf "${TEMP_DIR}"
    print_success "Source tarball created: ${SOURCES_DIR}/v${VERSION}.tar.gz"
else
    # If not in git repo, try to download from GitHub
    print_warning "Not in a git repository, attempting to download source from GitHub..."
    
    if command -v curl &> /dev/null; then
        curl -L -o "${SOURCES_DIR}/v${VERSION}.tar.gz" \
            "https://github.com/homeport/dyff/archive/v${VERSION}.tar.gz"
        print_success "Source tarball downloaded: ${SOURCES_DIR}/v${VERSION}.tar.gz"
    else
        print_error "curl not found. Cannot download source tarball."
        print_error "Please either:"
        print_error "  1. Run this script from the dyff git repository, or"
        print_error "  2. Install curl: sudo dnf install curl"
        exit 1
    fi
fi

# Copy spec file
print_info "Copying spec file..."
cp "${SCRIPT_DIR}/dyff.spec" "${SPECS_DIR}/dyff.spec"

# Update version in spec file if different
sed -i "s/^Version:.*/Version:        ${VERSION}/" "${SPECS_DIR}/dyff.spec"

print_success "Spec file ready: ${SPECS_DIR}/dyff.spec"

# Install build dependencies
print_info "Checking build dependencies..."
sudo dnf builddep -y "${SPECS_DIR}/dyff.spec" 2>/dev/null || {
    print_warning "Could not auto-install dependencies. Installing manually..."
    sudo dnf install -y golang >= 1.23.0 git make rpm-build rpmdevtools
}

# Build the RPM
print_info "Building RPM package..."
print_info "This may take a few minutes..."

if rpmbuild -ba "${SPECS_DIR}/dyff.spec"; then
    print_success "RPM build completed successfully!"
    
    # Find and display the built RPM
    RPM_FILE=$(find "${RPMS_DIR}" -name "dyff-${VERSION}*.rpm" -type f | head -n 1)
    SRPM_FILE=$(find "${RPMBUILD_DIR}/SRPMS" -name "dyff-${VERSION}*.src.rpm" -type f | head -n 1)
    
    if [ -n "${RPM_FILE}" ]; then
        print_success "Binary RPM: ${RPM_FILE}"
        
        # Show package info
        print_info "Package information:"
        rpm -qip "${RPM_FILE}"
        
        # Show package contents
        print_info "Package contents:"
        rpm -qlp "${RPM_FILE}"
        
        # Copy to current directory
        cp "${RPM_FILE}" "${SCRIPT_DIR}/"
        BASENAME_RPM=$(basename "${RPM_FILE}")
        print_success "RPM copied to: ${SCRIPT_DIR}/${BASENAME_RPM}"
        
        echo ""
        print_success "Build complete!"
        echo ""
        echo "To install the package:"
        echo "  sudo dnf install ${SCRIPT_DIR}/${BASENAME_RPM}"
        echo ""
        echo "Or:"
        echo "  sudo rpm -ivh ${SCRIPT_DIR}/${BASENAME_RPM}"
    fi
    
    if [ -n "${SRPM_FILE}" ]; then
        print_success "Source RPM: ${SRPM_FILE}"
        cp "${SRPM_FILE}" "${SCRIPT_DIR}/"
        BASENAME_SRPM=$(basename "${SRPM_FILE}")
        print_success "Source RPM copied to: ${SCRIPT_DIR}/${BASENAME_SRPM}"
    fi
else
    print_error "RPM build failed!"
    exit 1
fi

# Optional: Run basic tests
print_info "Running basic package tests..."

# Extract and test in temporary directory
TEST_DIR=$(mktemp -d)
cd "${TEST_DIR}"
rpm2cpio "${RPM_FILE}" | cpio -idmv 2>/dev/null

if [ -f "./usr/bin/dyff" ]; then
    print_info "Testing dyff binary..."
    if ./usr/bin/dyff version; then
        print_success "Binary test passed!"
    else
        print_warning "Binary test failed, but package was built"
    fi
fi

# Cleanup
cd "${SCRIPT_DIR}"
rm -rf "${TEST_DIR}"

print_success "All done! Your RPM package is ready."

