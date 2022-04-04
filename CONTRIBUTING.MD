# Contributing
In case you want to contribute to Delta by providing icons please do so by creating a vector-based icon, cloning this repo and issuing a pull request with regards to these points:
- Your created icon/s as __full vector__ SVG go/es to the `contributed-vectors` folder
	-  Please keep filenames in lowercase alphabet with underscores
- Add the info about the icon you added to `contributions.json` in the following format if adding a new icon:
	```json
		{
			"activity": "com.example.app/com.example.app.MainActivity",
			"drawable": "example_app", // with file extension omitted
			"label": "Example App",
		}
	```
- If you are updating the main icon of an application please add to `contributions.json` in the following way:
	```json
		{
			// example_app.png will be renamed to example_app_alt_xx.png automatically and example_app.svg converted to replace it
			// make sure the icons share the same name, if anything goes wrong we will have the previous version in the git history
			"update_drawable": "example_app"
		}
	```
- (Optional) Give yourself an entry at the bottom of `app/src/main/res/xml/contributors.xml`

## Resources for Contributions
### Color palette
Usage notes:
- Davy's grey (#56595B) as default Black
- Coral pink (#FF837D) as default Red and Fuzzy Wuzzy (#BA6561) as default Dark Red. Shades of Red are specifically for shading purposes
- Transparencies - White (25%, 50%, 70%) and Black (15%, 25%) can be used as overlay for additional shading

![Palette for Delta](https://github.com/Delta-Icons/android/raw/master/resources/Palette.svg) (Right-Click &rarr; Save as)

[Adobe Swatch Exchange Palette](https://github.com/Delta-Icons/android/raw/master/resources/Palette.ase) (Right-Click &rarr; Save as)

[GPL pallete](https://github.com/Delta-Icons/android/raw/master/resources/Palette.gpl) (Inkscape, Karbon) (Right-Click &rarr; Save as)

### Icon template
<img src="https://github.com/Delta-Icons/android/raw/master/resources/template.svg" width="177" height="177">
(Right-Click &rarr; Save as)

### Icon template tutorial
<img src="https://github.com/Delta-Icons/android/raw/master/resources/template_tutorial.svg" width="547,705" height="600">
(Right-Click &rarr; Save as)

### Font
[Now](https://www.1001fonts.com/now-font.html) (Use Now Alt from the same family for alternate lowercase "a")

### Gathering ComponentInfo from apps
- [Icon Pusher](https://iconpusher.com/) by southpaw.dev
- [Icon Request](https://github.com/Kaiserdragon2/IconRequest/releases) by [Kaiserdragon2](https://github.com/Kaiserdragon2)
