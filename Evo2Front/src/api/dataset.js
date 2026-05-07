import api from './index'

export function fetchDatasets() {
  return api.get('/datasets/datasetlist/')
}

export function fetchFilePreview(fileId) {
  return api.get(`/datasets/files/${fileId}/preview/`)
}

export function downloadFile(fileId) {
  return api.get(`/datasets/files/${fileId}/download/`, {
    responseType: 'blob',
  })
}