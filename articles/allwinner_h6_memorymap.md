---
title: "Allwinner H6 Memorymap"
emoji: "😸"
type:  "tech" # tech: 技術記事 / idea: アイデア記事
topics: ["ARM","Allwinner", "Baremetal", "H6", "Cortex-A"]
published: true # 公開設定（falseにすると下書き）
---

## Register BaseAddress

| Module            | Address Start | Address End | Size(Bytes) |
| ----------------- | ------------- | ----------- | ----------- |
| N-BROM            | 0x0000 0000   | 0x0000 9FFF | 40K         |
| S-BROM            | 0x0000 0000   | 0x0000 FFFF | 64K         |
| SRAM A1           | 0x0002 0000   | 0x0002 7FFF | 32K         |
| SRAM C            | 0x0002 8000   | 0x0004 5FFF | 120K        |
| SRAM A2           | 0x0010 0000   | 0x0010 3FFF | 16K         |
| "                 | 0x0010 4000   | 0x0011 7FFF | 80K         |
| DE                | 0x0100 0000   | 0x013F FFFF | 4M          |
| DI0               | 0x0142 0000   | 0x0143 FFFF | 128K        |
| GPU               | 0x0180 0000   | 0x0183 FFFF | 256K        |
| CE_NS             | 0x0190 4000   | 0x0190 47FF | 2K          |
| CE_S              | 0x0190 4800   | 0x0190 4FFF | 2K          |
| EMCE              | 0x0190 5000   | 0x0190 5FFF | 4K          |
| CE_KEY_SRAM       | 0x0190 8000   | 0x0190 8FFF | 4K          |
| VE SRAM           | 0x01A0 0000   | 0x01BF FFFF | 2M          |
| VP9               | 0x01C0 0000   | 0x01C0 0FFF | 4K          |
| VE                | 0x01C0 E000   | 0x01C0 FFFF | 8K          |
| SYS_CFG           | 0x0300 0000   | 0x0300 0FFF | 4K          |
| CCU               | 0x0300 1000   | 0x0300 1FFF | 4K          |
| DMAC              | 0x0300 2000   | 0x0300 2FFF | 4K          |
| MSGBOX            | 0x0300 3000   | 0x0300 3FFF | 4K          |
| SPINLOCK          | 0x0300 4000   | 0x0300 4FFF | 4K          |
| HSTIMER           | 0x0300 5000   | 0x0300 5FFF | 4K          |
| SID               | 0x0300 6000   | 0x0300 6FFF | 4K          |
| TIMER             | 0x0300 9000   | 0x0300 93FF | 1K          |
| PWM               | 0x0300 A000   | 0x0300 A3FF | 1K          |
| GPIO              | 0x0300 B000   | 0x0300 B3FF | 1K          |
| PSI               | 0x0300 C000   | 0x0300 C3FF | 1K          |
| DCU               | 0x0301 0000   | 0x0301 FFFF | 64K         |
| GIC               | 0x0302 0000   | 0x0302 FFFF | 64K         | 
| IOMMU             | 0x030F 0000   | 0x030F FFFF | 64K         |
| DRAM_CTRL         | 0x0400 2000   | 0x0400 5FFF | 16K         |
| NAND0             | 0x0401 1000   | 0x0401 1FFF | 4K          |
| SMHC0             | 0x0402 0000   | 0x0402 0FFF | 4K          |
| SMHC1             | 0x0402 1000   | 0x0402 1FFF | 4K          |
| SMHC2             | 0x0402 2000   | 0x0402 2FFF | 4K          |
| UART0             | 0x0500 0000   | 0x0500 03FF | 1K          |
| UART1             | 0x0500 0400   | 0x0500 07FF | 1K          |
| UART2             | 0x0500 0800   | 0x0500 0BFF | 1K          |
| UART3             | 0x0500 0C00   | 0x0500 0FFF | 1K          |
| TWI0              | 0x0500 2000   | 0x0500 23FF | 1K          |
| TWI1              | 0x0500 2400   | 0x0500 27FF | 1K          |
| TWI2              | 0x0500 2800   | 0x0500 2BFF | 1K          |
| TWI3              | 0x0500 2C00   | 0x0500 2FFF | 1K          |
| SCR0              | 0x0500 5000   | 0x0500 53FF | 1K          |
| SCR1              | 0x0500 5400   | 0x0500 57FF | 1K          |
| SPI0              | 0x0501 0000   | 0x0501 0FFF | 4K          |
| SPI1              | 0x0501 1000   | 0x0501 1FFF | 4K          |
| EMAC              | 0x0502 0000   | 0x0502 FFFF | 64K         |
| TS0               | 0x0506 0000   | 0x0506 0FFF | 4K          |
| THS               | 0x0507 0400   | 0x0507 07FF | 1K          |
| CIR_TX            | 0x0507 1000   | 0x0507 13FF | 1K          |
| I2S/PCM3          | 0x0508 F000   | 0x0508 FFFF | 4K          |
| I2S/PCM0          | 0x0509 0000   | 0x0509 0FFF | 4K          |
| I2S/PCM1          | 0x0509 1000   | 0x0509 1FFF | 4K          |
| I2S/PCM2          | 0x0509 2000   | 0x0509 2FFF | 4K          |
| OWA               | 0x0509 3000   | 0x0509 33FF | 1K          |
| DMIC              | 0x0509 5000   | 0x0509 53FF | 1K          |
| Audio HUB         | 0x0509 7000   | 0x0509 7FFF | 4K          |
| USB0(USB2.0_OTG)  | 0x0510 0000   | 0x051F FFFF | 1M          |
| USB1(USB3.0_HOST) | 0x0520 0000   | 0x052F FFFF | 1M          |
| USB3(USB2.0_HOST) | 0x0531 1000   | 0x0531 1FFF | 4K          |
| PCIe              | 0x0540 0000   | 0x054F FFFF | 1M          |
| HDMI_TX0(1.4/2.0) | 0x0600 0000   | 0x060F FFFF | 1M          |
| DISP_IF_TOP       | 0x0651 0000   | 0x0651 0FFF | 4K          |
| TCON_LCD          | 0x0651 1000   | 0x0651 1FFF | 4K          |
| TCON_TV           | 0x0651 5000   | 0x0651 5FFF | 4K          |
| CSI_SRAM          | 0x0660 0000   | 0x0661 FFFF | 128K        |
| CSI               | 0x0662 0000   | 0x0663 FFFF | 128K        |
| RTC               | 0x0700 0000   | 0x0700 03FF | 1K          |
| R_CPUS_CFG        | 0x0700 0400   | 0x0700 0BFF | 2K          |
| R_PRCM            | 0x0701 0000   | 0x0701 03FF | 1K          |
| R_TIMER           | 0x0702 0000   | 0x0702 03FF | 1K          |
| R_WDOG            | 0x0702 0400   | 0x0702 07FF | 1K          |
| R_TWDOG           | 0x0702 0800   | 0x0702 0BFF | 1K          |
| R_PWM             | 0x0702 0C00   | 0x0702 0FFF | 1K          |
| R_INTC            | 0x0702 1000   | 0x0702 13FF | 1K          |
| R_GPIO            | 0x0702 2000   | 0x0702 23FF | 1K          |
| R_CIR_RX          | 0x0704 0000   | 0x0704 03FF | 1K          |
| R_OWC             | 0x0704 0400   | 0x0704 07FF | 1K          |
| R_UART            | 0x0708 0000   | 0x0708 03FF | 1K          |
| R_TWI             | 0x0708 1400   | 0x0708 17FF | 1K          |
| CPU_SYS_CFG       | 0x0810 0000   | 0x0810 03FF | 1K          |
| CNT_R             | 0x0811 0000   | 0x0811 0FFF | 4K          |
| CNT_C             | 0x0812 0000   | 0x0812 0FFF | 4K          |
| C0_CPUX_CFG       | 0x0901 0000   | 0x0901 0FFF | 4K          |
| C0_CPUX_MBIST     | 0x0902 0000   | 0x0902 0FFF | 4K          |
| DRAM SPACE        | 0x4000 0000   | 0xFFFF FFFF | 3G          |

64bit CPUであるにも関わらずDRAM SPACEが3GBしか無い。

## CPU Subsystem Control Register List

| Module Name     | Base Address |
| --------------- | ------------ |
| CPU_SUBSYS_CTRL | 0x08100000   |


| Register Name     | Offset | Description                                |
| ----------------- | ------ | ------------------------------------------ |
| GENER_CTRL_REG0   | 0x0000 | General Control Register0                  |
| GENER_CTRL_REG1   | 0x0004 | General Control Register1                  |
| GIC_JTAG_RST_CTRL | 0x000C | GIC and Jtag Reset Control Register        |
| C0_INT_EN         | 0x0010 | Cluster0 Interrupt Enable Control Register |
| IRQ_FIQ_STATUS    | 0x0014 | GIC IRQ/FIQ Status Register                |
| GENER_CTRL_REG2   | 0x0018 | General Control Register2                  |


GIC IRQ/FIQ Status Register(Default Value: 0x0000_0000)

| Bit   | Description   |
| ----- | ------------- |
| 31:16 | FIQ_OUT[15:0] |
| 15:0  | IRQ_OUT[15:0] |

## Ref

* [u-boot-sunxi/arch/arm/include/asm/arch-sunxi/cpu_sun50i_h6.h](https://github.com/linux-sunxi/u-boot-sunxi/blob/0b80e1c63d5ff9585c79afff1092cf761cea46cc/arch/arm/include/asm/arch-sunxi/cpu_sun50i_h6.h)
* [clock_sun50i_h6.h](https://github.com/linux-sunxi/u-boot-sunxi/blob/0b80e1c63d5ff9585c79afff1092cf761cea46cc/arch/arm/include/asm/arch-sunxi/clock_sun50i_h6.h)
