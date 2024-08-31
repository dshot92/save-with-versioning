## Save with Versioning - Blender Extension

### Description
The "Save with Versioning" Blender add-on provides a convenient way to save your Blender files with automatic versioning and publishing functionality. This add-on helps you keep track of your project's progress and easily share the latest version with your team or clients.

### Location
The `increment` and `publish` buttons can be found in two locations:
1. `View3D > Header`, beside the viewport render modes.
2. `View3D > Sidebar > Tool > Save with Versioning` panel.

### Key Features
- **Automatic Versioning**: The add-on automatically increments the version number in the file name when you save your Blender file, making it easy to keep track of changes.
- **Publish Functionality**: The published version of the file will always be the newest, up-to-date version. This allows you to link assets to the published file, while you can continue working on different incremental versions.
- **Automatic Asset Linking**: When you publish the current file, all the files that are linked to the published version will automatically get the updated version.
- **Customizable Suffixes**: You can customize the version suffix and publish suffix in the add-on preferences.
- **File List**: View a list of all versioned and published files in the current directory.
- **Open Files**: Easily open any version of your file directly from the file list.
- **Open Current Directory**: Quickly access the directory of your current file.
- **Auto-refresh**: The file list automatically updates when you load or save a file.

### Extension Preferences
You can customize the add-on's behavior by accessing the "Save with Versioning" preferences:
- **Version Suffix**: Specify the suffix used for the incremented version numbers.
- **Publish Suffix**: Specify the suffix used for the published file.

### Usage
1. **Save Increment**: Save the current file with an incremented version number.
2. **Save Publish**: Save the current file as the published version, which will be the newest, up-to-date version. Any files linked to the published version will automatically update.
3. **View File List**: Use the file list in the sidebar to see all versions of your file.
4. **Open Files**: Click the folder icon next to a file in the list to open it.
5. **Open Current Directory**: Use the "Open Current Directory" button to access your file's location.

### Example
With these preferences for suffixes:

```
version_suffix = "_v001"
publish_suffix = "_published"
file = "scene.blend"
```

| Operation    | Current File              | Resulting File                | Notes |
|--------------|---------------------------|-------------------------------|-------|
| Initial      | scene.blend               | -                             | Starting file |
| Increment    | scene.blend               | scene_v001.blend              | First version |
| Increment    | scene_v001.blend          | scene_v002.blend              | Second version |
| Publish      | scene_v002.blend          | scene_published.blend         | First published version |
| Increment    | scene_v002.blend          | scene_v003.blend              | Continue working |
| Increment    | scene_v003.blend          | scene_v004.blend              | More changes |
| Publish      | scene_v004.blend          | scene_published.blend         | Update published version |
| Increment    | scene_v004.blend          | scene_v005.blend              | Continue working |
| New Branch   | scene_v002.blend          | scene_v002_v001.blend         | Start a new branch from v002 |
| Increment    | scene_v002_v001.blend     | scene_v002_v002.blend         | Work on new branch |
| Publish      | scene_v002_v002.blend     | scene_published.blend         | Publish from new branch |