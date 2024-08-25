## Installation
Clone this repository into your hexo root directory.
```
cd Hexo
git clone git@github.com:Chen-Yulin/HexoSyncObsidian.git
```

## Configuraion
Change the directory in `sync.py`
```
obsidian_path = os.path.expanduser('~')+'/OneDrive/Common/obsidian/CYL Planet/'
hexo_path = os.path.expanduser('~')+'/Hexo/source/_obsidian/'
post_path = os.path.expanduser('~')+'/Hexo/source/_posts/'
```
Change the directory to be ignored
```
ignore = [".git", ".gitignore", ".obsidian", "template"]
```

You can also generate thumbnail for obsidian posts through
```
validTagsForThumbnail = ["Unity","nvim", "hexo", "debate", "AI", "python", "Reading"]
```
If your obsidian notes include these tags, this script will automatically add the thumbnail setting for your post
> Make sure that the `png` file exists in `/thumb` and `/gallery`

## Usage
```
cd Hexo
python /HexoSyncObsidian/sync.py
```
or use a script to automate the process of sync obsidian and deploying
```
#!/bin/sh 
python3 ./SyncObsidian/sync.py
hexo cl
hexo g
hexo d
```
