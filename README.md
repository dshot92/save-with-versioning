## Save with Versioning - [Blender Extension Link](https://extensions.blender.org/add-ons/save-with-versioning/)

![Save with Versioning](https://extensions.blender.org/media/thumbnails/e0/e07eea86dfb0c9c937e86f127404999676bbf969c73891198d67b40f3ea8a4bd_1920x1080.webp)

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
- **Version Suffix**: Specify the suffix used for the incremented version numbers (e.g., '_v001').
- **Publish Suffix**: Specify the suffix used for the published file (e.g., '_published').
- **Panel Category**: Choose the category where the "Save with Versioning" panel will appear in the 3D Viewport sidebar. Options include:
  - Item
  - Tool
  - View
  - Edit

### Usage
1. **Save Increment**: Save the current file with an incremented version number.
2. **Save Publish**: Save the current file as the published version, which will be the newest, up-to-date version. Any files linked to the published version will automatically update.
3. **View File List**: Use the file list in the sidebar to see all versions of your file.
4. **Open Files**: Click the folder icon next to a file in the list to open it.
5. **Open Current Directory**: Use the "Open Current Directory" button to access your file's location.
6. **Change Panel Location**: Adjust the panel's location in the 3D Viewport sidebar by changing the Panel Category in the add-on preferences.

### Versioning Example

```
v001 -> v002 -> v003 -> v004 (Current) -> ... -> v00x
         |
         └─> v002_001 -> v002_002 -> ... -> v002_00x

published (Can be updated from any version)
```

File naming:
- Main: scene_v001.blend, scene_v002.blend, etc.
- Branch: scene_v002_001.blend, scene_v002_002.blend, etc.
- Published: scene_published.blend
