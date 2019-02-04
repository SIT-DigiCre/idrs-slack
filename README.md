# Integrated Digicre Room Service - Slack
This project aim to offer some services via Slack.

## 使用機材
* ~~Raspberry Pi Zero W~~ Raspberry Pi 3B に更新．私物です．
* Arduino互換ボード (私物の[SparkFun Pro Micro 3.3V/8MHz](https://www.sparkfun.com/products/12587)で実装)
* [曲げセンサ](https://www.sparkfun.com/products/10264)
* [電子ペーパ Waveshare 7.5inch](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT)

## 動作概要
曲げセンサをストライク部分に固定し，デッドボルトが曲げセンサを曲げることで施錠を検知，曲げセンサが元に戻ることで解錠を検知します．  
電子ペーパの制御は制御サーバ経由で行われ、更新リクエストの受付はHTTPで通信するAPIの実装を予定しています．
