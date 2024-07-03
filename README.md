## Save with Versioning - Blender Extension

### Description
The "Save with Versioning" Blender add-on provides a convenient way to save your Blender files with automatic versioning and publishing functionality. This add-on helps you keep track of your project's progress and easily share the latest version with your team or clients.

### Location
The `increment` and `publish` buttons can be found in `View3D > Header`, beside the viewport render modes.

### Key Features
- **Automatic Versioning**: The add-on automatically increments the version number in the file name when you save your Blender file, making it easy to keep track of changes.
- **Publish Functionality**: The published version of the file will always be the newest, up-to-date version. This allows you to link assets to the published file, while you can continue working on different incremental versions.
- **Automatic Asset Linking**: When you publish the current file, all the files that are linked to the published version will automatically get the updated version.
- **Customizable Suffixes**: You can customize the version suffix and publish suffix in the add-on preferences.

### Extension Preferences
You can customize the add-on's behavior by accessing the "Save with Versioning" preferences:
- **Version Suffix**: Specify the suffix used for the incremented version numbers.
- **Publish Suffix**: Specify the suffix used for the published file.

### Usage
1. **Save Increment**: Save the current file with an incremented version number.
2. **Save Publish**: Save the current file as the published version, which will be the newest, up-to-date version. Any files linked to the published version will automatically update.

### Example
With these preferences for suffices:
```
version_suffix = "_v001"
publish_suffix = "_published"
file = "scene_04.blend"
```

| Operation    | Original File              | Resulting File                |
|--------------|----------------------------|-------------------------------|
| (increment)  | scene.blend                | scene_04 **_v001**.blend      |
| (increment)  | scene **_v001**.blend      | scene_04 **_v002**.blend      |
| (publish)    | scene **_v002**.blend      | scene_04 **_published**.blend |
| (increment)  | scene **_v002**.blend      | scene_04 **_v003**.blend      |
| ... | ... | ... |
