# SIP実験 RSA306観測プログラム
-------------------------------
Author: Koji Ichikawa (ichikawa@awcc.uec.ac.jp)

##実行環境
Windows on Surface Pro 3
Python 2.7(64bit)
Tektronix RSA306API
Garmin USB 18x

##実行環境のインストールと設定
###Python
PythonはWindowsにインストール(CygwinではWindowsのライブラリが使えなかった)
必ず64bit版をインストールすること
インストーラの設定でPathを追加->Reboot
pip


* Numpy(64bit) (Windows用のwhlパッケージ利用)
* SciPy(64bit)
###pipでインストールするパッケージ一覧
* pyserial
* pynmea

###GPS関連
* Garming USB Driver
インストールする。GPSのファームウェアアップデートとは別物
* Franson GpsGate v2.6.0
Garmin USB 18xはGarmin独自形式なので変換用のソフトウェアを導入
* Franson GpsGateの設定
Input -> Garmin USB
Output -> Add output
Virtual COM Port / NMEA Filterを選択し、COM PORT 1を選択   
NMEA Filterの左側Basic settings をBlock everything but...   
右側のAdvanced settingsのCommand filterを%GPRMC、Time interval(s)を1にしてSave

##パラメータ設定
parameter.conf参照
##実行方法
コマンドプロンプトより
main.py : IQデータの取得
mainnogps.py : IQデータの習得
streaming.py : ADC Streamingの取得
readIQ.py : IQデータの読み込み(i0 q0 i1 q0 ...)
終了 Ctrl+c

##ファイルの出力形式




