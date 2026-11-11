#!/usr/bin/env bash
# ============================================================
# 统一环境配置 —— 所有 workflow 脚本在开头 source 本文件
#   用法：  source workflow/env.sh
# 项目：扬子鳄粪便病毒组预分析（PRJNA539906）
# 更新：2026-11-07
# ============================================================

# 项目根目录（本文件在 workflow/ 下）
PROJ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PROJ
cd "$PROJ" || return 1 2>/dev/null || exit 1

# ---- 关键：perl / bowtie2 需要 C locale，否则大量警告 ----
export LC_ALL=C
export LANG=C

TOOLS="$PROJ/workflow/tools"
export TOOLS

# ---- 工具路径 ----
export PERL="$TOOLS/perl/perl/bin/perl.exe"
export FASTP="$TOOLS/fastp/bin/fastp.exe"
export BOWTIE2="$TOOLS/bowtie2/bowtie2"                    # perl 包装脚本（需 $PERL 调用）
export BOWTIE2_ALIGN="$TOOLS/bowtie2/bowtie2-align-s.exe"  # 底层二进制（备用）
export BOWTIE2_BUILD="$TOOLS/bowtie2/bowtie2-build-s.exe"  # 底层二进制（备用）
export BOWTIE2_INSPECT="$TOOLS/bowtie2/bowtie2-inspect-s.exe"
export DIAMOND="$TOOLS/diamond/diamond.exe"
export PICARD_JAR="$TOOLS/picard/picard.jar"
export MULTIQC="$TOOLS/multiqc-venv/Scripts/multiqc.exe"

# 宿主索引前缀（small index；3.11 Gb 基因组用 -s 版二进制）
export HOST_IDX="$PROJ/00_raw/alligator_host"

# ---- 包装函数（让命令写法与 Linux 一致）----

# bowtie2 比对（双端 + 去宿主）
#   注意：-S 必须是真实文件，不可用 /dev/null；
#   配合 --no-unal 时 SAM 只含比对上的少量 reads，体积很小，用完即删。
bt2() {
  "$PERL" "$BOWTIE2" "$@"
}

# 建索引
bt2_build() {
  "$BOWTIE2_BUILD" "$@"
}

# 查看索引
bt2_inspect() {
  "$BOWTIE2_INSPECT" "$@"
}

# Picard（BAM 处理，替代 samtools：SortSam / BuildBamIndex / MarkDuplicates ...）
picard() {
  java -jar "$PICARD_JAR" "$@"
}

# 健康检查：确认各工具可执行
toolchain_check() {
  local ok=0
  printf '%-14s ' "perl";      "$PERL" -e 'printf "v%vd ok\n", $^V'      2>/dev/null || { echo "FAIL"; ok=1; }
  printf '%-14s ' "fastp";     "$FASTP" --version                        2>/dev/null || { echo "FAIL"; ok=1; }
  printf '%-14s ' "bowtie2";   bt2 --version 2>&1 | grep -oE 'version [0-9.]+' | head -1       || { echo "FAIL"; ok=1; }
  printf '%-14s ' "diamond";   "$DIAMOND" version                        2>/dev/null | head -1 || { echo "FAIL"; ok=1; }
  printf '%-14s ' "picard";    picard SortSam --version 2>&1 | grep -oE 'Version:[0-9.]+' | head -1 || { echo "FAIL"; ok=1; }
  printf '%-14s ' "multiqc";   "$MULTIQC" --version                      2>/dev/null | head -1 || { echo "FAIL"; ok=1; }
  return $ok
}

# 直接运行时打印工具链状态
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
  echo "项目根目录: $PROJ"
  echo "工具目录:   $TOOLS"
  echo ""
  echo "== 工具链状态 =="
  toolchain_check
fi
