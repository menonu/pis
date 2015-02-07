# SIP実験 RSA306観測プログラム
-------------------------------
AUthor: Koji Ichikawa (ichikawa@awcc.uec.ac.jp)

##実行環境
Windows on Surface Pro 3
Python 2.7(64bit)
Tektronix RSA306API
Garmin USB 18x

##実行環境のインストールと設定
###Python
PythonはWindowsにインストール(CygwinではWindowsのライブラリが使えなかった)
必ず64bit版をインストールすること
pip


* Numpy(64bit) (Windows用のwhlパッケージ利用)
* SciPy(64bit)
###pipでインストールするパッケージ一覧
* pyserial
* pynmea

###GPS関連
* Franson GpsGate v2.6.0
Garmin USB 18xはGarmin独自形式なので変換用のソフトウェアを導入
*Franson GpsGateの設定
Input -> Garmin USB
Output -> Add output
Virtual COM Port / NMEA Filterを選択し、COM PORT 1を選択   
NMEA Filterの左側Basic settings をBlock everything but...   
右側のAdvanced settingsのCommand filterを%GPRMC、Time interval(s)を1にしてSave

##パラメータ設定
parameter.conf参照
##実行方法
main.py : IQデータの取得
streaming.py : ADC Streamingの取得
終了 Ctrl+q




