# tagesschauDownloader

Script to download news reports from http://www.tagesschau.de.

## Usage
```
# python tagesschau.py

usage: Download videos [-h] [-d DATE] [-f FILE] [-p PATH]
                       {tagesschau,tagesschau20,tagesthemen,tagesthemengebaerden}
                       {mobil_h264,klein_h264,mittel_h264,mittel_webm,gross_h264,gross_webm,hd_h264}
Download videos: error: too few arguments
```

### Example

Download the Tagestehmen in a very low mobile version from the 2017-01-01.
```
# python tagesschau.py -d 2017-01-01 tagesthemen mobil_h264
```
