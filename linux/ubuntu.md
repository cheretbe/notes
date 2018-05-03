```shell
sudo apt-key list
```
Example output
```
...
pub   2048R/11260BA7 2016-04-25 [expired: 2018-04-25]
uid                  Ziirish Archive Automatic Signing Key (This is the Ziirish's packaging system) <ubuntu@ziirish.info>
```
Find key ID (11260BA7) and remove it 
```shell
sudo apt-key del 11260BA7
```
