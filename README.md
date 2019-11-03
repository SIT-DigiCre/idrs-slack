# Integrated Digicre Room Service - Slack
This project aim to offer some services via Slack.

## メンテナンスについて
メンテナンスに必要な情報は、このREADMEファイルか本リポジトリのwikiに記載されています。

ご質問等は、Slackの #idrs-develop チャンネルにお願いします。

## 使用機材
* ~~Raspberry Pi Zero W~~ Raspberry Pi 3B に更新．私物です．
* Arduino互換ボード (私物の[SparkFun Pro Micro 3.3V/8MHz](https://www.sparkfun.com/products/12587)で実装)
* [曲げセンサ](https://www.sparkfun.com/products/10264)
* [電子ペーパ Waveshare 7.5inch](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT)

## 動作概要
曲げセンサをストライク部分に固定し，デッドボルトが曲げセンサを曲げることで施錠を検知，曲げセンサが元に戻ることで解錠を検知します．  
電子ペーパの制御は制御サーバ経由で行われ、更新リクエストの受付はHTTPで通信するAPIの実装を予定しています．

## ツール概説
### ツールの実行について
このプロジェクトのスクリプトがdocker-composeを利用し、Docker上で実行されています。

ツールの実行は、次のようにしてDocker上で行います。

```sh
$ docker run -it --rm -v `pwd`:/script idrs-python:0.1 /script/tools/checkI2C.py
```

### tools/checkI2C.py
このスクリプトは1秒毎にセンサからの入力値そのままを出力します。

センサの値は0から255までです。
Arduino側では0から1024でアナログ入力を取得していますが、I2Cで通信する都合上、8bitに収める為に2bit右シフトを行なっています。

### tools/postMessage.py
このスクリプトはコマンドライン引数を2つ取り、第一引数にチャンネル、第二引数にメッセージの内容を与えられて、指定されたチャンネルに指定されたメッセージを送信します。
