import { computed, ref, watch } from 'vue'

const STORAGE_KEY = 'evo2_locale'
const SUPPORTED_LOCALES = ['zh', 'en']

const locale = ref(readInitialLocale())

const messages = {
  zh: {
    header: {
      subtitle: '基因大模型智能平台',
      switchLanguage: '切换语言'
    },
    sidebar: {
      menu: '功能菜单',
      dataset: '基因数据集',
      generate: 'DNA 生成',
      analysis: '序列分析'
    },
    dna: {
      input: '输入',
      output: '输出',
      modelSelect: '模型选择',
      taskSelect: '任务选择',
      dnaSequence: 'DNA 序列',
      params: '生成参数',
      seqPlaceholder: '请输入 DNA 序列（A / C / G / T），最多 {max} 个碱基',
      clearInputAria: '清空输入序列',
      basePairs: 'bp',
      seqTooLong: '序列长度不能超过 {max}',
      tokens: '生成长度',
      temperature: '温度',
      topK: 'Top-K',
      topP: 'Top-P',
      resetParams: '重置参数',
      generateSeq: '生成序列',
      score: '得分',
      frame: '阅读框',
      copySeq: '复制序列',
      downloadSeq: '下载序列',
      inputSeq: '输入序列',
      generatedSeq: '生成序列',
      totalLength: '总长度',
      chars: '字符',
      emptyAria: '空序列展示',
      modelFast: '快速',
      modelBalanced: '均衡',
      modelAccurate: '高精度',
      modelWheatLabel: 'Evo2-40B-小麦',
      modelWheat: '麦系优化',
      taskCds: 'CDS补全',
      taskPromoter: '启动子延伸',
      taskIntron: '内含子生成'
    },
    dataset: {
      refresh: '刷新数据',
      directoryTitle: '基因数据集目录',
      filesCount: '{count} 个文件',
      lastUpdated: '最后更新',
      selectToView: '选择文件查看内容',
      download: '下载',
      preview: '预览',
      stats: '统计',
      missingFastaHeader: '未找到 FASTA 标题',
      statSeqCount: '序列数量',
      statSeqCountSub: '条目总数',
      statAvgLength: '平均长度',
      statAvgLengthSub: '碱基/氨基酸',
      statFileSize: '文件大小',
      statFileSizeSub: '实际占用',
      emptyText: '请从左侧目录选择一个基因文件',
      emptySubText: '支持查看 FASTA 格式的基因数据文件',
      uploadDemo: '这里是基因数据集上传（Demo）。'
    },
    analysis: {
      title: '序列分析',
      description: '分析原始序列与生成序列之间的相似度与恢复率',
      originalSeq: '原始基因序列',
      generatedSeq: '生成基因序列',
      chars: '{count} 字符',
      originalPlaceholder: '请输入原始 DNA 序列（A/C/G/T）',
      generatedPlaceholder: '请输入生成 DNA 序列（A/C/G/T）',
      clear: '清空',
      generateMetrics: '生成分析指标',
      results: '分析结果',
      likelihood: '似然度打分',
      likelihoodSub: '生成序列概率',
      similarity: '序列相似度',
      similaritySub: '全局比对',
      recovery: '氨基酸恢复率',
      recoverySub: '保守位点',
      summary: '分析摘要',
      summaryText:
        '原始序列与生成序列之间表现出 {similarityLevel} 的相似性，生成序列的似然度评分较高，氨基酸恢复率表明关键位点具有 {recoveryLevel} 的保守性。',
      emptyHint: '输入序列并点击“生成分析指标”查看分析结果',
      alertMissingInput: '请先输入原始序列和生成序列',
      similarityHigh: '高度',
      similarityMedium: '中度',
      similarityLow: '低度',
      similarityVeryLow: '极低',
      recoveryGood: '良好',
      recoveryMedium: '中等',
      recoveryFair: '一般',
      recoveryPoor: '较差'
    }
  },
  en: {
    header: {
      subtitle: 'Gene Foundation Model Platform',
      switchLanguage: 'Switch language'
    },
    sidebar: {
      menu: 'Menu',
      dataset: 'Gene Datasets',
      generate: 'DNA Generation',
      analysis: 'Sequence Analysis'
    },
    dna: {
      input: 'Input',
      output: 'Output',
      modelSelect: 'Model',
      taskSelect: 'Task',
      dnaSequence: 'DNA Sequence',
      params: 'Generation Parameters',
      seqPlaceholder: 'Enter DNA sequence (A / C / G / T), up to {max} bases',
      clearInputAria: 'Clear input sequence',
      basePairs: 'bp',
      seqTooLong: 'Sequence length should not exceed {max}',
      tokens: 'Number of tokens',
      temperature: 'Temperature',
      topK: 'Top-K',
      topP: 'Top-P',
      resetParams: 'Reset',
      generateSeq: 'Generate',
      score: 'Score',
      frame: 'Frame',
      copySeq: 'Copy sequence',
      downloadSeq: 'Download sequence',
      inputSeq: 'Input sequence',
      generatedSeq: 'Generated sequence',
      totalLength: 'Total length',
      chars: 'chars',
      emptyAria: 'empty sequence',
      modelFast: 'Fast',
      modelBalanced: 'Balanced',
      modelAccurate: 'Accurate',
      modelWheatLabel: 'Evo2-40B-Wheat',
      modelWheat: 'Wheat Optimized',
      taskCds: 'CDS Completion',
      taskPromoter: 'Promoter Extension',
      taskIntron: 'Intron Generation'
    },
    dataset: {
      refresh: 'Refresh',
      directoryTitle: 'Gene Dataset Directory',
      filesCount: '{count} files',
      lastUpdated: 'Last updated',
      selectToView: 'Select a file to view',
      download: 'Download',
      preview: 'Preview',
      stats: 'Statistics',
      missingFastaHeader: 'FASTA header not found',
      statSeqCount: 'Sequence Count',
      statSeqCountSub: 'Total records',
      statAvgLength: 'Average Length',
      statAvgLengthSub: 'Base/Amino acid',
      statFileSize: 'File Size',
      statFileSizeSub: 'Storage used',
      emptyText: 'Select a gene file from the left directory',
      emptySubText: 'Supports FASTA gene data files',
      uploadDemo: 'Gene dataset upload area (Demo).'
    },
    analysis: {
      title: 'Sequence Analysis',
      description: 'Analyze similarity and recovery between original and generated sequences',
      originalSeq: 'Original Gene Sequence',
      generatedSeq: 'Generated Gene Sequence',
      chars: '{count} chars',
      originalPlaceholder: 'Enter original DNA sequence (A/C/G/T)',
      generatedPlaceholder: 'Enter generated DNA sequence (A/C/G/T)',
      clear: 'Clear',
      generateMetrics: 'Generate Metrics',
      results: 'Analysis Results',
      likelihood: 'Likelihood Score',
      likelihoodSub: 'Generated sequence probability',
      similarity: 'Sequence Similarity',
      similaritySub: 'Global alignment',
      recovery: 'Amino Acid Recovery',
      recoverySub: 'Conserved sites',
      summary: 'Summary',
      summaryText:
        'The original and generated sequences show {similarityLevel} similarity. The likelihood score is high, and amino acid recovery indicates {recoveryLevel} conservation at key sites.',
      emptyHint: 'Enter sequences and click "Generate Metrics" to view results',
      alertMissingInput: 'Please enter both original and generated sequences first',
      similarityHigh: 'high',
      similarityMedium: 'medium',
      similarityLow: 'low',
      similarityVeryLow: 'very low',
      recoveryGood: 'good',
      recoveryMedium: 'moderate',
      recoveryFair: 'fair',
      recoveryPoor: 'poor'
    }
  }
}

watch(
  locale,
  next => {
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(STORAGE_KEY, next)
    }
    if (typeof document !== 'undefined') {
      document.documentElement.lang = next
    }
  },
  { immediate: true }
)

function readInitialLocale() {
  if (typeof localStorage !== 'undefined') {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored && SUPPORTED_LOCALES.includes(stored)) {
      return stored
    }
  }
  return 'zh'
}

function interpolate(template, params) {
  return template.replace(/\{(\w+)\}/g, (_, key) => {
    if (params && params[key] != null) {
      return String(params[key])
    }
    return ''
  })
}

function resolveMessage(path) {
  const parts = path.split('.')
  let current = messages[locale.value]
  for (const part of parts) {
    current = current?.[part]
    if (current == null) return null
  }
  return typeof current === 'string' ? current : null
}

function t(path, params) {
  const localized = resolveMessage(path)
  if (localized == null) return path
  if (!params) return localized
  return interpolate(localized, params)
}

function setLocale(next) {
  if (SUPPORTED_LOCALES.includes(next)) {
    locale.value = next
  }
}

function toggleLocale() {
  locale.value = locale.value === 'zh' ? 'en' : 'zh'
}

export function useI18n() {
  return {
    locale,
    isZh: computed(() => locale.value === 'zh'),
    isEn: computed(() => locale.value === 'en'),
    setLocale,
    toggleLocale,
    t
  }
}
