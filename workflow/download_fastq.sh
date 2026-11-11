#!/usr/bin/env bash
# ============================================================
# 扬子鳄病毒组预分析 - fastq 下载脚本
# 项目: PRJNA539906 (6 个扬子鳄粪便 shotgun, 冬 vs 夏)
# 在 Linux 服务器 或 WSL 运行（Windows 本地 ftp.sra.ebi.ac.uk 被限速 ~10KB/s）
# ============================================================
set -euo pipefail

cd "$(dirname "$0")/.."   # 回到项目根目录
mkdir -p 00_raw
cd 00_raw

# ---------- 6 个 run 的 ENA fastq 路径 ----------
# 冬季 (winter): SRR14300938, SRR14300939, SRR14300942
# 夏季 (summer): SRR14300940, SRR14300941, SRR14300943
RUNS="SRR14300938 SRR14300939 SRR14300942 SRR14300940 SRR14300941 SRR14300943"

# ============ 方式一：Aspera（推荐，速度最快）============
download_aspera() {
  ASCP="${ASCP:-ascp}"
  KEY="asperaweb_id_dsa.openssh"

  # 下载 ENA 官方公开密钥（Aspera 4.2+ 安装包不再内置）
  if [ ! -f "$KEY" ]; then
    echo "==> 下载 ENA 公开密钥 ..."
    wget -q "https://downloads.ebi.ac.uk/vol1/security/asperaweb_id_dsa.openssh" -O "$KEY" \
      || curl -sSL -o "$KEY" "https://downloads.ebi.ac.uk/vol1/security/asperaweb_id_dsa.openssh"
    chmod 600 "$KEY"
  fi

  echo "==> 使用 Aspera 下载 6 个 fastq ..."
  for r in $RUNS; do
    p1=${r:0:6}   # 前 6 位: SRR143
    p2=${r: -3}   # 后 3 位: 038
    for mate in 1 2; do
      remote="era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/$p1/$p2/$r/${r}_${mate}.fastq.gz"
      echo "  -> ${r}_${mate}.fastq.gz"
      "$ASCP" -QT -l 300m -P 33001 -i "$KEY" "$remote" .
    done
  done
}

# ============ 方式二：HTTPS + aria2 兜底（慢，仅作备用）============
download_https() {
  ARIA2="${ARIA2:-aria2c}"
  echo "==> 使用 aria2 (HTTPS) 下载 6 个 fastq ..."
  for r in $RUNS; do
    p1=${r:0:6}
    p2=${r: -3}
    for mate in 1 2; do
      url="https://ftp.sra.ebi.ac.uk/vol1/fastq/$p1/$p2/$r/${r}_${mate}.fastq.gz"
      echo "  -> ${r}_${mate}.fastq.gz"
      "$ARIA2" -x 4 -s 4 -k 1M --continue=true "$url" -d .
    done
  done
}

# ---------- 宿主基因组（备用；本地已下载 GCA_000455745.1.fa）----------
download_genome() {
  echo "==> 下载宿主基因组 (GCA_000455745.1) ..."
  curl -L -o GCA_000455745.1.fa "https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_000455745.1"
}

# ============ 主入口 ============
case "${1:-aspera}" in
  aspera) download_aspera ;;
  https)  download_https ;;
  genome) download_genome ;;
  all)    download_aspera; download_genome ;;
  *)      echo "用法: $0 [aspera|https|genome|all]"; exit 1 ;;
esac

echo "==> 完成。检查文件完整性："
for f in *.fastq.gz; do
  gzip -t "$f" && echo "  OK  $f" || echo "  损坏 $f"
done
