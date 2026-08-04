## Method 1: The linkedProjects Configuration (Best for Separate Projects)

This is the cleanest approach if your subfolders are completely
unrelated projects. It tells the extension exactly where to look
for your Cargo roots without modifying any project code.

1. Open your main parent folder in VS Code.
2. Open the command palette using Ctrl+Shift+P.
3. Type and select Preferences: Open Workspace Settings (JSON).
4. Add the rust-analyzer.linkedProjects setting to point to your
   sub-projects

```json
{
  "rust-analyzer.linkedProjects": [
    "./project_one/Cargo.toml",
    "./project_two/Cargo.toml",
    "./project_three/Cargo.toml"
  ]
}
```
