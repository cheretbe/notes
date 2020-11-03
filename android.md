### Xiaomi Redmi

* Режимы USB
    * `Настройки` > `О телефоне` > `Версия MIUI` (нажать 7 раз)
    * `Настройки` > `Расширенные настройки` > `Для разработчиков` > `Отладка по USB`
    * Для выключения режима разработчика в меню `Для разработчиков` выключить пункт `Режим разработчика`
* Отключение хлама
    * https://github.com/Szaki/XiaomiADBFastbootTools/releases/latest
    * Скачать `XiaomiADBFastbootTools.jar`
    * Скачать OpenJDK с https://adoptopenjdk.net/
    * Запустить JAR
    * Режим отладки по USB должен быть включен, режим передачи данных не важен (:warning: в ВМ переподключить устройство или добавить фильтр)
* Полезные настройки
    * Поменять местами кнопки `назад` и `меню`: `Настройки` > `Расширенные настройки` > `Безграничный экран`(wtf?) > `Поменять местами кнопки`
    * https://zen.yandex.ru/media/iteasy/polnaia-optimizaciia-miui-11-i-telefon-zajil-novoi-jizniu-5ded5e46f7e01b00ad74230e?utm_source=serp
-----

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
