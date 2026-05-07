<template>
  <div class="sequence-analysis">
    <div class="header-section">
      <div class="title-wrapper">
        <svg class="title-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 17L9 19C9 20.1046 9.89543 21 11 21H19C20.1046 21 21 20.1046 21 19V11C21 9.89543 20.1046 9 19 9H17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M15 9H5C3.89543 9 3 8.10457 3 7V5C3 3.89543 3.89543 3 5 3H13C14.1046 3 15 3.89543 15 5V15C15 16.1046 14.1046 17 13 17H11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M8 13L12 17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M12 13L8 17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M12 8L16 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <h2>{{ t('analysis.title') }}</h2>
      </div>
      <div class="description">
        {{ t('analysis.description') }}
      </div>
    </div>

    <div class="input-section">
      <div class="sequences-row">
        <div class="sequence-input original-sequence">
          <div class="input-header">
            <div class="input-title">
              <div class="color-indicator" style="background: #2563eb;"></div>
              <span>{{ t('analysis.originalSeq') }}</span>
            </div>
            <div class="char-count">{{ t('analysis.chars', { count: originalSeq.length }) }}</div>
          </div>
          <div class="textarea-wrapper">
            <textarea
              v-model="originalSeq"
              :placeholder="t('analysis.originalPlaceholder')"
              rows="8"
              class="sequence-textarea"
              :style="{ borderColor: '#2563eb30' }"
            ></textarea>
          </div>
          <div class="sequence-info">
            <div class="nucleotide-stats">
              <span class="stat-item">A: {{ countNucleotides(originalSeq).A }}</span>
              <span class="stat-item">C: {{ countNucleotides(originalSeq).C }}</span>
              <span class="stat-item">G: {{ countNucleotides(originalSeq).G }}</span>
              <span class="stat-item">T: {{ countNucleotides(originalSeq).T }}</span>
            </div>
          </div>
        </div>

        <div class="sequence-input generated-sequence">
          <div class="input-header">
            <div class="input-title">
              <div class="color-indicator" style="background: #10b981;"></div>
              <span>{{ t('analysis.generatedSeq') }}</span>
            </div>
            <div class="char-count">{{ t('analysis.chars', { count: generatedSeq.length }) }}</div>
          </div>
          <div class="textarea-wrapper">
            <textarea
              v-model="generatedSeq"
              :placeholder="t('analysis.generatedPlaceholder')"
              rows="8"
              class="sequence-textarea"
              :style="{ borderColor: '#10b98130' }"
            ></textarea>
          </div>
          <div class="sequence-info">
            <div class="nucleotide-stats">
              <span class="stat-item">A: {{ countNucleotides(generatedSeq).A }}</span>
              <span class="stat-item">C: {{ countNucleotides(generatedSeq).C }}</span>
              <span class="stat-item">G: {{ countNucleotides(generatedSeq).G }}</span>
              <span class="stat-item">T: {{ countNucleotides(generatedSeq).T }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="control-section">
      <div class="control-buttons">
        <button class="control-btn clear-btn" @click="clearAll">
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <path d="M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span>{{ t('analysis.clear') }}</span>
        </button>
        <button
          class="control-btn generate-btn"
          :class="{ 'is-loading': isGenerating }"
          :disabled="isGenerating"
          @click="generateMetrics"
        >
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 17L9 19C9 20.1046 9.89543 21 11 21H19C20.1046 21 21 20.1046 21 19V11C21 9.89543 20.1046 9 19 9H17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <path d="M15 9H5C3.89543 9 3 8.10457 3 7V5C3 3.89543 3.89543 3 5 3H13C14.1046 3 15 3.89543 15 5V15C15 16.1046 14.1046 17 13 17H11" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span class="btn-label">
            {{ isGenerating ? `${t('analysis.generateMetrics')}...` : t('analysis.generateMetrics') }}
          </span>
          <span v-if="isGenerating" class="btn-spinner" aria-hidden="true"></span>
        </button>
      </div>
    </div>

    <div v-if="showMetrics" class="metrics-section">
      <div class="metrics-header">
        <svg class="metrics-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M3 10H21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M3 18H21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M3 6H21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M7 3V21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M12 3V21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M17 3V21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span>{{ t('analysis.results') }}</span>
      </div>

      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-header">
            <div class="metric-icon" style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z" stroke="white" stroke-width="2"/>
                <path d="M12 6V12L16 14" stroke="white" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <div class="metric-info">
              <div class="metric-title">{{ t('analysis.likelihood') }}</div>
              <div class="metric-subtitle">{{ t('analysis.likelihoodSub') }}</div>
            </div>
          </div>
          <div class="metric-value">{{ metrics.likelihood.toFixed(2) }}</div>
          <div class="metric-progress">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: (metrics.likelihood * 100) + '%' }"></div>
            </div>
            <div class="progress-label">{{ (metrics.likelihood * 100).toFixed(1) }}%</div>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-header">
            <div class="metric-icon" style="background: linear-gradient(135deg, #10b981 0%, #047857 100%);">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 13L12 17L20 9" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M3 12C3 12 5.63636 4 12 4C18.3636 4 22 12 22 12C22 12 18.3636 20 12 20C5.63636 20 3 12 3 12Z" stroke="white" stroke-width="2"/>
              </svg>
            </div>
            <div class="metric-info">
              <div class="metric-title">{{ t('analysis.similarity') }}</div>
              <div class="metric-subtitle">{{ t('analysis.similaritySub') }}</div>
            </div>
          </div>
          <div class="metric-value">{{ (metrics.similarity * 100).toFixed(1) }}%</div>
          <div class="metric-progress">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: (metrics.similarity * 100) + '%' }"></div>
            </div>
            <div class="progress-label">{{ (metrics.similarity * 100).toFixed(1) }}%</div>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-header">
            <div class="metric-icon" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="metric-info">
              <div class="metric-title">{{ t('analysis.recovery') }}</div>
              <div class="metric-subtitle">{{ t('analysis.recoverySub') }}</div>
            </div>
          </div>
          <div class="metric-value">{{ (metrics.recoveryRate * 100).toFixed(1) }}%</div>
          <div class="metric-progress">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: (metrics.recoveryRate * 100) + '%' }"></div>
            </div>
            <div class="progress-label">{{ (metrics.recoveryRate * 100).toFixed(1) }}%</div>
          </div>
        </div>
      </div>

      <div class="analysis-summary">
        <div class="summary-title">{{ t('analysis.summary') }}</div>
        <div class="summary-content">
          {{ t('analysis.summaryText', { similarityLevel: getSimilarityLevel(metrics.similarity), recoveryLevel: getRecoveryLevel(metrics.recoveryRate) }) }}
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <svg class="empty-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M9 17L9 19C9 20.1046 9.89543 21 11 21H19C20.1046 21 21 20.1046 21 19V11C21 9.89543 20.1046 9 19 9H17" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round"/>
        <path d="M15 9H5C3.89543 9 3 8.10457 3 7V5C3 3.89543 3.89543 3 5 3H13C14.1046 3 15 3.89543 15 5V15C15 16.1046 14.1046 17 13 17H11" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round"/>
      </svg>
      <div class="empty-text">{{ t('analysis.emptyHint') }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'
import { useI18n } from '../i18n'

const { t } = useI18n()

const originalSeq = ref('ATGCGATACGTTACGATGCGATACGTTACG')
const generatedSeq = ref('ATGCGTTACGTTACGATGCGTTACGTTACG')
const showMetrics = ref(false)
const isGenerating = ref(false)

const metrics = ref({
  likelihood: 0.85,
  similarity: 0.76,
  recoveryRate: 0.82
})

function countNucleotides(sequence) {
  return {
    A: (sequence.match(/A/gi) || []).length,
    C: (sequence.match(/C/gi) || []).length,
    G: (sequence.match(/G/gi) || []).length,
    T: (sequence.match(/T/gi) || []).length
  }
}

function clearAll() {
  originalSeq.value = ''
  generatedSeq.value = ''
  showMetrics.value = false
}

function normalizeSequence(sequence) {
  return String(sequence || '').toUpperCase().replace(/\s+/g, '')
}

function getErrorMessage(err, fallback) {
  const detail = err?.response?.data?.detail
  const nestedError = err?.response?.data?.error
  if (typeof detail === 'string' && detail) return detail
  if (typeof nestedError === 'string' && nestedError) return nestedError
  if (typeof err?.message === 'string' && err.message) return err.message
  return fallback
}

async function generateMetrics() {
  if (isGenerating.value) return
  const reference = normalizeSequence(originalSeq.value)
  const generated = normalizeSequence(generatedSeq.value)

  if (!reference || !generated) {
    alert(t('analysis.alertMissingInput'))
    return
  }

  isGenerating.value = true
  try {
    const [likelihoodResp, compareResp] = await Promise.all([
      api.post('/dnaAnalysis/likelihood/', {
        model: 'evo2_1b',
        sequence: generated
      }, { timeout: 300000 }),
      api.post('/dnaAnalysis/compare/', {
        reference,
        generated
      }, { timeout: 300000 })
    ])

    const likelihoodScore = Number(likelihoodResp?.data?.quality_score_0_to_1 ?? 0)
    const similarity = Number(compareResp?.data?.global_alignment?.similarity ?? 0)
    const recoveryRate = Number(compareResp?.data?.aa_recovery?.recovery ?? 0)

    metrics.value = {
      likelihood: Number.isFinite(likelihoodScore) ? Math.min(Math.max(likelihoodScore, 0), 1) : 0,
      similarity: Number.isFinite(similarity) ? Math.min(Math.max(similarity, 0), 1) : 0,
      recoveryRate: Number.isFinite(recoveryRate) ? Math.min(Math.max(recoveryRate, 0), 1) : 0
    }

    showMetrics.value = true
  } catch (err) {
    const msg = getErrorMessage(err, 'Generate metrics failed.')
    alert(msg)
  } finally {
    isGenerating.value = false
  }
}

function getSimilarityLevel(similarity) {
  if (similarity > 0.8) return t('analysis.similarityHigh')
  if (similarity > 0.6) return t('analysis.similarityMedium')
  if (similarity > 0.4) return t('analysis.similarityLow')
  return t('analysis.similarityVeryLow')
}

function getRecoveryLevel(recovery) {
  if (recovery > 0.8) return t('analysis.recoveryGood')
  if (recovery > 0.6) return t('analysis.recoveryMedium')
  if (recovery > 0.4) return t('analysis.recoveryFair')
  return t('analysis.recoveryPoor')
}

function getSimilarityColor(similarity) {
  if (similarity > 0.8) return '#10b981'
  if (similarity > 0.6) return '#3b82f6'
  if (similarity > 0.4) return '#f59e0b'
  return '#ef4444'
}

function getRecoveryColor(recovery) {
  if (recovery > 0.8) return '#10b981'
  if (recovery > 0.6) return '#3b82f6'
  if (recovery > 0.4) return '#f59e0b'
  return '#ef4444'
}
</script>
<style scoped>
.sequence-analysis {
  padding: 24px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  min-height: 100%;
}

/* 鏍囬鏍?*/
.header-section {
  margin-bottom: 32px;
}

.title-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.title-icon {
  width: 28px;
  height: 28px;
  color: #3b82f6;
}

h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.description {
  font-size: 15px;
  color: #64748b;
  margin-left: 40px;
  line-height: 1.6;
}

/* 鍙屽簭鍒楄緭鍏ュ尯鍩?*/
.input-section {
  margin-bottom: 32px;
}

.sequences-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.sequence-input {
  width: 100%;             /* 宸叉纭?*/
  box-sizing: border-box;  /* 寮虹儓寤鸿 */
  background: #ffffff;
  border-radius: 20px;
  padding: 24px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}


.input-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.input-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}

.color-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.char-count {
  font-size: 14px;
  color: #64748b;
  background: #f1f5f9;
  padding: 4px 12px;
  border-radius: 12px;
  font-weight: 500;
}

.textarea-wrapper {
  position: relative;
  width: 100%;
}

.sequence-textarea {
  width: 100%;
  max-width: 100%;
  display: block;
  padding: 20px;
  border-radius: 16px;
  border: 2px solid;
  font-family: 'Courier New', monospace;
  font-size: 16px;
  line-height: 1.6;
  resize: vertical;
  background: #f8fafc;
  transition: all 0.3s ease;
  resize: none;
  box-sizing: border-box;
}

.sequence-textarea:focus {
  outline: none;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.original-sequence .sequence-textarea {
  color: #2563eb; /* 钃濊壊瀛椾綋 */
}

.generated-sequence .sequence-textarea {
  color: #10b981; /* 缁胯壊瀛椾綋 */
}

.sequence-info {
  margin-top: 12px;
}

.nucleotide-stats {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.stat-item {
  font-family: 'Courier New', monospace;
  font-size: 14px;
  color: #64748b;
  background: #f1f5f9;
  padding: 4px 12px;
  border-radius: 8px;
}

/* 鎺у埗鎸夐挳鍖哄煙 */
.control-section {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 32px;
}

.control-buttons {
  display: flex;
  gap: 16px;
}

.control-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 28px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  font-size: 15px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-icon {
  width: 20px;
  height: 20px;
}

.clear-btn {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  color: #475569;
  border: 1px solid #cbd5e1;
}

.clear-btn:hover {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(148, 163, 184, 0.25);
  border-color: #94a3b8;
}

.generate-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
}

.generate-btn:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
}

.generate-btn:disabled {
  opacity: 0.8;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.generate-btn.is-loading:hover {
  transform: none;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.35);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: btn-spin 0.8s linear infinite;
}

@keyframes btn-spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 鎸囨爣灞曠ず鍖哄煙 */
.metrics-section {
  background: #ffffff;
  border-radius: 20px;
  padding: 32px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.metrics-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 28px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f1f5f9;
}

.metrics-icon {
  width: 24px;
  height: 24px;
  color: #3b82f6;
}

.metrics-header span {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.metric-card {
  background: #f8fafc;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #e2e8f0;
  transition: transform 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-4px);
}

.metric-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.metric-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.metric-icon svg {
  width: 24px;
  height: 24px;
}

.metric-info {
  flex: 1;
}

.metric-title {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.metric-subtitle {
  font-size: 14px;
  color: #64748b;
}

.metric-value {
  font-size: 32px;
  font-weight: 800;
  color: #1e293b;
  text-align: center;
  margin-bottom: 16px;
  font-family: 'Courier New', monospace;
}

.metric-progress {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #10b981);
  border-radius: 4px;
  transition: width 1s ease;
}

.progress-label {
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  min-width: 45px;
}

/* 鍒嗘瀽鎽樿 */
.analysis-summary {
  background: #f1f5f9;
  border-radius: 16px;
  padding: 24px;
  border-left: 4px solid #3b82f6;
}

.summary-title {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 12px;
}

.summary-content {
  font-size: 15px;
  line-height: 1.7;
  color: #475569;
}

.highlight-text {
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.7);
}

/* 绌虹姸鎬佹彁绀?*/
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 32px;
  background: #ffffff;
  border-radius: 20px;
  border: 2px dashed #e2e8f0;
}

.empty-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 16px;
  color: #94a3b8;
  text-align: center;
}

/* 鍝嶅簲寮忚璁?*/
@media (max-width: 1024px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .sequence-analysis {
    padding: 16px;
  }
  
  .sequences-row {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .control-buttons {
    flex-direction: column;
    width: 100%;
  }
  
  .control-btn {
    width: 100%;
  }
}
</style>
