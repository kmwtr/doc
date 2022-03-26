# RK3308 の Boot Process とベアメタルLチカ

## Boot Process 概要

### 0. ブータブルメディアの構成（U-Bootの場合）

| Sector hex | dd seek decimal | Offset (Byte)     | Name            | .img file Name | 
| ---------- | --------------- | ----------------- | --------------- | -------------- |
| -          | -               | -                 | ROM (BootRom)   |                |
| 0x40       | 64              | 0x8000 (32KB)     | U-Boot SPL      | idbloader.img  |
| 0x4000     | 16384           | 0x800000 (8MB)    | U-Boot          | uboot.img      |
| 0x6000     | 24576           | 0xC00000 (12MB)   | ATF/TEE         | trust.img      |
| 0x8000     | 32768           | 0x1000000 (16MB)  | boot (Kernel)   |                |
| 0x40000    | 262144          | 0x8000000 (128MB) | rootfs (Rootfs) |                |

`rk3308_loader_xxx_xxx_xxx.bin` はUSB経由でemmcをフラッシュする場合のもの

引用元
[Boot option](http://opensource.rock-chips.com/wiki_Boot_option)

```bash:書き込み例
dd if=idbloader.img   of=/dev/sdx seek=64
dd if=uboot.img       of=/dev/sdx seek=16384 
dd if=trust.img       of=/dev/sdx seek=24576 
dd if=boot.img        of=/dev/sdx seek=32768 
dd if=rootfs.img      of=/dev/sdx seek=262144
```

### 1. Header | Offset 0x8000

SoCのBootROMはSDカードの`0x8000`位置から内容を読み込みを始めるが、その先頭１セクター（512Byte）にはRockchip固有のシグネチャやSRAMにロードすべきSPLの位置等の情報を格納した「header0」が期待されている。

```C:ヘッダの構成（U-Bootから引用
struct header0_info {
	uint32_t signature;    // Signature (must be RKSD_SIGNATURE)
	uint8_t reserved[4];
	uint32_t disable_rc4;    // 0 to use rc4 for boot image,  1 to plain binary
	uint16_t init_offset;    // Offset in blocks of the SPL code from this header block. E.g. 4 means 2KB after the start of this header.
	uint8_t reserved1[492];
	uint16_t init_size;      // RK_BLK_SIZE==512 で spl_params.init_size を割ったもののようだ。
	uint16_t init_boot_size;
	uint8_t reserved2[2];
};

// Other fields are not used by U-Boot ... じゃあ 0x0 で埋めてもいいのかな。
```

header0 のルール
* 先頭 4 Byte にはロックチップのシグネチャ`0x0ff0aa55`がないといけない。
* RC4 で暗号化しないといけない。　
  * キー： `7c4e0304550509072d2c7b38170d1711`
  * `disable_rc4`はSPLについて。ヘッダ自体は暗号化の必要があるようだ。

RC4で暗号化された`header0_info`は、Armbian等の様々なイメージで共通だった。以下にダンプしたものを例示する。

```hexdump:暗号化されたヘッダ
3B 8C DC FC BE 9F 9D 51 EB 30 34 CE 24 51 1F 98 FF 0C F2 36 05 50 C8 BB 3F EC DD BD 06 85 FA B7 B3 AB 6A EA C8 68 E0 08 AD 9D 6F 9C 3C 98 B0 8C 45 13 54 1C 1D 1B 1F 15 A7 F1 F0 0B E3 4E 0C C7 60 96 01 6A B5 F0 E2 C1 50 C6 24 9E 12 F7 58 8E 40 B9 B7 BE 8B FA 25 DD 74 D7 6F 59 46 7E 13 41 EE FD F5 91 39 BC 74 95 25 3C 1A E1 F1 57 30 05 CA F8 72 9A 1B E6 9D 26 35 5D 81 2B 2B 93 BD 01 3A 54 0C A1 4B 11 06 98 A1 91 19 4A 4E 92 30 1A F2 B2 D5 AE 59 6C 9E 96 FD F4 FF A4 88 E3 9F 87 49 6C 3A 76 6D 3D 1A AC 1E 77 0A 5E FF 92 52 61 19 FF 74 96 EE 13 93 7A E0 B9 F0 1B 51 38 B3 8D 2F 59 87 02 65 C1 88 6B 4C 21 AA 7B 16 D5 50 CE 37 80 A4 1F 46 DF BD B0 D9 65 8F E1 15 CE 08 0F 7C EE 5A 0C 61 50 3C 90 BF 79 1A BF 05 96 B0 61 EB ED 62 53 4B 3A EE A4 AA 77 95 DF E9 E7 44 FB 2D F8 BA 7E B2 1E E0 04 EA EA D2 D7 61 F9 90 92 88 E3 07 B6 5A 8F 9B 4E 4F 9E F9 C8 38 D9 11 5D 41 37 F4 DD 5B 78 47 95 8A AC F5 42 5D AA 0C 52 49 C8 0D 9D A7 32 2E D7 03 B1 41 95 49 50 2D 89 27 5B 0D 0E 72 6F FA 0E 0B 70 BC 15 42 A2 26 CB D5 26 65 0C CB B1 EC 54 45 45 E5 39 D5 7B 77 FF 9B C0 C8 38 4E E5 6E 4A BB 42 9F 43 D1 D0 5E 04 78 0F 00 3E 06 BC 07 3C C9 4D 2A 64 B9 43 77 CF 93 D7 F8 68 00 38 B9 7B E8 AA F3 8A 47 96 27 8B 44 45 C4 C4 ED E0 A1 26 02 6F DD 37 87 92 C6 01 03 14 A0 E6 AA 2B 6C DA E5 98 75 35 3A 2C BF CC B5 27 62 5F D0 DC 2A 9B D7 A2 4D D7 72 65 7A D1 17 3A 98 E7 3C 57 8E B6 A0 32 34 C9 6E D1 CA CD 81 95 BD 6E 0E 84 5C A6 CB 0C 42 5F C8 16 E0 3E AC F3 32 8E 44 56 02 25 DF CD AF 1E 1D 36 59 B6 44 58 D1 D5 EA 04 C3 6B 91 8D 6B 93 18 2C 27 45
```

```hexdump:復号したヘッダ
55 AA F0 0F 
00 00 00 00 
01 00 00 00 
04 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
04 00 
04 04 
00 00
```

#### 要確認

> Other fields are not used by U-Boot

とU-Bootに書いてあった部分は、消すと動かなくなった。U-Bootが使わないだけでBootROMには必要という事か。

* uint16_t init_size == 0x0004 == 4
* uint16_t init_boot_size == 0x0404 == 1028

#### メモ：復号に使ったツール

![clipboard.png](inkdrop://file:3DWmKkwa6)

### 2. SPL | Offset 0x8000 + 0x800 (init_offset = 0x00000004)

このSPLの位置はヘッダの`init_offset`の値によって決定されている。まずは実物を観察した。

#### 実例

```hexdump:SPL の場合
52 4B 33 33 
00 00 00 00 52 53 41 4B F8 01 00 00
```

```hexdump:Armbian の場合
52 4B 33 33
D1 00 00 14 17 01 00 14 FF FF FF 17
```

#### 2.1 | + 0x800 位置 (SPL Header)

`0x8800 (0x8000 + 0x800)` 位置にSPLヘッダー `spl_hdr` を4バイト配置。

RK3308 の場合 `RK33` というシグネチャが期待されている。

#### 2.2 | + 0x8804 位置

BootROM が命令を実行し始める位置。


#### SPLのサイズについて

> The maximum size of u-boot-spl-dtb.bin which the boot ROM will read is 32KB, or 0x40 blocks. This is a severe and annoying limitation. There may be a way around this limitation, since there is plenty of SRAM, but at present the board refuses to boot if this limit is exceeded.

BOOT0 は 32KiB (0x40 セクター分)までしかロードしないとある。一方で、このような記述もあった。

```C:rkcommon.c（一部抜粋）
struct spl_info {
	const char *imagename;
	const char *spl_hdr;
	const uint32_t spl_size;
	const bool spl_rc4;
};
static struct spl_info spl_infos[] = {
	{ "rk3288", "RK32", 0x8000, false },
	{ "rk3308", "RK33", 0x40000 - 0x1000, false},
	{ "rk3399", "RK33", 0x30000 - 0x2000, false },
};
```

RK3288 などは `0x8000 == 32KiB` だが、RK3308 は `0x3F000 == 258,048 == 252KiB` となっている。`0x40000 == 256KiB` なので、 System SRAM 256KiB @fff80000 の範囲を指しているように見える

**疑問**
* 4KiB 引いてるのは何だろう？
* SPL といった時ヘッダやオフセットは含まれるのだろうか？
  * 多分 SPL header からを指している。SRAM上にはメディアの`0x8800`からが展開されていた。


## ベアメタルLチカ

C-Boot and LEDBlink ...

### 1. SD の `0x8000` 位置に header0 を配置。

```C:header0 イメージ
struct header0 {
	uint32_t signature   = 0x0ff0aa55; // RK_SIGNATURE
	uint32_t reserved    = 0x00000000; // -
	uint32_t disable_rc4 = 0x00000001; // plain binary
	uint16_t init_offset = 0x00000002; // Base + 0x400 のオフセット。
	uint8_t reserved1[492]; // -
	uint16_t init_size       = 0x0004; // 4 (4 * 512 == 2048) を指しているようだが よくわからんので同じにした
	uint16_t init_boot_size  = 0x0404; // 1028 (1024 + 4 ?)何を指しているのかよくわからんので同じにした
	uint16_t reserved2       = 0x0000; // -
};
```

オレオレ流としてオフセットをコンパクトにした。これを RC4 で暗号化する。


### 2. SD の `0x8400 (0x8000 + 0x400)` 位置にRK33シグネチャ。

SPL header は "RK33".

```hexdump:SPL header
52 4B 33 33
```

### 3. SD の `0x8404 (0x8000 + 0x400 + 0x4)` 位置から命令。

命令はメディアの `0x8404` から実行されるが、中途半端なので `0x8410` (SRAM上の `0xfff80010` ) にジャンプする命令をこの場所に置いて、これを汎用ブートイメージとした。

（普通にコードをコンパイルするとどうしても0x10からのLチカbinができてしまって、良い解決方法が見つからなかった。とりあえず手作業で0x04位置にジャンプ命令 `0x14000003` を入れた。一度作っておけば再利用できるのでヨシとした。）

```hexdump:header0_to_SPL.bin （0x8000 以降を抜粋）
3B 8C DC FC BE 9F 9D 51 EB 30 34 CE 22 51 1F 98 FF 0C F2 36 05 50 C8 BB 3F EC DD BD 06 85 FA B7 B3 AB 6A EA C8 68 E0 08 AD 9D 6F 9C 3C 98 B0 8C 45 13 54 1C 1D 1B 1F 15 A7 F1 F0 0B E3 4E 0C C7 60 96 01 6A B5 F0 E2 C1 50 C6 24 9E 12 F7 58 8E 40 B9 B7 BE 8B FA 25 DD 74 D7 6F 59 46 7E 13 41 EE FD F5 91 39 BC 74 95 25 3C 1A E1 F1 57 30 05 CA F8 72 9A 1B E6 9D 26 35 5D 81 2B 2B 93 BD 01 3A 54 0C A1 4B 11 06 98 A1 91 19 4A 4E 92 30 1A F2 B2 D5 AE 59 6C 9E 96 FD F4 FF A4 88 E3 9F 87 49 6C 3A 76 6D 3D 1A AC 1E 77 0A 5E FF 92 52 61 19 FF 74 96 EE 13 93 7A E0 B9 F0 1B 51 38 B3 8D 2F 59 87 02 65 C1 88 6B 4C 21 AA 7B 16 D5 50 CE 37 80 A4 1F 46 DF BD B0 D9 65 8F E1 15 CE 08 0F 7C EE 5A 0C 61 50 3C 90 BF 79 1A BF 05 96 B0 61 EB ED 62 53 4B 3A EE A4 AA 77 95 DF E9 E7 44 FB 2D F8 BA 7E B2 1E E0 04 EA EA D2 D7 61 F9 90 92 88 E3 07 B6 5A 8F 9B 4E 4F 9E F9 C8 38 D9 11 5D 41 37 F4 DD 5B 78 47 95 8A AC F5 42 5D AA 0C 52 49 C8 0D 9D A7 32 2E D7 03 B1 41 95 49 50 2D 89 27 5B 0D 0E 72 6F FA 0E 0B 70 BC 15 42 A2 26 CB D5 26 65 0C CB B1 EC 54 45 45 E5 39 D5 7B 77 FF 9B C0 C8 38 4E E5 6E 4A BB 42 9F 43 D1 D0 5E 04 78 0F 00 3E 06 BC 07 3C C9 4D 2A 64 B9 43 77 CF 93 D7 F8 68 00 38 B9 7B E8 AA F3 8A 47 96 27 8B 44 45 C4 C4 ED E0 A1 26 02 6F DD 37 87 92 C6 01 03 14 A0 E6 AA 2B 6C DA E5 98 75 35 3A 2C BF CC B5 27 62 5F D0 DC 2A 9B D7 A2 4D D7 72 65 7A D1 17 3A 98 E7 3C 57 8E B6 A0 32 34 C9 6E D1 CA CD 81 95 BD 6E 0E 84 5C A6 CB 0C 42 5F C8 16 E0 3E AC F3 32 8E 44 56 02 25 DF CD AF 1E 1D 36 59 B6 44 58 D1 D5 EA 04 C3 6B 91 8D 6B 93 18 2C 27 45 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 52 4B 33 33 03 00 00 14 00 00 00 00 00 00 00 00
```

任意の命令のバイナリ（エントリ == SRAM 0xfff80010）をこの後ろに結合してやれば動く。


### 4. LED Blink

SRAM は位置 `0xfff80000` にある。SRAM の `0xfff80010`から始まるようにCをコンパイルして、SD の位置 `0x8410` に配置すればよい。

`aarch64-none-elf-gcc` でビルド。（Allwinnerとは違って）このSoCはBootROMの段階からAArch64状態になっているようだ。いいね！

```hexdump:Lチカコードを抜粋。
85 00 80 D2 45 E4 BF F2 44 E4 BF D2 40 00 80 52 FF 43 00 D1 E2 03 04 AA E3 03 00 2A A0 00 00 B9 E1 8F 90 52 C1 03 A0 72 80 00 00 B9 1F 20 03 D5 FF 0F 00 B9 E0 0F 40 B9 1F 00 01 6B E8 00 00 54 E0 0F 40 B9 00 04 00 11 E0 0F 00 B9 E0 0F 40 B9 1F 00 01 6B 69 FF FF 54 43 00 00 B9 FF 0F 00 B9 E0 0F 40 B9 1F 00 01 6B E8 00 00 54 E0 0F 40 B9 00 04 00 11 E0 0F 00 B9 E0 0F 40 B9 1F 00 01 6B 69 FF FF 54 5F 00 00 B9 EA FF FF 17 00 00 00 00
```

catでバイナリを結合する処理をMakefileに入れた。


![200912_RK.gif](inkdrop://file:YssuU7C02)
おめでとう！
