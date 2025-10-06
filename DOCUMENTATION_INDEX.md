# dyff Documentation Index

## Overview

This repository contains comprehensive documentation and packaging materials for **dyff** - a diff tool for YAML files (and sometimes JSON).

## Documentation Files

### 📚 User Documentation

#### 1. [QUICKSTART.md](QUICKSTART.md)
**Quick reference for common tasks**
- Installation instructions
- Basic command examples
- Common use cases
- Integration snippets
- Flag reference

**Who it's for**: Users who need quick answers and common command examples.

#### 2. [USER_GUIDE.md](USER_GUIDE.md)
**Comprehensive user manual** (10 chapters, ~800 lines)
- Complete command reference
- Detailed usage examples
- Advanced features and techniques
- Integration with kubectl, git, CI/CD
- Troubleshooting guide
- Tips and best practices

**Who it's for**: All users, from beginners to advanced. The definitive dyff reference.

#### 3. [README.md](README.md)
**Project README**
- Project overview
- Basic examples
- Installation methods
- Contributing guidelines

**Who it's for**: First-time visitors, contributors.

### 📦 Packaging Documentation

#### 4. [PACKAGING.md](PACKAGING.md)
**Packaging overview and workflow**
- Files overview
- Quick start for RPM building
- Package contents
- Distribution options
- CI/CD integration examples
- Maintenance procedures

**Who it's for**: Package maintainers and distributors.

#### 5. [RPM_BUILD_INSTRUCTIONS.md](RPM_BUILD_INSTRUCTIONS.md)
**Detailed RPM building guide** (comprehensive)
- Prerequisites and system requirements
- Step-by-step build instructions
- Manual and automated processes
- Installation and verification
- Troubleshooting build issues
- Distribution methods
- Advanced topics (Mock, Copr, signing)

**Who it's for**: RPM package builders and Fedora packagers.

### 🔧 Packaging Files

#### 6. [dyff.spec](dyff.spec)
**RPM specification file**
- Package metadata
- Build instructions
- Installation rules
- Man page generation
- Changelog

**Technical file**: Used by rpmbuild to create RPM packages.

#### 7. [build-rpm.sh](build-rpm.sh)
**Automated RPM build script**
- Environment setup
- Dependency installation
- Source tarball creation
- RPM building
- Testing and verification

**Usage**: `./build-rpm.sh [version]`

## Quick Navigation

### I want to...

#### Use dyff
- **Just starting?** → [QUICKSTART.md](QUICKSTART.md)
- **Need detailed info?** → [USER_GUIDE.md](USER_GUIDE.md)
- **Learn basics?** → [README.md](README.md)

#### Build RPM Package
- **First time?** → [PACKAGING.md](PACKAGING.md) (Quick Start section)
- **Need full instructions?** → [RPM_BUILD_INSTRUCTIONS.md](RPM_BUILD_INSTRUCTIONS.md)
- **Just build it!** → Run `./build-rpm.sh`

#### Distribute or Maintain
- **Package overview?** → [PACKAGING.md](PACKAGING.md)
- **Update version?** → Edit [dyff.spec](dyff.spec) and run [build-rpm.sh](build-rpm.sh)
- **Create repository?** → [RPM_BUILD_INSTRUCTIONS.md](RPM_BUILD_INSTRUCTIONS.md) (Distribution section)

#### Integrate with Tools
- **kubectl?** → [USER_GUIDE.md](USER_GUIDE.md) (Integration section) or [QUICKSTART.md](QUICKSTART.md)
- **Git?** → [USER_GUIDE.md](USER_GUIDE.md) (Integration section)
- **CI/CD?** → [USER_GUIDE.md](USER_GUIDE.md) + [PACKAGING.md](PACKAGING.md)

#### Troubleshoot
- **Usage issues?** → [USER_GUIDE.md](USER_GUIDE.md) (Troubleshooting section)
- **Build issues?** → [RPM_BUILD_INSTRUCTIONS.md](RPM_BUILD_INSTRUCTIONS.md) (Troubleshooting section)

## File Relationships

```
Documentation Structure:

User Path:
  QUICKSTART.md → USER_GUIDE.md → README.md
  (Quick ref)     (Comprehensive)   (Overview)

Builder Path:
  PACKAGING.md → RPM_BUILD_INSTRUCTIONS.md → build-rpm.sh → dyff.spec
  (Overview)     (Detailed instructions)      (Automation)    (Spec file)

All Documentation:
  DOCUMENTATION_INDEX.md (this file)
  └─ Points to all documentation
```

## Documentation Statistics

| File | Lines | Size | Purpose |
|------|-------|------|---------|
| QUICKSTART.md | ~100 | ~3 KB | Quick reference |
| USER_GUIDE.md | ~800 | ~42 KB | Complete manual |
| PACKAGING.md | ~500 | ~18 KB | Packaging overview |
| RPM_BUILD_INSTRUCTIONS.md | ~700 | ~30 KB | Build guide |
| dyff.spec | ~200 | ~8 KB | RPM spec |
| build-rpm.sh | ~250 | ~9 KB | Build script |

**Total Documentation**: ~2,500 lines, ~110 KB

## Quick Start by Role

### End User
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Install dyff: `sudo dnf install ./dyff-*.rpm`
3. Try: `dyff between file1.yml file2.yml`
4. Read [USER_GUIDE.md](USER_GUIDE.md) for advanced usage

### System Administrator
1. Review [PACKAGING.md](PACKAGING.md)
2. Build RPM: `./build-rpm.sh`
3. Distribute: See [RPM_BUILD_INSTRUCTIONS.md](RPM_BUILD_INSTRUCTIONS.md) Distribution section
4. Deploy to systems: `sudo dnf install dyff`

### Package Maintainer
1. Read [PACKAGING.md](PACKAGING.md)
2. Follow [RPM_BUILD_INSTRUCTIONS.md](RPM_BUILD_INSTRUCTIONS.md)
3. Customize [dyff.spec](dyff.spec) if needed
4. Use [build-rpm.sh](build-rpm.sh) for automation

### Developer Integrating dyff
1. Skim [USER_GUIDE.md](USER_GUIDE.md) Integration section
2. See examples in [QUICKSTART.md](QUICKSTART.md)
3. Reference specific sections in [USER_GUIDE.md](USER_GUIDE.md)

## Installation Quick Reference

### Install from RPM
```bash
sudo dnf install ./dyff-*.rpm
```

### Build RPM
```bash
./build-rpm.sh
```

### Verify Installation
```bash
dyff version
man dyff
```

## Getting Help

### Command Help
```bash
dyff --help
dyff between --help
man dyff
```

### Documentation Help
- Start with: [QUICKSTART.md](QUICKSTART.md)
- Deep dive: [USER_GUIDE.md](USER_GUIDE.md)
- Build issues: [RPM_BUILD_INSTRUCTIONS.md](RPM_BUILD_INSTRUCTIONS.md)

### Online Resources
- **GitHub**: https://github.com/homeport/dyff
- **Issues**: https://github.com/homeport/dyff/issues
- **Discussions**: https://github.com/homeport/dyff/discussions

## Documentation Updates

### Last Updated
- **Date**: October 6, 2025
- **dyff Version**: 1.9.3
- **Documentation Version**: 1.0

### Maintenance
To update documentation:
1. Edit relevant .md files
2. Update version numbers if needed
3. Test all examples and commands
4. Update this index if structure changes

## Contributing to Documentation

Improvements welcome! When contributing:
1. Keep existing structure
2. Update this index for new files
3. Test all code examples
4. Follow markdown style
5. Update "Last Updated" section

## License

All documentation is provided under the MIT License, matching the dyff project.

---

**Navigation**: [Top](#dyff-documentation-index) | [User Docs](#-user-documentation) | [Packaging](#-packaging-documentation) | [Quick Start](#quick-start-by-role)

