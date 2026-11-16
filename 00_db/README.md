# 00_db 已迁移至服务器

**迁移日期** 2026-11-16　|　**本地已清空**，全部文件存于服务器
**服务器** `192.168.71.177`（用户 `wuyanching`），路径 `/mnt/work/chicken/db/rvdb_src/`
**校验** 6 个文件逐一 MD5 比对通过，与本地原件字节一致

## 清单

| 文件 | 大小 | MD5 |
|---|---|---|
| `RVDBv32.dmnd` | 357 MB | `f4b5291a5376c9b460acf889a9a61e87` |
| `RVDBv32_rev.dmnd` | 357 MB | `1a2e20592151a290a4923f8d4b9ff13a` |
| `RVDBv32_rev.fasta` | 346 MB | `721e12fc93bcb02019b3fd0b3f234a69` |
| `RVDBv32_unique.fasta` | 345 MB | `75bebc137ad9658d350312d656c1edbb` |
| `U-RVDBv29.0-prot.fasta.xz` | 398 MB | `bcd732817ffa7b188858762068e9c6d0` |
| `U-RVDBv32.0-prot_unique.fasta.xz` | 70 MB | `5bb367c39dc71776cc5a91637f9d7a68` |

服务器路径说明：
- `RVDBv32.dmnd` 另有一份在 `/mnt/work/chicken/db/RVDBv32.dmnd`（项目流程原先使用的就是这一份）
- 其余 5 个在 `/mnt/work/chicken/db/rvdb_src/`

## 重新获取方式

| 文件 | 来源 |
|---|---|
| `U-RVDBv29.0-prot.fasta.xz` | RVDB 官网 `https://rvdb-prot.pasteur.fr/files/U-RVDBv29.0-prot.fasta.xz` |
| `U-RVDBv32.0-prot_unique.fasta.xz` | 同上，版本号替换为 v32.0 |
| `RVDBv32_unique.fasta` | 由上面的 xz 解压得到 |
| `RVDBv32_rev.fasta` | 由 `RVDBv32_unique.fasta` 反向生成（`seqkit seq -r -p`） |
| `*.dmnd` | 由对应 fasta 用 `diamond makedb` 重建 |

## 一个必须记住的判断

这批库**以真核病毒 / RNA 病毒为主**（SARS-CoV-2、海洋 RNA 病毒、昆虫病毒），噬菌体只占很小一部分。

因此用它测肠道噬菌体占比会系统性低估约 **4.7 倍**（实测：旧库 0.839% vs PHROG 3.929%，同一批 reads）。

**问题不是库小，而是库的宿主范围不对。** 详见 `13_calibration/参考库核查_2026-11-15.md`。
