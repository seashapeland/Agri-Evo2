<template>
  <div class="dna-generate">
    <!-- 主体布局 -->
    <div class="main-panel">
      <!-- 左侧：Input -->
      <div class="card input-panel">
        <div class="panel-header">
          <svg class="panel-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="6" width="14" height="12" rx="2.5" stroke="currentColor" stroke-width="1.5"/>
            <path d="M10.5 9L14 12L10.5 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M14 12H21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <h3>{{ t('dna.input') }}</h3>
        </div>

        <div class="scrollable-content">
          <!-- 模型选择 -->
          <div class="form-item">
            <div class="form-label">
              <svg class="label-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 10C3 6.22876 3 4.34315 4.17157 3.17157C5.34315 2 7.22876 2 11 2H13C16.7712 2 18.6569 2 19.8284 3.17157C21 4.34315 21 6.22876 21 10V14C21 17.7712 21 19.6569 19.8284 20.8284C18.6569 22 16.7712 22 13 22H11C7.22876 22 5.34315 22 4.17157 20.8284C3 19.6569 3 17.7712 3 14V10Z" stroke="currentColor" stroke-width="1.5"/>
                <path d="M8 2V5M16 2V5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M3 10H21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              <span>{{ t('dna.modelSelect') }}</span>
            </div>
            <div class="model-selector">
              <button
                v-for="item in modelOptions"
                :key="item.value"
                type="button"
                class="model-chip"
                :class="{ active: model === item.value }"
                @click="model = item.value"
              >
                <span class="model-name">{{ item.label }}</span>
                <small v-if="item.tag" class="model-tag">{{ item.tag }}</small>
              </button>
            </div>
          </div>

          <!-- 任务选择 -->
          <div class="form-item">
            <div class="form-label">
              <svg class="label-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M4 7.5C4 5.567 5.567 4 7.5 4H16.5C18.433 4 20 5.567 20 7.5V16.5C20 18.433 18.433 20 16.5 20H7.5C5.567 20 4 18.433 4 16.5V7.5Z" stroke="currentColor" stroke-width="1.5"/>
                <path d="M8 8H16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M8 12H16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M8 16H12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              <span>{{ t('dna.taskSelect') }}</span>
            </div>
            <div class="model-selector">
              <button
                v-for="item in taskOptions"
                :key="item.value"
                type="button"
                class="model-chip"
                :class="{ active: task === item.value }"
                @click="task = item.value"
              >
                <span class="model-name">{{ item.label }}</span>
              </button>
            </div>
          </div>

          <!-- DNA Sequence -->
          <div class="form-item">
            <div class="form-label">
              <svg class="label-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 10H21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M3 18H21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M3 6H21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M7 3V21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M12 3V21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M17 3V21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              <span>{{ t('dna.dnaSequence') }}</span>
            </div>
            <div class="textarea-wrapper">
              <textarea
                v-model="inputSeq"
                @input="onSeqInput"
                :placeholder="t('dna.seqPlaceholder', { max: maxSeqLength })"
                class="dna-textarea"
                :class="{ error: isSeqTooLong }"
              />
              <button
                v-if="inputSeq.length"
                type="button"
                class="clear-input"
                @click="clearInput"
                :aria-label="t('dna.clearInputAria')"
              >
                ✕
              </button>
              <div class="char-count-below" :class="{ error: isSeqTooLong }">
                {{ inputSeq.length }} {{ t('dna.basePairs') }}
                <span v-if="isSeqTooLong" class="error-tail">
                  . {{ t('dna.seqTooLong', { max: maxSeqLength }) }}
                </span>
              </div>
            </div>
          </div>

          <!-- 生成参数 -->
          <div class="slider-section">
            <div class="section-header">
              <svg class="section-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 8L21 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M3 16L21 16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <circle cx="8" cy="8" r="2" stroke="currentColor" stroke-width="1.5"/>
                <circle cx="16" cy="16" r="2" stroke="currentColor" stroke-width="1.5"/>
              </svg>
              <span>{{ t('dna.params') }}</span>
            </div>
            
            <div class="sliders-grid">
              <div class="slider-item">
                <div class="slider-header">
                  <span class="slider-label">{{ t('dna.tokens') }}</span>
                  <input
                    type="number"
                    class="slider-value-input"
                    v-model="parameterDrafts.tokens"
                    min="0"
                    max="1000"
                    step="1"
                    @focus="onParameterFocus('tokens')"
                    @blur="onParameterBlur('tokens', $event)"
                    @keydown.enter.prevent="$event.target.blur()"
                  />
                </div>
                <input 
                  type="range" 
                  v-model.number="tokens"
                  min="0"
                  max="1000"
                  class="slider"
                  :style="{
                    '--progress': `${(tokens / 1000) * 100}%`,
                    '--color': '#3b82f6'
                  }"
                />
                <div class="slider-ticks">
                  <span>0</span>
                  <span>500</span>
                  <span>1000</span>
                </div>
              </div>

              <div class="slider-item">
                <div class="slider-header">
                  <span class="slider-label">{{ t('dna.temperature') }}</span>
                  <input
                    type="number"
                    class="slider-value-input"
                    v-model="parameterDrafts.temperature"
                    min="0.0"
                    max="2.0"
                    step="0.01"
                    @focus="onParameterFocus('temperature')"
                    @blur="onParameterBlur('temperature', $event)"
                    @keydown.enter.prevent="$event.target.blur()"
                  />
                </div>
                <input 
                  type="range" 
                  v-model.number="temperature"
                  min="0.0"
                  max="2.0"
                  step="0.01"
                  class="slider"
                  :style="{
                    '--progress': `${((temperature - 0.0) / 2.0) * 100}%`,
                    '--color': '#10b981'
                  }"
                />
                <div class="slider-ticks">
                  <span>0.0</span>
                  <span>1.0</span>
                  <span>2.0</span>
                </div>
              </div>

              <div class="slider-item">
                <div class="slider-header">
                  <span class="slider-label">{{ t('dna.topK') }}</span>
                  <span class="slider-value">{{ topk }}</span>
                </div>
                <input 
                  type="range" 
                  v-model.number="topk"
                  min="1"
                  max="10"
                  class="slider"
                  :style="{
                    '--progress': `${((topk - 1) / 9) * 100}%`,
                    '--color': '#8b5cf6'
                  }"
                />
                <div class="slider-ticks">
                  <span>1</span>
                  <span>5</span>
                  <span>10</span>
                </div>
              </div>

              <div class="slider-item">
                <div class="slider-header">
                  <span class="slider-label">{{ t('dna.topP') }}</span>
                  <span class="slider-value">{{ topp.toFixed(1) }}</span>
                </div>
                <input 
                  type="range" 
                  v-model.number="topp"
                  min="0.0"
                  max="1.0"
                  step="0.1"
                  class="slider"
                  :style="{
                    '--progress': `${((topp - 0.0) / 1.0) * 100}%`,
                    '--color': '#ef4444'
                  }"
                />
                <div class="slider-ticks">
                  <span>0.0</span>
                  <span>0.5</span>
                  <span>1.0</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        

        <!-- 操作按钮 -->
        <div class="actions">
          <button class="btn reset" @click="reset">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M2 12C2 17.5228 6.47715 22 12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M2 12H12M12 12L8 8M12 12L8 16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>{{ t('dna.resetParams') }}</span>
          </button>
          <button class="btn generate" :disabled="isLoading || isInputInvalid" @click="generate">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 12L21 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M12 3L12 21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <circle cx="12" cy="12" r="2" stroke="currentColor" stroke-width="1.5"/>
              <path d="M18.364 5.63604C21.8787 9.15076 21.8787 14.8492 18.364 18.3639C14.8492 21.8787 9.15076 21.8787 5.63604 18.3639C2.12132 14.8492 2.12132 9.15076 5.63604 5.63604" stroke="currentColor" stroke-width="1.5"/>
            </svg>
            <span>{{ t('dna.generateSeq') }}</span>
          </button>
        </div>
      </div>

      <!-- 右侧：Output -->
      <div class="card output-panel">
        <!-- 输出面板头部 -->
        <div class="output-header">
          <div class="header-left">
            <svg class="header-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="7" y="5" width="14" height="12" rx="2.5" stroke="currentColor" stroke-width="1.5"/>
              <path d="M13.5 15L10 12L13.5 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M3 12H10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            <h3>{{ t('dna.output') }}</h3>
          </div>
          <div class="header-right">
            <div class="score-display" aria-live="polite">
              <span class="score-label">{{ t('dna.score') }}</span>
              <span class="score-value">{{ scoreDisplay }}</span>
            </div>
            <div class="frame-selector">
              <span class="frame-label">{{ t('dna.frame') }}</span>
              <select v-model.number="readingFrame" class="frame-select" :aria-label="t('dna.frame')">
                <option
                  v-for="item in readingFrameOptions"
                  :key="item.value"
                  :value="item.value"
                >
                  {{ item.label }}
                </option>
              </select>
            </div>
            <div class="header-actions">
              <button class="copy-btn" @click="copyOutput" :title="t('dna.copySeq')">
                <svg class="copy-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="9" y="9" width="13" height="13" rx="2" stroke="currentColor" stroke-width="1.5"/>
                  <path d="M5 15H4C2.89543 15 2 14.1046 2 13V4C2 2.89543 2.89543 2 4 2H13C14.1046 2 15 2.89543 15 4V5" stroke="currentColor" stroke-width="1.5"/>
                </svg>
              </button>
              <button class="download-btn" @click="downloadOutput" :title="t('dna.downloadSeq')">
                <svg class="download-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 3V16M12 16L8 12M12 16L16 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M20 21H4C3.44772 21 3 20.5523 3 20V16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <div
          v-if="task === 'intron-generation' && outputInputSeq.length"
          class="intron-meta-row"
        >
          <span class="intron-meta-hint">{{ intronInsertHintText }}</span>
          <span class="intron-meta-value">{{ intronInsertStatLabel }} {{ intronInsertStatValue }}</span>
        </div>

        <!-- 序列展示框 -->
        <div class="sequence-display">
          <div class="sequence-wrapper">
            <div v-if="formattedLines.length" class="sequence-legend-row">
              <span
                v-for="item in sequenceLegendItems"
                :key="item.key"
                class="sequence-legend-item"
              >
                <i class="sequence-legend-dot" :class="`legend-${item.key}`" />
                {{ item.label }}
              </span>
            </div>
            <div
              class="sequence-content"
              :class="{ 'is-loading': isLoading }"
              ref="sequenceContainer"
              @copy="onSequenceCopy"
            >
                <template v-if="isLoading">
                  <div class="dna-helix" aria-live="polite">
                    <span
                      v-for="dot in helixDots"
                      :key="`a-${dot}`"
                      class="dna-node strand-a"
                      :style="nodeStyle(dot, 'a')"
                    />
                    <span
                      v-for="dot in helixDots"
                      :key="`b-${dot}`"
                      class="dna-node strand-b"
                      :style="nodeStyle(dot, 'b')"
                    />
                    <span
                      v-for="dot in helixDots"
                      :key="`c-${dot}`"
                      class="dna-bridge"
                      :style="bridgeStyle(dot)"
                    />
                  </div>
                </template>
              <template v-else>
                <div v-if="formattedLines.length" class="sequence-formatted">
                  <div
                    v-for="(line, lineIndex) in formattedLines"
                    :key="`line-${lineIndex}`"
                    class="sequence-line"
                    :style="{ '--char-width': '14px' }"
                  >
                    <div
                      class="line-bases"
                      :class="{ 'is-intron-selectable': task === 'intron-generation' }"
                      :style="{ width: `${line.totalChars * charWidth}px` }"
                      @click="onLineBasesClick($event, line)"
                    >
                      <span
                        v-for="(group, groupIndex) in line.groups"
                        :key="`line-${lineIndex}-group-${groupIndex}`"
                        class="base-group"
                        :class="[
                          group.type === 'input' ? 'group-input' : 'group-generated',
                          group.isCodon ? 'is-codon' : 'frame-lead',
                          group.isCodon
                            ? group.bucket % 2 === 0
                              ? 'codon-even'
                              : 'codon-odd'
                            : '',
                          group.codonKind === 'start' ? 'codon-start' : '',
                          group.codonKind === 'stop' ? 'codon-stop' : '',
                          selectedPos === group.letters[0].pos ? 'selected' : ''
                        ]"
                      @click="onGroupClick($event, group.letters[0].pos)"
                      >
                        {{ group.letters.map(letter => letter.base).join('') }}
                      </span>
                      <span
                        v-if="task === 'intron-generation' && line.insertOffset !== null"
                        class="intron-insert-marker"
                        :style="{ left: `${line.insertOffset * charWidth}px` }"
                      />
                    </div>
                    <div
                      class="line-scale"
                      :style="{ width: `${line.totalChars * charWidth}px` }"
                    >
                      <span
                        v-for="(tick, tickIndex) in line.ticks"
                        :key="`line-${lineIndex}-tick-${tickIndex}`"
                        class="scale-tick"
                        :style="{ left: `${tick.offset * charWidth}px` }"
                      >
                        <i></i>
                        <em>{{ tick.label }}</em>
                      </span>
                    </div>
                  </div>
                </div>
                <div v-else class="empty-sequence" :aria-label="t('dna.emptyAria')">
                  <svg class="empty-icon" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M20 14C20 10.6863 22.6863 8 26 8H38C41.3137 8 44 10.6863 44 14C44 23.9411 52 24 52 32C52 40 44 40.0589 44 50C44 53.3137 41.3137 56 38 56H26C22.6863 56 20 53.3137 20 50C20 40.0589 12 40 12 32C12 24 20 23.9411 20 14Z" stroke="#cbd5e1" stroke-width="2.4" />
                    <path d="M24 18L40 46" stroke="#cbd5e1" stroke-width="2.4" stroke-linecap="round"/>
                    <path d="M40 18L24 46" stroke="#cbd5e1" stroke-width="2.4" stroke-linecap="round"/>
                  </svg>
                </div>
              </template>
            </div>
            <div class="sequence-stats">
              <div class="stat-item">
                <div class="stat-label">{{ t('dna.inputSeq') }}</div>
                <div class="stat-value">{{ outputInputSeq.length }} {{ t('dna.chars') }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">{{ t('dna.generatedSeq') }}</div>
                <div class="stat-value">{{ outputGeneratedSeq.length }} {{ t('dna.chars') }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">{{ t('dna.totalLength') }}</div>
                <div class="stat-value">{{ outputTotalLength }} {{ t('dna.chars') }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { useI18n } from '../i18n'
import { fetchAvailableModels, fetchCdsCompletion } from '../api/dnaGenerte'

const { t, isZh } = useI18n()

/* 输入状态 */
const defaults = {
  model: '',
  task: 'cds-completion',
  readingFrame: 1,
  tokens: 200,
  temperature: 1.0,
  topk: 4,
  topp: 1.0
}

const availableModels = ref([])

const formatModelLabel = modelName => {
  const normalized = String(modelName ?? '').trim().replace(/_/g, '-')
  if (!normalized) return ''
  return normalized.charAt(0).toUpperCase() + normalized.slice(1)
}

const modelOptions = computed(() =>
  availableModels.value.map(modelName => ({
    value: modelName,
    label: formatModelLabel(modelName)
  }))
)

const taskOptions = computed(() => [
  { value: 'cds-completion', label: t('dna.taskCds') },
  { value: 'promoter-extension', label: t('dna.taskPromoter') },
  { value: 'intron-generation', label: t('dna.taskIntron') }
])

const readingFrameOptions = [
  { value: 1, label: 'F1' },
  { value: 2, label: 'F2' },
  { value: 3, label: 'F3' }
]

const model = ref(defaults.model)
const task = ref(defaults.task)
const readingFrame = ref(defaults.readingFrame)
const inputSeq = ref('')
const maxSeqLength = 500
const tokens = ref(defaults.tokens)
const temperature = ref(defaults.temperature)
const topk = ref(defaults.topk)
const topp = ref(defaults.topp)
const displayInputSeq = ref('')
const displayGeneratedSeq = ref('')
const selectedPos = ref(null)
const isLoading = ref(false)
const helixDots = Array.from({ length: 12 }, (_, i) => i)
const waveDuration = 1.2
const waveStep = waveDuration / (helixDots.length - 1)
const tickStep = 10
const lineWidth = ref(50)
const sequenceContainer = ref(null)
const charWidth = ref(8)

const parameterRules = {
  tokens: {
    min: 0,
    max: 1000,
    step: 1,
    decimals: 0,
    ref: tokens
  },
  temperature: {
    min: 0,
    max: 2,
    step: 0.01,
    decimals: 2,
    ref: temperature
  },
  topk: {
    min: 1,
    max: 10,
    step: 1,
    decimals: 0,
    ref: topk
  },
  topp: {
    min: 0,
    max: 1,
    step: 0.1,
    decimals: 1,
    ref: topp
  }
}

const parameterDrafts = reactive({
  tokens: String(tokens.value),
  temperature: temperature.value.toFixed(2)
})

const parameterEditing = reactive({
  tokens: false,
  temperature: false
})

/* 输出状态 */
const outputTab = ref('preview')
const generatedSeq = ref('')
const generatedPrefixSeq = ref('')
const generatedSuffixSeq = ref('')
const intronInsertIndex = ref(-1)
const generationScore = ref(null)

const scoreDisplay = computed(() => {
  if (generationScore.value == null) return '--'
  return generationScore.value.toFixed(4)
})

const mockLikelihoodScore = sequence => {
  if (!sequence) return null
  let hash = 0
  for (let i = 0; i < sequence.length; i += 1) {
    hash = (hash * 33 + sequence.charCodeAt(i)) >>> 0
  }
  return 0.7 + (hash % 3000) / 10000
}

const defaultIntronInsertIndex = exonLength =>
  exonLength <= 1 ? exonLength : Math.floor(exonLength / 2)

const resolveIntronInsertIndex = exonLength => {
  if (exonLength <= 0) return 0
  if (intronInsertIndex.value < 0) return defaultIntronInsertIndex(exonLength)
  return Math.min(exonLength, Math.max(0, Math.floor(intronInsertIndex.value)))
}

const clearOutputState = () => {
  generatedSeq.value = ''
  generatedPrefixSeq.value = ''
  generatedSuffixSeq.value = ''
  intronInsertIndex.value = -1
  generationScore.value = null
  displayInputSeq.value = ''
  displayGeneratedSeq.value = ''
  selectedPos.value = null
}

const resolveDefaultModel = () => modelOptions.value[0]?.value || defaults.model

const loadModelOptions = async () => {
  try {
    const data = await fetchAvailableModels()
    const models = Array.isArray(data.available_models)
      ? data.available_models.filter(item => typeof item === 'string' && item.trim())
      : []

    availableModels.value = models

    if (!models.includes(model.value)) {
      model.value = resolveDefaultModel()
    }
  } catch {
    availableModels.value = []
    model.value = defaults.model
  }
}

/* mock 生成 */
async function generate() {
  isLoading.value = true
  generatedSeq.value = ''
  generatedPrefixSeq.value = ''
  generatedSuffixSeq.value = ''
  try {
    if (task.value === 'promoter-extension') {
      /*time out */
      await new Promise(resolve => setTimeout(resolve, 5000))
      const prefix = 'AAGCTTGCATGCCTGCAGGTCACTAGTAGCTTATATAAGGGAGGTGGTGGAGGAGGAAGCC'
      const suffix = 'GCATGCCGCGCTCGAGCTCTAGAGGGTATATAATGGCGGCCGCTCGAGCATGCATCTAGAGGGCCCAATTCGCCCTATAGTGAGTCGTATTACAATTCACTGGCCGTCGTTTTACAACGTCGTGACTGGGAAAACCCTA'
      generatedPrefixSeq.value = prefix
      generatedSuffixSeq.value = suffix
      generatedSeq.value = `${prefix}${inputSeq.value}${suffix}`
      displayInputSeq.value = inputSeq.value
      displayGeneratedSeq.value = `${prefix}${suffix}`
    } else if (task.value === 'intron-generation') {
      await new Promise(resolve => setTimeout(resolve, 5000))
      const intron = 'CTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCCCCCTCCCTCCCTCCCTCCCTCCCTCCCTCCCTCCCTCCCTCCCTCCCTCCCTCCCTCCCTTCTTCTTCTTCTTCTTCTTCTTCTTCTTCTTCTTCTTCTTCTTCTTCTTCTTTAATTTATTTATTTATTTATTTATTTATTTATTTATTTATTTATTTTTTTTTTTTTTTTTTT'
      const exon = inputSeq.value
      const insertAt = resolveIntronInsertIndex(exon.length)

      generatedSeq.value = intron
      intronInsertIndex.value = insertAt
      displayInputSeq.value = exon
      displayGeneratedSeq.value = intron
    } else {
      const data = await fetchCdsCompletion({
        prompt: inputSeq.value,
        model: model.value,
        tokens: tokens.value,
        temperature: temperature.value,
        topk: topk.value
      })
      /*const data = {
        result: {
          generated: 'GAGAGAGCTCTCTCTCTCTCTGAGAGAGAG'
        }
      }*/
      const result = data?.result ?? {}
      const generated = String(result.generated ?? '')
      const fullSequence = String(result.full_sequence ?? '')
      const generatedSegment =
        generated ||
        (fullSequence.startsWith(inputSeq.value)
          ? fullSequence.slice(inputSeq.value.length)
          : fullSequence)

      generatedSeq.value = generatedSegment || fullSequence
      displayInputSeq.value = inputSeq.value
      displayGeneratedSeq.value = generatedSegment
    }

    generationScore.value = mockLikelihoodScore(generatedSeq.value)
    selectedPos.value = null
  } catch {
    clearOutputState()
    if (typeof window !== 'undefined') {
      window.alert(pickLocaleText('CDS 生成失败，请稍后重试。', 'CDS generation failed. Please try again.'))
    }
  } finally {
    isLoading.value = false
  }
}

function reset() {
  model.value = resolveDefaultModel()
  task.value = defaults.task
  readingFrame.value = defaults.readingFrame
  tokens.value = defaults.tokens
  temperature.value = defaults.temperature
  topk.value = defaults.topk
  topp.value = defaults.topp
  clearOutputState()
}

const pickLocaleText = (zhText, enText) => (isZh.value ? zhText : enText)

const escapeHtml = value =>
  String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')

const formatDateForFilename = date => {
  const yyyy = date.getFullYear()
  const mm = String(date.getMonth() + 1).padStart(2, '0')
  const dd = String(date.getDate()).padStart(2, '0')
  const hh = String(date.getHours()).padStart(2, '0')
  const mi = String(date.getMinutes()).padStart(2, '0')
  const ss = String(date.getSeconds()).padStart(2, '0')
  return `${yyyy}${mm}${dd}-${hh}${mi}${ss}`
}

const triggerDownload = (filename, content, mimeType) => {
  if (typeof document === 'undefined') return
  const blob = new Blob([content], { type: mimeType })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

const copyTextToClipboard = async text => {
  if (!text) return false
  if (typeof navigator !== 'undefined' && navigator.clipboard?.writeText) {
    try {
      await navigator.clipboard.writeText(text)
      return true
    } catch {
      // fallback below
    }
  }
  if (typeof document === 'undefined') return false
  const textarea = document.createElement('textarea')
  textarea.value = text
  textarea.setAttribute('readonly', '')
  textarea.style.position = 'fixed'
  textarea.style.opacity = '0'
  textarea.style.pointerEvents = 'none'
  document.body.appendChild(textarea)
  textarea.select()
  textarea.setSelectionRange(0, textarea.value.length)
  let copied = false
  try {
    copied = document.execCommand('copy')
  } finally {
    document.body.removeChild(textarea)
  }
  return copied
}

const reportLineGroupClasses = group => {
  const classes = [group.type === 'input' ? 'group-input' : 'group-generated']
  if (group.isCodon) {
    classes.push('is-codon')
    classes.push(group.bucket % 2 === 0 ? 'codon-even' : 'codon-odd')
  } else {
    classes.push('frame-lead')
  }
  if (group.codonKind === 'start') classes.push('codon-start')
  if (group.codonKind === 'stop') classes.push('codon-stop')
  return classes.join(' ')
}

const REPORT_CHARS_PER_LINE = 96

const buildOutputLetters = () => {
  const letters = []
  let position = 1

  outputSegments.value.forEach(segment => {
    segment.sequence.split('').forEach(base => {
      letters.push({
        base,
        type: segment.type,
        pos: position
      })
      position += 1
    })
  })

  if (task.value === 'cds-completion') {
    const codonKindByPos = new Map()
    const sequence = letters.map(letter => letter.base).join('')
    const frameStartIndex = readingFrame.value - 1

    for (let idx = frameStartIndex; idx + 2 < sequence.length; idx += 3) {
      const codon = sequence.slice(idx, idx + 3)
      let kind = ''

      if (codon === 'ATG') {
        kind = 'start'
      } else if (codon === 'TAA' || codon === 'TAG' || codon === 'TGA') {
        kind = 'stop'
      }

      if (kind) {
        codonKindByPos.set(idx + 1, kind)
        codonKindByPos.set(idx + 2, kind)
        codonKindByPos.set(idx + 3, kind)
      }
    }

    letters.forEach(letter => {
      letter.codonKind = codonKindByPos.get(letter.pos) || ''
    })
  }

  return letters
}

const buildReportPreviewLines = () => {
  const letters = buildOutputLetters()
  if (!letters.length) return []

  const width = Math.max(20, REPORT_CHARS_PER_LINE)
  const localFrameBucket = pos => {
    if (pos < readingFrame.value) return `lead-${pos}`
    return Math.floor((pos - readingFrame.value) / 3)
  }

  const lines = []
  for (let cursor = 0; cursor < letters.length; cursor += width) {
    const slice = letters.slice(cursor, cursor + width)
    if (!slice.length) break

    const groups = []
    slice.forEach(letter => {
      const bucket = localFrameBucket(letter.pos)
      const prev = groups[groups.length - 1]
      const canMerge = prev && prev.type === letter.type && prev.bucket === bucket

      if (canMerge) {
        prev.letters.push(letter)
        return
      }

      groups.push({
        type: letter.type,
        bucket,
        isCodon: typeof bucket === 'number',
        codonKind: letter.codonKind || '',
        letters: [letter]
      })
    })

    const lineStartOffset = slice[0].pos - 1
    const lineEndOffset = lineStartOffset + slice.length
    let insertOffset = null

    if (intronInsertBoundary.value !== null) {
      const boundary = intronInsertBoundary.value
      if (boundary >= lineStartOffset && boundary <= lineEndOffset) {
        insertOffset = boundary - lineStartOffset
      }
    }

    lines.push({
      groups,
      insertOffset
    })
  }

  return lines
}

const buildSequencePreviewHtml = () => {
  const reportLines = buildReportPreviewLines()
  if (!reportLines.length) {
    return `<div class="report-empty">${escapeHtml(
      pickLocaleText('暂无可导出的序列结果', 'No sequence result to export')
    )}</div>`
  }

  return reportLines
    .map(line => {
      const groupsHtml = line.groups
        .map(group => {
          const text = escapeHtml(group.letters.map(letter => letter.base).join(''))
          return `<span class="base-group ${reportLineGroupClasses(group)}">${text}</span>`
        })
        .join('')

      const insertMarkerHtml =
        task.value === 'intron-generation' && line.insertOffset !== null
          ? `<span class="insert-marker" style="left:${line.insertOffset}ch"></span>`
          : ''

      return `
        <div class="sequence-line">
          <div class="line-bases">
            ${groupsHtml}
            ${insertMarkerHtml}
          </div>
        </div>
      `
    })
    .join('')
}

const buildExportReportHtml = () => {
  const now = new Date()
  const taskLabel = taskOptions.value.find(item => item.value === task.value)?.label || task.value
  const modelLabel = modelOptions.value.find(item => item.value === model.value)?.label || model.value
  const fullSequence = outputSegments.value.map(segment => segment.sequence).join('')
  const exportTime = now.toLocaleString(isZh.value ? 'zh-CN' : 'en-US')
  const metadataRows = [
    [pickLocaleText('任务', 'Task'), taskLabel],
    [pickLocaleText('模型', 'Model'), modelLabel],
    [pickLocaleText('得分', 'Score'), scoreDisplay.value],
    [pickLocaleText('阅读框', 'Frame'), `F${readingFrame.value}`],
    [pickLocaleText('生成长度', 'Tokens'), String(tokens.value)],
    [pickLocaleText('温度', 'Temperature'), temperature.value.toFixed(2)],
    [pickLocaleText('Top-K', 'Top-K'), String(topk.value)],
    [pickLocaleText('Top-P', 'Top-P'), topp.value.toFixed(1)],
    [pickLocaleText('导出时间', 'Exported at'), exportTime]
  ]

  if (task.value === 'intron-generation') {
    metadataRows.push([intronInsertStatLabel.value, intronInsertStatValue.value])
  }

  const metadataHtml = metadataRows
    .map(
      ([label, value]) =>
        `<div class="meta-item"><span class="meta-label">${escapeHtml(label)}</span><span class="meta-value">${escapeHtml(value)}</span></div>`
    )
    .join('')

  return `<!doctype html>
<html lang="${isZh.value ? 'zh' : 'en'}">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>${escapeHtml(pickLocaleText('CAU-Evo2 序列导出报告', 'CAU-Evo2 Sequence Export Report'))}</title>
    <style>
      body {
        margin: 0;
        padding: 28px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: #0f172a;
        background: #f8fafc;
      }
      .report {
        max-width: 1080px;
        margin: 0 auto;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 24px;
      }
      .title {
        margin: 0 0 4px;
        font-size: 24px;
        font-weight: 800;
        color: #1e293b;
      }
      .subtitle {
        margin: 0 0 18px;
        font-size: 13px;
        color: #64748b;
      }
      .meta-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 10px;
        margin-bottom: 18px;
      }
      .meta-item {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 9px 11px;
        background: #f8fafc;
      }
      .meta-label {
        display: block;
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 3px;
      }
      .meta-value {
        display: block;
        color: #0f172a;
        font-size: 13px;
        font-weight: 700;
      }
      .stats {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 18px;
      }
      .stats-item {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        background: #ffffff;
        padding: 8px 12px;
        font-size: 13px;
        font-weight: 700;
      }
      .stats-item span {
        color: #64748b;
        font-weight: 600;
        margin-right: 6px;
      }
      .legend {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 4px 0 12px;
        font-size: 12px;
      }
      .legend-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        color: #475569;
      }
      .legend-chip i {
        width: 10px;
        height: 10px;
        border-radius: 2px;
        display: inline-block;
      }
      .legend-input i { background: rgba(59, 130, 246, 0.22); }
      .legend-generated i { background: rgba(16, 185, 129, 0.24); }
      .legend-start i { background: #fef3c7; }
      .legend-stop i { background: #fee2e2; }
      .sequence-block {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        background: #ffffff;
        padding: 14px;
        margin-bottom: 16px;
      }
      .sequence-line {
        margin-bottom: 8px;
      }
      .line-bases {
        position: relative;
        display: flex;
        width: fit-content;
        background: #f8fafc;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        line-height: 1.6;
      }
      .base-group {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 1ch;
        font-weight: 600;
      }
      .group-input { color: #1d4ed8; background: rgba(59, 130, 246, 0.12); }
      .group-generated { color: #0f9f6e; background: rgba(16, 185, 129, 0.16); }
      .base-group.is-codon.codon-even.group-input { background: rgba(59, 130, 246, 0.18); }
      .base-group.is-codon.codon-odd.group-input { background: rgba(59, 130, 246, 0.11); }
      .base-group.is-codon.codon-even.group-generated { background: rgba(16, 185, 129, 0.24); }
      .base-group.is-codon.codon-odd.group-generated { background: rgba(16, 185, 129, 0.16); }
      .base-group.frame-lead { opacity: 0.85; }
      .base-group.codon-start {
        background: #fef3c7 !important;
        color: #92400e;
        box-shadow: inset 0 0 0 1px rgba(217, 119, 6, 0.28);
      }
      .base-group.codon-stop {
        background: #fee2e2 !important;
        color: #991b1b;
        box-shadow: inset 0 0 0 1px rgba(220, 38, 38, 0.24);
      }
      .insert-marker {
        position: absolute;
        top: -2px;
        bottom: -2px;
        width: 0;
        border-left: 2px solid #f59e0b;
      }
      .section-title {
        margin: 14px 0 8px;
        font-size: 14px;
        font-weight: 800;
        color: #334155;
      }
      .mono {
        font-family: 'Courier New', monospace;
        font-size: 13px;
        line-height: 1.5;
        color: #1e293b;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 10px 12px;
        white-space: pre-wrap;
        word-break: break-all;
      }
      .report-empty {
        color: #94a3b8;
        font-size: 13px;
      }
    </style>
  </head>
  <body>
    <div class="report">
      <h1 class="title">${escapeHtml(
        pickLocaleText('CAU-Evo2 序列导出报告', 'CAU-Evo2 Sequence Export Report')
      )}</h1>
      <p class="subtitle">${escapeHtml(
        pickLocaleText('包含任务信息、参数、长度统计与高亮序列视图', 'Contains task info, parameters, length stats and highlighted sequence view')
      )}</p>

      <div class="meta-grid">${metadataHtml}</div>

      <div class="stats">
        <div class="stats-item"><span>${escapeHtml(t('dna.inputSeq'))}</span>${escapeHtml(
          `${outputInputSeq.value.length} ${t('dna.chars')}`
        )}</div>
        <div class="stats-item"><span>${escapeHtml(t('dna.generatedSeq'))}</span>${escapeHtml(
          `${outputGeneratedSeq.value.length} ${t('dna.chars')}`
        )}</div>
        <div class="stats-item"><span>${escapeHtml(t('dna.totalLength'))}</span>${escapeHtml(
          `${outputTotalLength.value} ${t('dna.chars')}`
        )}</div>
      </div>

      <div class="legend">
        <span class="legend-chip legend-input"><i></i>${escapeHtml(pickLocaleText('输入序列', 'Input segment'))}</span>
        <span class="legend-chip legend-generated"><i></i>${escapeHtml(pickLocaleText('生成序列', 'Generated segment'))}</span>
        <span class="legend-chip legend-start"><i></i>${escapeHtml(pickLocaleText('起始密码子', 'Start codon'))}</span>
        <span class="legend-chip legend-stop"><i></i>${escapeHtml(pickLocaleText('终止密码子', 'Stop codon'))}</span>
      </div>

      <div class="sequence-block">${buildSequencePreviewHtml()}</div>

      <div class="section-title">${escapeHtml(pickLocaleText('完整序列', 'Full sequence'))}</div>
      <div class="mono">${escapeHtml(fullSequence)}</div>

      <div class="section-title">${escapeHtml(t('dna.generatedSeq'))}</div>
      <div class="mono">${escapeHtml(outputGeneratedSeq.value)}</div>
    </div>
  </body>
</html>`
}

function downloadOutput() {
  const hasResult = outputGeneratedSeq.value.length > 0 || outputInputSeq.value.length > 0
  if (!hasResult) return

  const taskLabel = taskOptions.value.find(item => item.value === task.value)?.value || 'sequence'
  const report = buildExportReportHtml()
  const timestamp = formatDateForFilename(new Date())
  const filename = `evo2-${taskLabel}-${timestamp}.html`
  triggerDownload(filename, report, 'text/html;charset=utf-8')
}

async function copyOutput() {
  const linesText = formattedLines.value
    .map(line => line.groups.map(group => group.letters.map(letter => letter.base).join('')).join(''))
    .filter(Boolean)
    .join('\n')
  const fullSequenceText = outputSegments.value.map(segment => segment.sequence).join('')
  const textToCopy = fullSequenceText || linesText.replace(/\s+/g, '')
  if (!textToCopy) return

  const copied = await copyTextToClipboard(textToCopy)
  if (!copied && typeof window !== 'undefined') {
    window.alert(pickLocaleText('复制失败，请手动复制。', 'Copy failed. Please copy manually.'))
  }
}

const nodeStyle = (dot, strand) => ({
  left: `${dot * 14}px`,
  // 两股同时起始，方向相反由各自关键帧决定
  animationDelay: `${dot * waveStep}s`
})

const bridgeStyle = dot => ({
  left: `${dot * 14}px`,
  animationDelay: `${dot * waveStep}s`
})

const outputSegments = computed(() => {
  if (task.value === 'promoter-extension') {
    return [
      { sequence: generatedPrefixSeq.value, type: 'generated' },
      { sequence: displayInputSeq.value, type: 'input' },
      { sequence: generatedSuffixSeq.value, type: 'generated' }
    ]
  }

  if (task.value === 'intron-generation') {
    const exon = outputInputSeq.value
    const insertAt = resolveIntronInsertIndex(exon.length)

    return [
      { sequence: exon.slice(0, insertAt), type: 'input' },
      { sequence: displayGeneratedSeq.value, type: 'generated' },
      { sequence: exon.slice(insertAt), type: 'input' }
    ]
  }

  return [
    { sequence: displayInputSeq.value, type: 'input' },
    { sequence: displayGeneratedSeq.value, type: 'generated' }
  ]
})

const outputInputSeq = computed(() => {
  if (task.value === 'intron-generation') {
    return displayInputSeq.value || inputSeq.value
  }
  return displayInputSeq.value
})

const outputGeneratedSeq = computed(() => displayGeneratedSeq.value)
const outputTotalLength = computed(() => outputInputSeq.value.length + outputGeneratedSeq.value.length)

const intronInsertStatLabel = computed(() => (isZh.value ? '插入位置' : 'Insert position'))

const intronInsertStatValue = computed(() => {
  if (task.value !== 'intron-generation') return '--'
  const exonLength = outputInputSeq.value.length
  if (!exonLength) return '--'
  const insertAt = resolveIntronInsertIndex(exonLength)
  const ratio = Math.round((insertAt / exonLength) * 100)
  return `${insertAt}/${exonLength} (${ratio}%)`
})

const intronInsertHintText = computed(() =>
  isZh.value
    ? '点击序列可调整内含子插入位置'
    : 'Click the sequence to change intron insertion position'
)

const intronInsertBoundary = computed(() => {
  if (task.value !== 'intron-generation') return null
  if (!outputInputSeq.value.length) return null
  return resolveIntronInsertIndex(outputInputSeq.value.length)
})

const sequenceLegendItems = computed(() => {
  const items = [
    {
      key: 'input',
      label: pickLocaleText('输入序列', 'Input sequence')
    },
    {
      key: 'generated',
      label: pickLocaleText('生成序列', 'Generated sequence')
    }
  ]

  if (task.value === 'cds-completion') {
    items.push(
      {
        key: 'start',
        label: pickLocaleText('起始密码子', 'Start codon')
      },
      {
        key: 'stop',
        label: pickLocaleText('终止密码子', 'Stop codon')
      }
    )
  }

  return items
})

const frameBucket = pos => {
  if (pos < readingFrame.value) return `lead-${pos}`
  return Math.floor((pos - readingFrame.value) / 3)
}

const formattedLines = computed(() => {
  const letters = []
  let position = 1

  outputSegments.value.forEach(segment => {
    segment.sequence.split('').forEach(base => {
      letters.push({
        base,
        type: segment.type,
        pos: position
      })
      position += 1
    })
  })

  if (task.value === 'cds-completion') {
    const codonKindByPos = new Map()
    const sequence = letters.map(letter => letter.base).join('')
    const frameStartIndex = readingFrame.value - 1

    for (let idx = frameStartIndex; idx + 2 < sequence.length; idx += 3) {
      const codon = sequence.slice(idx, idx + 3)
      let kind = ''

      if (codon === 'ATG') {
        kind = 'start'
      } else if (codon === 'TAA' || codon === 'TAG' || codon === 'TGA') {
        kind = 'stop'
      }

      if (kind) {
        codonKindByPos.set(idx + 1, kind)
        codonKindByPos.set(idx + 2, kind)
        codonKindByPos.set(idx + 3, kind)
      }
    }

    letters.forEach(letter => {
      letter.codonKind = codonKindByPos.get(letter.pos) || ''
    })
  }

  const lines = []
  const width = Math.max(10, lineWidth.value)

  for (let cursor = 0; cursor < letters.length; cursor += width) {
    const slice = letters.slice(cursor, cursor + width)
    if (!slice.length) break

    const groups = []
    slice.forEach(letter => {
      const bucket = frameBucket(letter.pos)
      const prev = groups[groups.length - 1]
      const canMerge =
        prev &&
        prev.type === letter.type &&
        prev.bucket === bucket

      if (canMerge) {
        prev.letters.push(letter)
        return
      }

      groups.push({
        type: letter.type,
        bucket,
        isCodon: typeof bucket === 'number',
        codonKind: letter.codonKind || '',
        letters: [letter]
      })
    })

    const firstPos = slice[0].pos
    const lastPos = slice[slice.length - 1].pos
    const ticks = []

    if (firstPos === 1) {
      // always show position 1 at the center of its character cell
      ticks.push({ label: 1, offset: 0.5 })
    }

    const startTick = Math.max(tickStep, Math.ceil(firstPos / tickStep) * tickStep)
    for (let p = startTick; p <= lastPos; p += tickStep) {
      ticks.push({ label: p, offset: (p - firstPos) + 0.5 })
    }

      const lineStartOffset = firstPos - 1
      const lineEndOffset = lineStartOffset + slice.length
      let insertOffset = null

      if (intronInsertBoundary.value !== null) {
        const boundary = intronInsertBoundary.value
        if (boundary >= lineStartOffset && boundary <= lineEndOffset) {
          insertOffset = boundary - lineStartOffset
        }
      }

      lines.push({
        groups,
        ticks,
        totalChars: slice.length,
        startOffset: lineStartOffset,
        insertOffset
    })
  }

  return lines
})

const isSeqTooLong = computed(() => inputSeq.value.length > maxSeqLength)
const isSeqEmpty = computed(() => inputSeq.value.length === 0)
const isInputInvalid = computed(() => isSeqTooLong.value || isSeqEmpty.value)

const sanitizeSeq = value =>
  value
    .toUpperCase()
    .replace(/[^ACGT]/g, '')

const normalizeParameterValue = (key, value) => {
  const rule = parameterRules[key]
  if (!rule || !Number.isFinite(value)) return null

  const clamped = Math.min(rule.max, Math.max(rule.min, value))
  const stepped = rule.min + Math.round((clamped - rule.min) / rule.step) * rule.step
  return Number(Math.min(rule.max, Math.max(rule.min, stepped)).toFixed(rule.decimals))
}

const formatParameterValue = key => {
  const rule = parameterRules[key]
  if (!rule) return ''

  const current = rule.ref.value
  return rule.decimals > 0 ? current.toFixed(rule.decimals) : String(current)
}

const onParameterFocus = key => {
  if (key in parameterEditing) {
    parameterEditing[key] = true
  }
}

const onParameterBlur = (key, event) => {
  const rawValue = event.target.value
  if (key in parameterEditing) {
    parameterEditing[key] = false
  }

  if (rawValue === '') {
    parameterDrafts[key] = formatParameterValue(key)
    return
  }

  const nextValue = normalizeParameterValue(key, Number(rawValue))
  if (nextValue != null) {
    parameterRules[key].ref.value = nextValue
  }

  parameterDrafts[key] = formatParameterValue(key)
}

watch(tokens, value => {
  if (!parameterEditing.tokens) {
    parameterDrafts.tokens = String(value)
  }
})

watch(temperature, value => {
  if (!parameterEditing.temperature) {
    parameterDrafts.temperature = value.toFixed(2)
  }
})

const onSeqInput = event => {
  const cleaned = sanitizeSeq(event.target.value)
  if (cleaned !== event.target.value) {
    event.target.value = cleaned
  }
  inputSeq.value = cleaned
}

const clearInput = () => {
  inputSeq.value = ''
}

const onSequenceCopy = event => {
  const selectedText = window.getSelection ? window.getSelection().toString() : ''
  if (!selectedText) return

  const cleaned = selectedText
    .toUpperCase()
    .replace(/[^A-Z]/g, '')

  if (!cleaned) return

  const clipboard = event.clipboardData || window.clipboardData
  if (!clipboard) return

  event.preventDefault()
  clipboard.setData('text/plain', cleaned)
}

const onLineBasesClick = (event, line) => {
  if (task.value !== 'intron-generation') return
  if (!outputInputSeq.value.length) return

  const rect = event.currentTarget.getBoundingClientRect()
  const x = Math.max(0, Math.min(rect.width, event.clientX - rect.left))
  const localBoundary = Math.round(x / (charWidth.value || 8))
  const combinedBoundary = line.startOffset + localBoundary

  const exonLength = outputInputSeq.value.length
  const generatedLength = outputGeneratedSeq.value.length
  const currentInsertAt = resolveIntronInsertIndex(exonLength)
  let nextInsertAt = combinedBoundary

  if (combinedBoundary > currentInsertAt) {
    if (combinedBoundary <= currentInsertAt + generatedLength) {
      nextInsertAt = currentInsertAt
    } else {
      nextInsertAt = combinedBoundary - generatedLength
    }
  }

  intronInsertIndex.value = Math.min(exonLength, Math.max(0, nextInsertAt))
  selectedPos.value = null
}

const onGroupClick = (event, pos) => {
  if (task.value === 'intron-generation') return
  event.stopPropagation()
  selectBase(pos)
}

const selectBase = pos => {
  selectedPos.value = pos
}

const updateLineWidth = () => {
  if (!sequenceContainer.value) return
  const rect = sequenceContainer.value.getBoundingClientRect()
  // padding-left/right = 24px each in .sequence-content
  const innerWidth = Math.max(0, rect.width - 48)
  const ch = charWidth.value || 8
  const charsPerLine = Math.max(10, Math.floor(innerWidth / ch))
  lineWidth.value = charsPerLine
}

watch(task, () => {
  clearOutputState()
})

onMounted(async () => {
  await loadModelOptions()

  // measure a single character width using a hidden span
  const probe = document.createElement('span')
  probe.style.visibility = 'hidden'
  probe.style.position = 'absolute'
  probe.style.fontFamily = "'Courier New', monospace"
  probe.style.fontSize = '16px'
  probe.textContent = 'A'
  document.body.appendChild(probe)
  charWidth.value = probe.getBoundingClientRect().width || 8
  document.body.removeChild(probe)

  updateLineWidth()
  const observer = new ResizeObserver(updateLineWidth)
  observer.observe(sequenceContainer.value)
  window.addEventListener('resize', updateLineWidth)

  onBeforeUnmount(() => {
    observer.disconnect()
    window.removeEventListener('resize', updateLineWidth)
  })
})


</script>

<style scoped>
.dna-generate {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.main-panel {
  flex: 1;
  display: flex;
  gap: 24px;
  min-height: 0;
}

/* 通用卡片 */
.card {
  background: #ffffff;
  border-radius: 2px;
  border: 1px solid #e2e8f0;
  padding: 28px;
  display: flex;
  border-radius: 16px;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}


.panel-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 28px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f1f5f9;
}

.panel-icon {
  width: 24px;
  height: 24px;
  color: #3b82f6;
}

.panel-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  flex: 1;
}

/* 左侧 Input */
.input-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: auto;
}

.scrollable-content {
  flex: 1;
  overflow-y: auto;
  padding-right: 8px; /* 为滚动条留出空间 */
}

.form-item {
  margin-bottom: 24px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.label-icon {
  width: 18px;
  height: 18px;
  color: #64748b;
}

.form-label span {
  font-size: 15px;
  font-weight: 600;
  color: #475569;
}

/* 模型选择器 */
.model-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.model-chip {
  padding: 12px 14px;
  border-radius: 14px;
  border: 1.5px solid #e2e8f0;
  background: #f8fafc;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-width: 120px;
  justify-content: space-between;
}

.model-chip:hover {
  border-color: #cbd5e1;
  background: #f1f5f9;
}

.model-chip.active {
  border-color: #2563eb;
  background: #ebf2ff;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.18);
}

.model-name {
  font-weight: 700;
  color: #1e293b;
  font-size: 15px;
}

.model-tag {
  padding: 2px 8px;
  border-radius: 999px;
  background: #e0f2fe;
  color: #075985;
  font-size: 12px;
  font-weight: 700;
}


/* DNA 输入框 */
.textarea-wrapper {
  position: relative;
  width: 100%;
}

.dna-textarea {
  width: 100%;             
  box-sizing: border-box;  
  padding: 16px 44px 16px 16px;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  background: #f8fafc;
  font-family: 'Courier New', monospace;
  font-size: 15px;
  line-height: 1.6;
  resize: none;
  height: 180px;
  transition: all 0.3s ease;
  min-height: 180px;
  max-height: 180px;
  overflow-y: auto;
}

.dna-textarea::-webkit-scrollbar {
  width: 12px;
}

.dna-textarea::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 999px;
}

.dna-textarea::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 999px;
  border: 3px solid #f8fafc;
}

.dna-textarea {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
}

.dna-textarea.error {
  border-color: #e11d48;
  background: #fff1f2;
  box-shadow: 0 0 0 3px rgba(225, 29, 72, 0.12);
  color: #e11d48;
  caret-color: #e11d48;
}

.dna-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.dna-textarea.error:focus {
  border-color: #e11d48;
  background: #fff1f2;
  box-shadow: 0 0 0 3px rgba(225, 29, 72, 0.12);
  color: #e11d48;
  caret-color: #e11d48;
}

.dna-textarea::placeholder {
  color: #94a3b8;
}

.char-count-below {
  margin-top: 8px;
  font-size: 12px;
  color: #64748b;
}

.char-count-below.error {
  color: #e11d48;
}

.error-tail {
  white-space: normal;
}

.clear-input {
  position: absolute;
  top: 8px;
  right: 14px;
  width: 20px;
  height: 20px;
  border: none;
  border-radius: 50%;
  background: #ffffff;
  color: #475569;
  cursor: pointer;
  font-size: 13px;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);
  z-index: 2;
}

.clear-input:hover {
  background: #e2e8f0;
  color: #1e293b;
}


/* 滑动条区域 */
.slider-section {
  background: #f8fafc;
  border-radius: 16px;
  padding: 20px;
  margin: 20px 0;
  margin-top: 5px;
  border: 1px solid #e2e8f0;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.section-icon {
  width: 20px;
  height: 20px;
  color: #64748b;
}

.section-header span {
  font-size: 16px;
  font-weight: 600;
  color: #475569;
}

.sliders-grid {
  display: grid;
  gap: 20px;
}

.slider-item {
  background: #ffffff;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #f1f5f9;
}

.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.slider-label {
  font-weight: 600;
  color: #475569;
  font-size: 14px;
}

.slider-value {
  font-family: 'Courier New', monospace;
  font-weight: 700;
  color: #1e293b;
  background: #f1f5f9;
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 15px;
  min-width: 50px;
  text-align: center;
}

.slider-value-input {
  font-family: 'Courier New', monospace;
  font-weight: 700;
  color: #1e293b;
  background: #f1f5f9;
  padding: 4px 12px;
  border-radius: 8px;
  border: 1px solid transparent;
  font-size: 15px;
  min-width: 72px;
  width: 72px;
  text-align: center;
  outline: none;
  transition: border-color 0.2s ease, background 0.2s ease, box-shadow 0.2s ease;
}

.slider-value-input:focus {
  background: #ffffff;
  border-color: #cbd5e1;
  box-shadow: 0 0 0 3px rgba(148, 163, 184, 0.14);
}

.slider-value-input::-webkit-outer-spin-button,
.slider-value-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.slider-value-input[type='number'] {
  -moz-appearance: textfield;
}

/* 自定义滑动条 */
.slider {
  -webkit-appearance: none;
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(to right, var(--color) 0%, var(--color) var(--progress), #e2e8f0 var(--progress), #e2e8f0 100%);
  outline: none;
  margin: 10px 0;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: white;
  border: 3px solid var(--color);
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
}

.slider::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.slider-ticks {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 12px;
  color: #64748b;
}

/* 操作按钮 */
.actions {
  margin-top: auto;
  display: flex;
  gap: 12px;
  padding-top: 20px;
  border-top: 1px solid #f1f5f9;
  
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 24px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  font-size: 15px;
  transition: all 0.3s ease;
  flex: 1;
}

.btn-icon {
  width: 18px;
  height: 18px;
}

.reset {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  color: #475569;
  border: 1px solid #cbd5e1;
}

.reset:hover {
  background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(148, 163, 184, 0.2);
}

.generate {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
}

.generate:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4);
}

.generate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* 右侧 Output */
/* 输出面板样式 */
.output-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

/* 头部样式 */
.output-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f1f5f9;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  width: 24px;
  height: 24px;
  color: #3b82f6;
}

.output-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 14px;
}

.score-display {
  height: 30px;
  min-width: 104px;
  padding: 0 8px;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  display: inline-flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.score-label {
  font-size: 12px;
  font-weight: 700;
  color: #64748b;
  white-space: nowrap;
}

.score-value {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: 0.02em;
}

.frame-selector {
  display: flex;
  align-items: center;
  gap: 6px;
}

.frame-label {
  font-size: 12px;
  font-weight: 700;
  color: #64748b;
  white-space: nowrap;
}

.frame-select {
  height: 30px;
  min-width: 64px;
  padding: 0 24px 0 8px;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  color: #334155;
  font-size: 12px;
  font-weight: 700;
  line-height: 1;
  outline: none;
  cursor: pointer;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.frame-select:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.14);
}

/* 头部操作按钮容器 */
.header-actions {
  display: flex;
  gap: 12px;
}

/* 复制按钮 */
.copy-btn {
  width: 60px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); /* 蓝色渐变 */
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
}

.copy-btn:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4);
}

.copy-btn:active {
  transform: translateY(0);
}

.copy-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.copy-icon {
  width: 20px;
  height: 20px;
}

/* 下载按钮 */
.download-btn {
  width: 60px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%); /* 绿色渐变 */
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.download-btn:hover {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.4);
}

.download-btn:active {
  transform: translateY(0);
}

.download-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.download-icon {
  width: 20px;
  height: 20px;
}

/* 序列展示框 */
.sequence-display {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.sequence-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f8fafc;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.sequence-legend-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px 14px;
  padding: 10px 16px;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.sequence-legend-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #475569;
}

.sequence-legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 2px;
  border: 1px solid transparent;
  flex: 0 0 auto;
}

.sequence-legend-dot.legend-input {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.3);
}

.sequence-legend-dot.legend-generated {
  background: rgba(16, 185, 129, 0.22);
  border-color: rgba(16, 185, 129, 0.34);
}

.sequence-legend-dot.legend-start {
  background: #fef3c7;
  border-color: rgba(217, 119, 6, 0.4);
}

.sequence-legend-dot.legend-stop {
  background: #fee2e2;
  border-color: rgba(220, 38, 38, 0.34);
}

.sequence-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  overflow-x: hidden;
  font-family: 'Courier New', monospace;
  font-size: 16px;
  line-height: 1.8;
  word-break: break-all;
  background: #ffffff;
}

.sequence-content.is-loading {
  display: flex;
  align-items: center;
  justify-content: center;
}

.sequence-formatted {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sequence-line {
  display: flex;
  flex-direction: column;
  gap: 6px;
  --char-width: 14px;
}

.line-bases {
  font-family: 'Courier New', monospace;
  font-size: 16px;
  line-height: 1.6;
  letter-spacing: 0;
  display: flex;
  align-items: stretch;
  position: relative;
  background: #f8fafc;
  border-radius: 6px;
  padding: 0;
  width: fit-content;
}

.line-bases.is-intron-selectable {
  cursor: crosshair;
}

.line-bases.is-intron-selectable:hover {
  background: #fff7ed;
  box-shadow: inset 0 0 0 1px rgba(245, 158, 11, 0.26);
}

.base-group {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1ch;
  padding: 0;
  margin: 0;
  font-weight: 600;
}

.group-input {
  color: #1d4ed8;
  background: rgba(59, 130, 246, 0.12);
}

.group-generated {
  color: #0f9f6e;
  background: rgba(16, 185, 129, 0.16);
}

.base-group.is-codon.codon-even.group-input {
  background: rgba(59, 130, 246, 0.18);
}

.base-group.is-codon.codon-odd.group-input {
  background: rgba(59, 130, 246, 0.11);
}

.base-group.is-codon.codon-even.group-generated {
  background: rgba(16, 185, 129, 0.24);
}

.base-group.is-codon.codon-odd.group-generated {
  background: rgba(16, 185, 129, 0.16);
}

.base-group.frame-lead {
  opacity: 0.85;
}

.base-group.codon-start {
  background: #fef3c7 !important;
  color: #92400e;
  box-shadow: inset 0 0 0 1px rgba(217, 119, 6, 0.28);
}

.base-group.codon-stop {
  background: #fee2e2 !important;
  color: #991b1b;
  box-shadow: inset 0 0 0 1px rgba(220, 38, 38, 0.24);
}

.base-group.selected {
  box-shadow: inset 0 0 0 1.5px rgba(15, 23, 42, 0.18);
}

.intron-insert-marker {
  position: absolute;
  top: -2px;
  bottom: -2px;
  width: 0;
  border-left: 2px solid #f59e0b;
  box-shadow: 0 0 0 1px rgba(245, 158, 11, 0.22);
  pointer-events: none;
  animation: intronMarkerPulse 1.6s ease-in-out infinite;
}

.intron-insert-marker::before {
  content: '';
  position: absolute;
  width: 6px;
  height: 6px;
  left: -4px;
  top: -4px;
  border-radius: 999px;
  background: #f59e0b;
}

@keyframes intronMarkerPulse {
  0%,
  100% {
    box-shadow: 0 0 0 1px rgba(245, 158, 11, 0.2);
  }
  50% {
    box-shadow: 0 0 0 1px rgba(245, 158, 11, 0.45), 0 0 0 4px rgba(245, 158, 11, 0.08);
  }
}

.intron-meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin: -2px 0 10px;
  padding: 0 2px;
  min-height: 18px;
}

.intron-meta-hint {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  color: #64748b;
}

.intron-meta-hint::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 999px;
  background: #f59e0b;
  opacity: 0.7;
}

.intron-meta-value {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  font-weight: 700;
  color: #475569;
  padding: 2px 8px;
  border-radius: 999px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  white-space: nowrap;
}

.line-scale {
  position: relative;
  height: 18px;
  width: fit-content;
  pointer-events: none;
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
}

.line-scale * {
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
}

.scale-tick {
  position: absolute;
  bottom: 0;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  font-size: 11px;
  color: #94a3b8;
  min-width: 20px;
}

.scale-tick i {
  display: block;
  width: 1px;
  height: 8px;
  background: #cbd5e1;
}

.scale-tick em {
  font-style: normal;
  font-weight: 600;
  color: #94a3b8;
}

.empty-sequence {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.empty-icon {
  width: 64px;
  height: 64px;
  color: #cbd5e1;
}
.dna-helix {
  position: relative;
  width: 170px;
  height: 70px;
}

.dna-node {
  position: absolute;
  border-radius: 50%;
  width: 7px;
  height: 7px;
  transform-origin: center;
  animation-duration: 1.2s;
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.12));
}

.strand-a {
  background: #2563eb;
  animation-name: waveA;
  animation-delay: calc(var(--i) * 0.06s);
}

.strand-b {
  background: #60a5fa;
  animation-name: waveB;
  animation-delay: calc(var(--i) * 0.06s + 0.65s);
}

.dna-bridge {
  position: absolute;
  width: 2px;
  height: 22px;
  top: 24px;
  background: rgba(37, 99, 235, 0.18);
  transform-origin: center;
  animation: bridgePulse 1.2s ease-in-out infinite;
}

@keyframes waveA {
  0%   { transform: translateY(16px) scale(0.65); opacity: 0.55; }
  25%  { transform: translateY(0px)  scale(0.9);  opacity: 0.85; }
  50%  { transform: translateY(-18px) scale(1.15); opacity: 1; }
  75%  { transform: translateY(0px)  scale(0.9);  opacity: 0.85; }
  100% { transform: translateY(16px) scale(0.65); opacity: 0.55; }
}

@keyframes waveB {
  0%   { transform: translateY(-16px) scale(0.65); opacity: 0.55; }
  25%  { transform: translateY(0px)   scale(0.9);  opacity: 0.85; }
  50%  { transform: translateY(18px)  scale(1.15); opacity: 1; }
  75%  { transform: translateY(0px)   scale(0.9);  opacity: 0.85; }
  100% { transform: translateY(-16px) scale(0.65); opacity: 0.55; }
}

@keyframes bridgePulse {
  0%, 100% { opacity: 0.12; transform: scaleY(0.65); }
  50%      { opacity: 0.28; transform: scaleY(1.05); }
}

/* 序列配色 */
.input-sequence {
  color: #2563eb; /* 蓝色 */
  font-weight: 500;
}

.generated-sequence {
  color: #10b981; /* 绿色 */
  font-weight: 500;
}

/* 统计信息 */
.sequence-stats {
  display: flex;
  background: #ffffff;
  border-top: 1px solid #e2e8f0;
  padding: 16px 24px;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #f8fafc;
  border-radius: 10px;
  border: 1px solid #f1f5f9;
}

.stat-label {
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
}

.stat-value {
  font-size: 14px;
  font-weight: 700;
  color: #1e293b;
  font-family: 'Courier New', monospace;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .output-header {
    align-items: flex-start;
  }

  .header-right {
    width: 100%;
    flex-direction: column;
    align-items: flex-end;
    gap: 10px;
  }

  .frame-selector {
    align-self: flex-end;
  }

  .score-display {
    align-self: flex-end;
  }

  .intron-meta-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
    margin-bottom: 8px;
  }

  .sequence-stats {
    flex-direction: column;
    gap: 8px;
  }
  
  .stat-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-panel {
    flex-direction: column;
  }
  
  .txt-stats {
    grid-template-columns: repeat(1, 1fr);
  }
}

@media (max-width: 768px) {
  .dna-generate {
    padding: 16px;
  }
  
  .card {
    padding: 20px;
  }
  
  .model-selector {
    grid-template-columns: repeat(1, 1fr);
  }
}
</style>
