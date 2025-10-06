# dyff Quick Start Guide

## Installation

### From RPM (Fedora/RHEL)
```bash
sudo dnf install ./dyff-*.rpm
```

### From Source
```bash
go install github.com/homeport/dyff/cmd/dyff@latest
```

## Basic Commands

### Compare Files
```bash
dyff between old.yml new.yml
```

### Convert YAML to JSON
```bash
dyff json config.yml
```

### Convert JSON to YAML
```bash
dyff yaml config.json
```

### Pretty Print YAML
```bash
dyff yaml config.yml
```

### Restructure YAML Keys
```bash
dyff yaml --restructure --in-place config.yml
```

## Common Use Cases

### Compare with Remote File
```bash
dyff between local.yml https://example.com/remote.yml
```

### Compare from stdin
```bash
cat config.yml | dyff between - other.yml
```

### Brief Output
```bash
dyff between --output brief old.yml new.yml
```

### Ignore Order Changes
```bash
dyff between --ignore-order-changes old.yml new.yml
```

### Filter to Specific Path
```bash
dyff between --filter /spec old.yml new.yml
```

### Exclude Paths
```bash
dyff between --exclude /metadata old.yml new.yml
```

## kubectl Integration

```bash
export KUBECTL_EXTERNAL_DIFF="dyff between --omit-header --set-exit-code"
kubectl diff -f deployment.yml
```

## Git Integration

```bash
# Setup
git config --local diff.dyff.command 'dyff_between() { dyff --color on between --omit-header "$2" "$5"; }; dyff_between'
echo '*.yml diff=dyff' >> .gitattributes

# Use
git diff config.yml
```

## Output Formats

- `--output human` - Default, colorful, detailed
- `--output brief` - Concise summary
- `--output github` - GitHub PR format
- `--output gitlab` - GitLab MR format
- `--output gitea` - Gitea format

## Common Flags

| Flag | Description |
|------|-------------|
| `-o, --output` | Output format |
| `-i, --ignore-order-changes` | Ignore list order |
| `-s, --set-exit-code` | Exit 0/1 based on diff |
| `-b, --omit-header` | Skip header |
| `--filter` | Include only paths |
| `--exclude` | Exclude paths |
| `-c, --color` | on/off/auto |

## Get Help

```bash
dyff --help
dyff between --help
man dyff
```

## Documentation

- Full User Guide: `USER_GUIDE.md`
- RPM Building: `RPM_BUILD_INSTRUCTIONS.md`
- Packaging Info: `PACKAGING.md`
- Online: https://github.com/homeport/dyff

