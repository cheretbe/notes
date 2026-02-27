* Player to test: https://krosbits.in/musicolet/
    * https://play.google.com/store/apps/details?id=in.krosbits.musicolet
    * https://www.techsupportalert.com/content/musicolet-music-player.htm
 
### MTP

* https://github.com/hanwen/go-mtpfs
```shell
apt install go-mtpfs
# as user
mkdir -p ~/mnt/android
go-mtpfs ~/mnt/android &
tree -d ~/mnt/android
fusermount -u ~/mnt/android
```

### Nothing Phone 3
* Отключение кнопки AI (Essential key)
   * Включить отладку по USB (как в Redmi, только тапать по номеру сборки в "Сведения о программном обеспечении")
   * источник: https://github.com/z3phydev/How-to-remap-or-disable-the-Essential-Key
   * ```shell
     wget https://dl.google.com/android/repository/platform-tools-latest-linux.zip
     unzip platform-tools-latest-linux.zip
     ./platform-tools/adb devices
     ./platform-tools/adb shell pm disable-user --user 0 com.nothing.ntessentialspace
     # должно вывести: Package com.nothing.ntessentialspace new state: disabled-user
     ./platform-tools/adb shell pm disable-user --user 0 com.nothing.ntessentialrecorder
     # должно вывести: Package com.nothing.ntessentialrecorder new state: disabled-user
     
     ./platform-tools/adb kill-server
     rm -rf platform-tools
     ```

### Xiaomi Redmi

* Режимы USB
    * `Настройки` > `О телефоне` > `Версия MIUI` (нажать 7 раз)
    * `Настройки` > `Расширенные настройки` > `Для разработчиков` > `Отладка по USB`
    * Для выключения режима разработчика в меню `Для разработчиков` выключить пункт `Режим разработчика`
* Отключение хлама
    * https://github.com/Szaki/XiaomiADBFastbootTools/releases/latest
    * Скачать `XiaomiADBFastbootTools.jar`
    * Скачать OpenJDK с https://adoptopenjdk.net/
    ```shell
    apt-cache search openjdk
    sudo apt install openjdk-18-jre
    java -jar XiaomiADBFastbootTools.jar
    ```
    * Запустить JAR
    * Режим отладки по USB должен быть включен, режим передачи данных не важен (:warning: в ВМ переподключить устройство или добавить фильтр)
* Полезные настройки
    * Поменять местами кнопки `назад` и `меню`: `Настройки` > `Расширенные настройки` > `Безграничный экран`(wtf?) > `Поменять местами кнопки`
    * https://zen.yandex.ru/media/iteasy/polnaia-optimizaciia-miui-11-i-telefon-zajil-novoi-jizniu-5ded5e46f7e01b00ad74230e?utm_source=serp
* Прошивка
    * https://4pda.to/forum/index.php?showtopic=992818&st=8640#entry108925962
    * https://root-device.ru/root-prava/xiaomi/615-xiaomi-redmi-note-9-redmi-10x-4g.html
-----

* Prevent a media directory from appearing in Android Gallery
    * create an empty file titled `.nomedia`

* https://101android.com/developer-options-settings/
* https://101android.com/full-phone-backup-adb/
* https://developer.android.com/studio/releases/platform-tools.html#download

```shell
adb backup -apk -shared -all -f C:\Users\NAME\backup.ab
adb restore C:\Users\NAME\backup.ab
```
* https://www.androidpolice.com/2019/05/13/adbs-backup-and-restore-functionality-will-go-away-in-future-android-release/

------
* https://support.samsungcloud.com/#/login
* https://www.samsung.com/global/galaxy/apps/samsung-cloud/
