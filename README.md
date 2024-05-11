
![last commit](https://img.shields.io/github/last-commit/groland11/check-gitrelease.svg)
![release date](https://img.shields.io/github/release-date/groland11/check-gitrelease.svg)
![languages](https://img.shields.io/github/languages/top/groland11/check-gitrelease.svg)
![license](https://img.shields.io/github/license/groland11/check-gitrelease.svg)

# check-gitrelease
Check if local installed version of a program is the latest release on GitHub, or if there is an update available for download.

The local installed program needs to be a symbolic link to the downloaded version that includes the version string in its program name.

```
$ ls -l ~/Downloads
lrwxrwxrwx  1 ubuntu users         29 Mär 31 15:49  digikam -> digiKam-8.2.0-x86-64.appimage
-rwxrwxr-x  1 ubuntu users  253535424 Mär 31 14:12  digiKam-8.2.0-x86-64.appimage
```

The script queries all tagged releases from the remote git repository and compares the latest release version string with the version string from the local file.

## Why not web scraping?
You can also use the Python BeautifulSoup4 module to extract version information from a website, but web scraping has several disadvantages:
- The URL of those websites changes over time, and you have to continuously adapt your script.
- The contents or HTML structure of websites can change too.
- Project websites are sometimes outdated or not maintained any longer.

## Usage
```
./check-gitrelease.py -h
usage: check-gitrelease.py [-h] [-d] [-v] -l LOCAL -r REMOTE [-p PROXY] [-V]

Compare locally installed version of a program with latest release on GitHub

options:
  -h, --help            show this help message and exit
  -d, --debug           generate additional debug information
  -v, --verbose         increase output verbosity
  -l LOCAL, --local LOCAL
                        symbolic link to program file, e.g. /opt/app/application
  -r REMOTE, --remote REMOTE
                        remote git repository, e.g. https://invent.kde.org/graphics/digikam
  -p PROXY, --proxy PROXY
                        proxy, e.g. http://proxy.example.com:8080
  -V, --version         show program's version number and exit
```


## Example:
```
$ check-gitrelease.py -l ~/Downloads/digikam -r https://invent.kde.org/graphics/digikam
There is a new version 8.3.0 available for download at https://invent.kde.org/graphics/digikam. Please update!

```
