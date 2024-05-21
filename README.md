
![last commit](https://img.shields.io/github/last-commit/groland11/check-gitrelease.svg)
![release date](https://img.shields.io/github/release-date/groland11/check-gitrelease.svg)
![languages](https://img.shields.io/github/languages/top/groland11/check-gitrelease.svg)
![license](https://img.shields.io/github/license/groland11/check-gitrelease.svg)

# check-gitrelease
Check if local installed version of a program is the latest release on GitHub, or if there is an update available for download.

The locally installed program needs to be referenced by a symbolic link to the downloaded executable binary which includes the version string in its filename.
For example:

```
$ ls -l ~/Downloads
lrwxrwxrwx  1 ubuntu users         29 Mär 31 15:49  digikam -> digiKam-8.2.0-x86-64.appimage
-rwxrwxr-x  1 ubuntu users  253535424 Mär 31 14:12  digiKam-8.2.0-x86-64.appimage
```
> [!NOTE]
> The script queries all tagged releases from the remote git repository and compares them to the version string of the local executable file.

Remote git release tags:
```
66b84e1ba8f8003994fa398a669e1ccc4224a901        refs/tags/v8.0.0^{}
0bfe6be695c534fafeebf916c5bd68ecccb4bfa3        refs/tags/v8.0.0-beta1
32899a31edfa223faf99b012c03190c5260efb82        refs/tags/v8.0.0-beta1^{}
5fc7a843b951e992fbc9e61c7696a45f5b1c3c24        refs/tags/v8.1.0
5d0a5e499b5cc5b9c7aa917575d1fb14e0105687        refs/tags/v8.1.0^{}
e04b87c47aa3319ed8e708668057d6b647f5303c        refs/tags/v8.2.0
d9b5f5bcf81df10de7b3b33b1fca1cd189eab79a        refs/tags/v8.2.0^{}
4724e74447f7f277d9bbb6e197adc7af0ad75c11        refs/tags/v8.3.0
9e9222fa4002acf2fcca6741b79260f01817eb30        refs/tags/v8.3.0^{}
```
Local filename:
```
digiKam-8.2.0-x86-64.appimage
```

## Why not web scraping?
You could also use the BeautifulSoup4 Python module to extract version information from a website, but web scraping has several disadvantages:
- The URL of websites changes over time, so you need to continuously adapt your script.
- HTML content or structure can change as well without notice.
- Project websites get outdated or are not maintained any longer.

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
$ ls -l ~/Downloads
lrwxrwxrwx  1 ubuntu users         29 Mär 31 15:49  digikam -> digiKam-8.2.0-x86-64.appimage
...
$ check-gitrelease.py -l ~/Downloads/digikam -r https://invent.kde.org/graphics/digikam
There is a new version 8.3.0 available for download at https://invent.kde.org/graphics/digikam. Please update!

```
