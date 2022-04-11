---
title: "Windows上でArm Cortex-Aベアメタル開発環境構築"
emoji: "😸"
type:  "tech" # tech: 技術記事 / idea: アイデア記事
topics: ["ARM","Cortex-A", "Baremetal", "C/C++"]
published: true # 公開設定（falseにすると下書き）
---


## 0. ダウンロードリンク

必要なもの

* [Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm)
  * [Setup program](http://gnuwin32.sourceforge.net/downlinks/make.php) から、インストーラーを普通にダウンロードできる。
* [GNU Toolchain for the A-profile Architecture](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-a/downloads)
* [Git for Windows](https://gitforwindows.org/)


## 1. Make のインストール

パスを通す。システム環境変数の編集 > 環境変数

```:Path(e.g.
C:\Program Files (x86)\GnuWin32\bin
```

コマンドプロンプトで動作確認。

```Bash
> make --version
GNU Make 3.81
Copyright (C) 2006  Free Software Foundation, Inc.
これはフリーソフトウェアです. 利用許諾についてはソースを
ご覧ください.
商業性や特定の目的への適合性の如何に関わらず, 無保証です.

This program built for i386-pc-mingw32
```


## 2. GCC のインストール

ツールチェーンをダウンロードして任意のディレクトリにインストール。

今回入れたもの

* gcc-arm-10.3-2021.07-mingw-w64-i686-arm-none-eabi.tar.xz
* gcc-arm-10.3-2021.07-mingw-w64-i686-aarch64-none-elf.tar.xz

自分はリネームしてパスを通した。

```:Path(e.g.
D:\gcc_for_arm\gcc-arm-10.3-arm-none-eabi\bin
D:\gcc_for_arm\gcc-arm-10.3-aarch64-none-elf\bin
```

コマンドプロンプトで動作確認。

```Bash
> arm-none-eabi-gcc --version
arm-none-eabi-gcc (GNU Toolchain for the A-profile Architecture 10.3-2021.07 (arm-10.29)) 10.3.1 20210621
Copyright (C) 2020 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

```Bash
> aarch64-none-elf-gcc --version
aarch64-none-elf-gcc (GNU Toolchain for the A-profile Architecture 10.3-2021.07 (arm-10.29)) 10.3.1 20210621
Copyright (C) 2020 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```


## 3. 動作確認

適当なCファイルと Makefile を作ってコマンドプロンプトでコンパイルする。

```Bash
> make
aarch64-none-elf-gcc -mcpu=cortex-a35  -I include -Wall -O2 -nostartfiles -ffreestanding  -c source/main.c -o main.o
aarch64-none-elf-as -mcpu=cortex-a35  -c source/start.s -o start.o
aarch64-none-elf-ld -nostdlib -T link.lds main.o start.o -o main.elf
aarch64-none-elf-objcopy -O binary main.elf main.bin
```

おめでとう（ ' v ' ）


## 4. より扱いやすくするために

Windows環境でもBashコマンドを使いたい。Git for Windows の Git Bash がとても便利。

### Tips

ショートカット（タスクバーなどの）のプロパティで、実行時の初期ディレクトリを設定することができる。

![clipboard.png](/images/windows_zyoude_arm_cortex_a_baremetal_kankyou/OpdutuABO-clipboard.png)

