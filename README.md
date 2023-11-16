# VISSIM2CZML

PTV Groupが開発・販売しているミクロ交通シミュレーター[PTV Vissim](https://www.ptvgroup.com/ja/products/ptv-vissim)が出力する車両軌跡（.fzp）及び歩行者軌跡（*.pp）データをCZML形式に変換します。
国土交通省が主導するプロジェクト[PLATEAU](https://www.mlit.go.jp/plateau/)で公開しているPLATEAU Viewにインポートすることで、3D都市モデルや土砂災害、洪水・津波被害等とともにアニメーションを可視化することができます。

## ファイル構成
```txt
root  
　├ input
　│　├ ***.fzp
　│　├ ***.pp
　├ output  	※自動生成される
　│　├ ***.fzp.czml
　│　└ ***.pp.czml
　├ requirements.txt
　└ Vissim2CZML.py
```
### Vissim2CZML.py：  
　コマンドラインから呼び出すPythonファイル。fzp、ppファイルを読込み、PLATEAU Viewに読込可能なczml形式で出力する。 

## 使い方

#### ①VissimでBing Maps等の衛星写真に合わせてシミュレーションモデルを作成
衛星写真と道路ネットワークの位置を一致させる。
![image](https://github.com/MototsuguMiura/VISSIM2CZML/assets/85535019/828e2c88-94db-4ca2-8032-c9371d403a2d)

#### ②緯度・経度のユーザー定義属性（UDA)が設定されたファイルを追加読込
デフォルトの設定では、下記フォルダにファイルが存在する。<br />
C:\Users\Public\Documents\PTV Vision\PTV Vissim 2023\Examples Training\Evaluation\WGS Coordinates.UDA
![image](https://github.com/MototsuguMiura/VISSIM2CZML/assets/85535019/9286bf0e-d5aa-4247-9f98-179d0236e80f)

#### ③評価の設定（Evaluation-configuration)で出力する属性を選択
順不同だが、属性が不足していると変換時にエラーが発生するので注意。<br />
保存周期（Resolution）を細かくするとデータサイズが膨大になり、変換にかかる時間も長くなるので注意。<br /><br />
**Pedestrian record：**
- Simulation second
- Number
- Pedestrian Type
- Longtitute
- Latitude
- Coordinate center (z)

**Vehicle record：**
- Simulation second
- Number
- Vehicle Type
- Longtitute (Front)
- Latitude (Front)
- Coordinate front (z)
![image](https://github.com/MototsuguMiura/VISSIM2CZML/assets/85535019/572acbab-6ff2-4d5e-be0a-3ab05571c0dc)

#### ④シミュレーションを実行し、出力されたfzpファイル及びppファイルをinputフォルダに移す
![image](https://github.com/MototsuguMiura/VISSIM2CZML/assets/85535019/538dcb3b-a4a8-4e73-b758-562315f2fb36)

#### ⑤コマンドラインからPythonスクリプトを実行
![image](https://github.com/MototsuguMiura/VISSIM2CZML/assets/85535019/ff4175a6-c0f2-4be6-8ddd-e6c19110cd58)

#### ⑥Plateau Viewを開き、カタログにczmlファイルを追加
![image](https://github.com/MototsuguMiura/VISSIM2CZML/assets/85535019/1f4432f2-9170-4ef2-b1f5-7e64797485dc)

#### 補足
Pythonスクリプトをエディターで開き、日付の設定やPLATEAU View上で表示される色とサイズを車両タイプ/歩行者タイプ番号に連動して変更することができる
![image](https://github.com/MototsuguMiura/VISSIM2CZML/assets/85535019/acfee348-656e-4f0b-993b-310412c60171)
![image](https://github.com/MototsuguMiura/VISSIM2CZML/assets/85535019/fda62f9f-eeea-49a8-9184-8bca38d88cc7)

<br />

### PLATEAU Viewにインポートされた車両・歩行者アニメーション（例：西新宿）
![image](https://github.com/MototsuguMiura/VISSIM2CZML/assets/85535019/5b39716d-4d9d-45d4-9192-17eddde662de)

## 動作環境  
- PTV Vissim 2024  
- Python 3.9 + pandas<br />
※今後の開発によっては仕様が変わり本ツールが利用できなくなる可能性があります。予めご了承ください。  


## ライセンス  
本ツールは、[MIT License](https://opensource.org/license/mit/)に従います。<br />
PTV Vissimは、有償のソフトウェアです。[こちら](https://www.ptvgroup.com/ja/contact)からお問合せください。
