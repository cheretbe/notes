* https://en.wikipedia.org/wiki/Blu-ray
* http://gimmor.blogspot.com/2012/10/blu-ray-ubuntu-linux.html
* http://fy.chalmers.se/~appro/linux/DVD+RW/Blu-ray/
* http://www.hughsnews.ca/faqs/authoritative-blu-ray-disc-bd-faq/9-disc-capacity
* https://wiki.gentoo.org/wiki/CD/DVD/BD_Writing

| Type                         | Diameter (cm) | Layers |	Capacity (bytes)  |
| ---------------------------- | ------------: | -----: | ----------------: |
| Standard size, single layer  | 12            | 1      | 25,025,314,816    |
| Standard size, dual layer	   | 12            | 2      | 50,050,629,632    |
| Mini disc size, single layer | 8             | 1      | 7,791,181,824     |
| Mini disc size, dual layer   | 8             | 2      | 15,582,363,648    |

Track sizes

| Disk type            |                Track Size |   Space Available|
|----------------------|--------------------------:|-----------------:|
| 25Gb BD-R            | 12219392*2KiB=25025314816 |          23.3GiB |
| Formatted 25Gb BD-RE | 11826176*2KiB=24220008448 |:warning: 22.6GiB |
| 50Gb BD-R            | 24438784*2Kib=50050629632 |         46.61GiB |
| Formatted 50Gb BD-RE | 23652352*2KiB=48440016896 |:warning: 45.1GiB |
* 1 sector is 2,048 bytes

```shell
dvd+rw-mediainfo /dev/sr0
```
