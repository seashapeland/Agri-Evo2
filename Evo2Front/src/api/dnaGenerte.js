import api from './index'

export function fetchAvailableModels() {
  return api.get('/dnaGenerate/models/').then(response => {
    const data = response?.data ?? {}
    const availableModels = Array.isArray(data.available_models)
      ? data.available_models
      : []

    return {
      ...data,
      available_models: availableModels
    }
  })
}

export function fetchCdsCompletion({
  prompt,
  model,
  tokens = 200,
  temperature = 1.0,
  topk = 40
}) {
  const payload = {
    prompt: String(prompt ?? ''),
    model: String(model ?? ''),
    tokens: Number(tokens),
    temperature: Number(temperature),
    topk: Number(topk)
  }

  return api
    .post('/dnaGenerate/cds-completion/', payload, { timeout: 120000 })
    .then(response => {
      const data = response?.data ?? {}
      const result = data.result ?? {}

      return {
        ...data,
        status: data.status ?? '',
        job_id: data.job_id ?? result.job_id ?? '',
        result: {
          ...result,
          generated: result.generated ?? '',
          full_sequence: result.full_sequence ?? '',
          tokens_generated: Number.isFinite(result.tokens_generated)
            ? result.tokens_generated
            : 0
        }
      }
    })
}
