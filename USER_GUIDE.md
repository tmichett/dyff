# dyff User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Concepts](#basic-concepts)
4. [Commands Reference](#commands-reference)
5. [Common Use Cases](#common-use-cases)
6. [Advanced Features](#advanced-features)
7. [Configuration and Flags](#configuration-and-flags)
8. [Integration with Other Tools](#integration-with-other-tools)
9. [Troubleshooting](#troubleshooting)
10. [Examples](#examples)

---

## Introduction

**dyff** (pronounced /ˈdʏf/) is a powerful diff tool specifically designed for YAML files, with support for JSON as well. Unlike traditional diff tools, dyff understands the structure of YAML/JSON documents and presents differences in a human-readable format.

### Key Features

- **Structured Comparison**: Understands YAML/JSON structure, not just line-by-line text
- **Multiple Output Formats**: Human-readable, GitHub, GitLab, Gitea, and brief formats
- **Path Reference Syntax**: Uses Spruce dot-style or go-patch path syntax for precise location references
- **Format Conversion**: Convert between YAML and JSON while preserving key order
- **Kubernetes Integration**: Special support for Kubernetes resources with entity detection
- **Color Output**: Beautiful, readable output with syntax highlighting
- **Flexible Input**: Supports local files, remote URLs, and stdin
- **Certificate Inspection**: Can parse and display differences in X.509 certificates

---

## Installation

### RPM Package (Fedora/RHEL/CentOS)

If you have the RPM package:

```bash
sudo dnf install dyff-*.x86_64.rpm
```

### From Pre-built Binaries

Download the latest release from GitHub:

```bash
curl -LO https://github.com/homeport/dyff/releases/latest/download/dyff_linux_amd64.tar.gz
tar -xzf dyff_linux_amd64.tar.gz
sudo mv dyff /usr/local/bin/
```

### Using Go

If you have Go 1.23 or later installed:

```bash
go install github.com/homeport/dyff/cmd/dyff@latest
```

### Verify Installation

```bash
dyff version
```

---

## Basic Concepts

### Path Syntax

dyff uses two types of path syntax to reference locations in YAML/JSON documents:

1. **Spruce Dot-Style** (default): `some.path.in.the.file`
   - Simple and readable
   - Uses dots to separate levels
   - Example: `metadata.name`

2. **Go-Patch Style** (use `--use-go-patch-style` flag): `/some/name=path/in/the/id=file`
   - More powerful for complex structures
   - Can specify identifiers in lists
   - Example: `/metadata/labels/name=app`

### Difference Types

dyff identifies several types of changes:

- **Addition (+)**: New content added
- **Removal (-)**: Content deleted
- **Modification (±)**: Content changed
- **Order Change**: Items reordered in a list
- **Type Change**: Value type changed (e.g., string to integer)

### Input Sources

dyff accepts input from multiple sources:

- **Local files**: `/path/to/file.yml`
- **Remote URLs**: `https://example.com/config.yaml`
- **Standard input**: `-` (dash)

---

## Commands Reference

### dyff between

Compare two YAML/JSON files and show differences.

**Syntax:**
```bash
dyff between [flags] <from> <to>
```

**Basic Example:**
```bash
dyff between old-config.yml new-config.yml
```

**Common Flags:**
- `-o, --output <style>`: Output format (human, brief, github, gitlab, gitea)
- `-i, --ignore-order-changes`: Ignore order changes in lists
- `-s, --set-exit-code`: Exit with code 0 (no diff), 1 (differences), 255 (error)
- `-b, --omit-header`: Omit the summary header
- `--swap`: Swap the from and to files
- `--chroot <path>`: Change the root level to a specific path in the document

### dyff yaml

Convert files to YAML format or pretty-print YAML.

**Syntax:**
```bash
dyff yaml [flags] <file-location> ...
```

**Examples:**
```bash
# Convert JSON to YAML
dyff yaml config.json

# Pretty-print YAML with syntax highlighting
dyff yaml config.yml

# Restructure keys in a more logical order
dyff yaml --restructure config.yml

# Modify file in-place
dyff yaml --restructure --in-place config.yml

# Convert from stdin
cat config.json | dyff yaml -
```

**Flags:**
- `-p, --plain`: Output without syntax highlighting
- `-r, --restructure`: Reorder map keys in a logical order
- `-i, --in-place`: Overwrite the input file
- `-O, --omit-indent-helper`: Omit indent helper lines

### dyff json

Convert files to JSON format or pretty-print JSON.

**Syntax:**
```bash
dyff json [flags] <file-location> ...
```

**Examples:**
```bash
# Convert YAML to JSON
dyff json config.yml

# Pretty-print JSON with syntax highlighting
dyff json config.json

# Convert from stdin
cat config.yml | dyff json -

# Save to file
dyff json config.yml > config.json
```

**Flags:**
Same as `dyff yaml` command.

### dyff last-applied

Compare Kubernetes resource with its last-applied configuration.

**Syntax:**
```bash
dyff last-applied [flags] <kubernetes-resource.yml>
```

**Example:**
```bash
kubectl get deployment myapp -o yaml | dyff last-applied -
```

This command extracts the `kubectl.kubernetes.io/last-applied-configuration` annotation and compares it with the current state.

### dyff version

Display the version of dyff.

**Syntax:**
```bash
dyff version
```

---

## Common Use Cases

### 1. Compare Configuration Files

```bash
dyff between production.yml staging.yml
```

### 2. Review Changes Before Applying

```bash
# Compare local changes to remote version
dyff between \
  https://raw.githubusercontent.com/org/repo/main/config.yml \
  local-config.yml
```

### 3. Kubernetes Diff with kubectl

Set up dyff as the external diff tool for kubectl:

```bash
export KUBECTL_EXTERNAL_DIFF="dyff between --omit-header --set-exit-code"
kubectl diff -f deployment.yml
```

### 4. Git Integration

Compare YAML files in Git repositories:

```bash
# Setup
git config --local diff.dyff.command 'dyff_between() { dyff --color on between --omit-header "$2" "$5"; }; dyff_between'
echo '*.yml diff=dyff' >> .gitattributes
echo '*.yaml diff=dyff' >> .gitattributes

# Use
git diff HEAD~1 HEAD config.yml
git show --ext-diff HEAD
git log --ext-diff -u -p path/to/file.yml
```

### 5. CI/CD Pipeline Integration

```bash
# In your CI script
if ! dyff between --set-exit-code expected.yml actual.yml; then
  echo "Configuration mismatch detected!"
  exit 1
fi
```

### 6. Convert Between Formats

```bash
# YAML to JSON
dyff json deployment.yml > deployment.json

# JSON to YAML
dyff yaml config.json > config.yml

# Multiple files
dyff yaml *.json
```

### 7. Restructure YAML Files

Reorder keys in a more human-friendly way:

```bash
# Preview changes
dyff yaml --restructure messy-config.yml

# Apply changes
dyff yaml --restructure --in-place messy-config.yml
```

### 8. Compare Specific Sections

Use `--chroot` to compare only a specific section:

```bash
dyff between --chroot /spec/template old.yml new.yml
```

---

## Advanced Features

### Filtering and Excluding Paths

#### Include Specific Paths

```bash
# Only show differences under specific paths
dyff between --filter /metadata --filter /spec from.yml to.yml
```

#### Exclude Specific Paths

```bash
# Ignore differences in metadata
dyff between --exclude /metadata from.yml to.yml

# Multiple exclusions
dyff between \
  --exclude /metadata/creationTimestamp \
  --exclude /metadata/generation \
  from.yml to.yml
```

#### Using Regular Expressions

```bash
# Filter using regex
dyff between --filter-regexp 'spec\..*\.image' from.yml to.yml

# Exclude using regex
dyff between --exclude-regexp 'metadata\.(uid|generation)' from.yml to.yml
```

### Kubernetes-Specific Features

#### Entity Detection

Automatically enabled when using `KUBECTL_EXTERNAL_DIFF`, or manually:

```bash
dyff between --detect-kubernetes deployment-v1.yml deployment-v2.yml
```

This helps dyff identify Kubernetes resources by name, namespace, and kind.

#### Additional Identifiers

For custom resources or complex lists:

```bash
dyff between \
  --additional-identifier app \
  --additional-identifier component \
  from.yml to.yml
```

### Rename Detection

dyff can detect when resources are renamed:

```bash
dyff between --detect-renames old.yml new.yml
```

### Ignoring Changes

#### Ignore Order Changes

```bash
dyff between --ignore-order-changes from.yml to.yml
```

Useful when the order of list items doesn't matter.

#### Ignore Whitespace Changes

```bash
dyff between --ignore-whitespace-changes from.yml to.yml
```

#### Ignore Value Changes

Show only structural changes (additions/removals):

```bash
dyff between --ignore-value-changes from.yml to.yml
```

### Output Customization

#### Brief Output

Get a concise summary:

```bash
dyff between --output brief from.yml to.yml
```

#### GitHub-Style Output

For GitHub PR comments:

```bash
dyff between --output github from.yml to.yml
```

#### GitLab-Style Output

For GitLab MR comments:

```bash
dyff between --output gitlab from.yml to.yml
```

#### No Table Style

Display side-by-side comparisons in single column:

```bash
dyff between --no-table-style from.yml to.yml
```

### Working with Certificates

dyff can inspect X.509 certificates and show meaningful differences:

```bash
dyff between old-cert.yml new-cert.yml
```

To treat certificates as plain text instead:

```bash
dyff between --no-cert-inspection old-cert.yml new-cert.yml
```

---

## Configuration and Flags

### Global Flags

These flags work with all commands:

| Flag | Short | Description |
|------|-------|-------------|
| `--color <on\|off\|auto>` | `-c` | Control color output |
| `--truecolor <on\|off\|auto>` | `-t` | Control true color (24-bit) output |
| `--fixed-width <number>` | `-w` | Set fixed terminal width |
| `--preserve-key-order-in-json` | `-k` | Preserve key order in JSON (non-standard) |

### Compare Flags (between, last-applied)

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--ignore-order-changes` | `-i` | false | Ignore order changes in lists |
| `--ignore-whitespace-changes` | | false | Ignore leading/trailing whitespace |
| `--detect-kubernetes` | | true | Enable Kubernetes entity detection |
| `--additional-identifier` | | | Add custom identifiers for list items |
| `--filter` | | | Filter to specific paths |
| `--exclude` | | | Exclude specific paths |
| `--filter-regexp` | | | Filter using regex |
| `--exclude-regexp` | | | Exclude using regex |
| `--ignore-value-changes` | `-v` | false | Show only structural changes |
| `--detect-renames` | | true | Detect renamed resources |

### Output Flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--output` | `-o` | human | Output style: human, brief, github, gitlab, gitea |
| `--use-indent-lines` | | true | Show indent guide lines |
| `--omit-header` | `-b` | false | Omit summary header |
| `--set-exit-code` | `-s` | false | Set exit code based on differences |
| `--no-table-style` | `-l` | false | Use single column layout |
| `--no-cert-inspection` | `-x` | false | Disable certificate inspection |
| `--use-go-patch-style` | `-g` | false | Use go-patch path syntax |

### Input Modification Flags (between only)

| Flag | Description |
|------|-------------|
| `--swap` | Swap from and to files |
| `--chroot <path>` | Change root to specific path |
| `--chroot-of-from <path>` | Change root of from file only |
| `--chroot-of-to <path>` | Change root of to file only |
| `--chroot-list-to-documents` | Treat list at chroot as multiple documents |

---

## Integration with Other Tools

### kubectl

**Method 1: Environment Variable (kubectl >= 1.20)**

```bash
export KUBECTL_EXTERNAL_DIFF="dyff between --omit-header --set-exit-code"
kubectl diff -f resource.yml
```

**Method 2: Wrapper Script (kubectl < 1.20)**

Create `/usr/local/bin/kubectl-dyff`:

```bash
#!/bin/bash
dyff between --omit-header --set-exit-code "$@"
```

```bash
chmod +x /usr/local/bin/kubectl-dyff
export KUBECTL_EXTERNAL_DIFF="kubectl-dyff"
```

### Git

**Setup:**

```bash
# Add to .gitconfig or .git/config
git config diff.dyff.command 'dyff_between() { dyff --color on between --omit-header "$2" "$5"; }; dyff_between'

# Add to .gitattributes
echo '*.yml diff=dyff' >> .gitattributes
echo '*.yaml diff=dyff' >> .gitattributes
```

**Usage:**

```bash
git diff config.yml
git show HEAD:config.yml
git log --ext-diff -p -- config.yml
```

### CI/CD Systems

**GitHub Actions:**

```yaml
- name: Compare configurations
  run: |
    dyff between --output github old.yml new.yml || true
```

**GitLab CI:**

```yaml
compare:
  script:
    - dyff between --output gitlab old.yml new.yml || true
```

**Generic CI:**

```bash
# Exit with error if differences found
dyff between --set-exit-code expected.yml actual.yml
```

### Vim/Neovim

Set dyff as diff tool:

```vim
set diffexpr=DyffDiff()
function DyffDiff()
  let opt = ""
  if &diffopt =~ "icase"
    let opt = opt . " --ignore-whitespace-changes"
  endif
  silent execute "!dyff --color off between --omit-header " . opt . " " . v:fname_in . " " . v:fname_new . " > " . v:fname_out
endfunction
```

### Helm

Compare Helm chart outputs:

```bash
helm template myapp ./mychart > old.yml
# Make changes to chart
helm template myapp ./mychart > new.yml
dyff between old.yml new.yml
```

---

## Troubleshooting

### Common Issues

#### Issue: No color output

**Solution:**
```bash
# Force color on
dyff --color on between file1.yml file2.yml

# Check if output is being piped (disables color by default)
dyff between file1.yml file2.yml | less -R
```

#### Issue: Terminal width too narrow

**Solution:**
```bash
# Set fixed width
dyff --fixed-width 120 between file1.yml file2.yml

# Disable table style for narrow terminals
dyff between --no-table-style file1.yml file2.yml
```

#### Issue: Too many differences shown

**Solution:**
```bash
# Use brief output
dyff between --output brief file1.yml file2.yml

# Filter to specific paths
dyff between --filter /spec file1.yml file2.yml
```

#### Issue: Certificate comparison not working

**Solution:**
```bash
# Disable certificate inspection if needed
dyff between --no-cert-inspection cert1.yml cert2.yml
```

#### Issue: kubectl diff not working with dyff

**Solution:**
```bash
# Make sure KUBECTL_EXTERNAL_DIFF is set correctly
echo $KUBECTL_EXTERNAL_DIFF

# Test dyff directly
dyff between <(kubectl get deploy myapp -o yaml) deploy.yml
```

### Error Messages

#### "failed to load input files"

- Check file paths are correct
- Verify files are valid YAML/JSON
- Check remote URLs are accessible
- Verify file permissions

#### "failed to compare input files"

- Ensure files have compatible structure
- Check for malformed YAML/JSON
- Try with `--plain` flag to see raw content

#### "unknown output style"

- Valid styles: human, brief, github, gitlab, gitea
- Check spelling and case sensitivity

---

## Examples

### Example 1: Basic File Comparison

**Files:**

`from.yml`:
```yaml
name: myapp
version: 1.0.0
config:
  replicas: 3
  image: nginx:1.19
```

`to.yml`:
```yaml
name: myapp
version: 1.0.1
config:
  replicas: 5
  image: nginx:1.20
  debug: true
```

**Command:**
```bash
dyff between from.yml to.yml
```

**Output:**
```
     _        __  __
   _| |_   _ / _|/ _|
 / _' | | | | |_| |_
| (_| | |_| |  _|  _|
 \__,_|\__, |_| |_|
       |___/

(comparison between from.yml and to.yml)

version
  ± value change
    - 1.0.0
    + 1.0.1

config.replicas
  ± value change
    - 3
    + 5

config.image
  ± value change
    - nginx:1.19
    + nginx:1.20

config.debug
  + one added entry
    + true
```

### Example 2: Kubernetes Deployment Comparison

```bash
dyff between \
  --detect-kubernetes \
  --exclude /metadata/generation \
  --exclude /metadata/resourceVersion \
  old-deployment.yml \
  new-deployment.yml
```

### Example 3: Remote File Comparison

```bash
dyff between \
  https://raw.githubusercontent.com/org/repo/v1.0/config.yml \
  https://raw.githubusercontent.com/org/repo/v2.0/config.yml
```

### Example 4: Compare with Standard Input

```bash
curl -s https://example.com/config.yml | dyff between - local-config.yml
```

### Example 5: Pipeline Processing

```bash
# Convert JSON stream to YAML
curl -s https://api.example.com/config | jq '.data' | dyff yaml -

# Chain multiple operations
cat config.json | dyff yaml - | grep -A5 "database"
```

### Example 6: Automation Script

```bash
#!/bin/bash
# compare-configs.sh

set -euo pipefail

FROM_FILE="$1"
TO_FILE="$2"

echo "Comparing configurations..."
if dyff between --set-exit-code "$FROM_FILE" "$TO_FILE"; then
  echo "✓ No differences found"
  exit 0
else
  EXIT_CODE=$?
  if [ $EXIT_CODE -eq 1 ]; then
    echo "⚠ Differences detected"
    exit 1
  else
    echo "✗ Error occurred"
    exit $EXIT_CODE
  fi
fi
```

### Example 7: Compare Specific Section

```bash
# Compare only the spec section
dyff between \
  --chroot /spec \
  deployment-v1.yml \
  deployment-v2.yml
```

### Example 8: Multi-format Conversion

```bash
#!/bin/bash
# convert-all-to-yaml.sh

for file in *.json; do
  dyff yaml "$file" > "${file%.json}.yml"
  echo "Converted: $file -> ${file%.json}.yml"
done
```

---

## Tips and Best Practices

### 1. Use Appropriate Output Format

- **Human**: Interactive terminal use, best readability
- **Brief**: Quick overview, ideal for CI/CD logs
- **GitHub/GitLab/Gitea**: For PR/MR comments with proper syntax highlighting

### 2. Set Exit Codes in Automation

Always use `--set-exit-code` in scripts and CI/CD:

```bash
dyff between --set-exit-code expected.yml actual.yml
```

### 3. Optimize Performance

For large files:
- Use `--filter` to compare only relevant sections
- Use `--brief` output for faster processing
- Consider `--ignore-order-changes` if order doesn't matter

### 4. Color in CI/CD

Most CI/CD systems support ANSI colors. Force colors if needed:

```bash
dyff --color on between file1.yml file2.yml
```

### 5. Preserve Key Order

When key order matters (like Kubernetes manifests):

```bash
dyff yaml --preserve-key-order-in-json config.json
```

### 6. Combine with Other Tools

```bash
# With jq
curl -s api.example.com/data | jq '.config' | dyff yaml -

# With yq
yq eval '.spec' deployment.yml | dyff yaml -

# With kubectl
kubectl get deploy myapp -o json | dyff yaml -
```

### 7. Document Your Integration

When integrating dyff into projects, document the usage:

```markdown
## Comparing Configurations

Use dyff to compare configuration files:

\`\`\`bash
dyff between config/production.yml config/staging.yml
\`\`\`
```

---

## Appendix

### Path Syntax Examples

**Spruce Style:**
- `metadata.name`
- `spec.template.spec.containers.[0].image`
- `config.database.host`

**Go-Patch Style:**
- `/metadata/name`
- `/spec/template/spec/containers/name=app/image`
- `/spec/ports/port=8080/protocol`

### Exit Codes

When using `--set-exit-code`:

- `0`: No differences detected
- `1`: Differences found
- `255`: Error occurred

### Supported File Formats

- YAML (.yml, .yaml)
- JSON (.json)
- Supports multi-document YAML files
- Automatically detects format

### Color Schemes

dyff uses colors based on the Atom editor scheme:
- **Green**: Additions
- **Red**: Removals
- **Yellow**: Modifications
- **Blue**: Keys and structure
- **Gray**: Helper lines and context

### Performance Considerations

- Large files (>10MB): Use `--filter` or `--chroot`
- Many differences (>1000): Consider `--brief` output
- Remote files: Downloaded once and cached in memory
- Stdin: Fully read into memory before processing

---

## Getting Help

### Command Help

```bash
# General help
dyff --help

# Command-specific help
dyff between --help
dyff yaml --help
dyff json --help
```

### Community and Support

- **GitHub Issues**: https://github.com/homeport/dyff/issues
- **GitHub Discussions**: https://github.com/homeport/dyff/discussions
- **Documentation**: https://github.com/homeport/dyff

### Reporting Bugs

When reporting issues, include:
1. dyff version (`dyff version`)
2. Operating system and version
3. Sample files (if possible)
4. Full command used
5. Expected vs actual output

---

## License

dyff is released under the MIT License. See LICENSE file for details.

Copyright (c) 2019 The Homeport Team

